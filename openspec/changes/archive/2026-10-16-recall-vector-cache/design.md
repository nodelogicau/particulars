## Context

`knowledge_recall(particular_id | query, author?, scope, include_retracted, limit)` is the format's read path. Its `particular_id` form is specified across four specs: `merge-records` (operate over the equivalence class), `source-attribution` (the `author` filter and `relations`), `retraction` (exclusion from the index alone), and `conflict-semantics` (lineage order, `current` as the belief, later claims as unsynthesised). Its `query` form is specified nowhere.

Two facts about the format shape the answer. First, objects are immutable apart from retraction, which is recorded in the index's `retracted` lists — so anything derived from an object's `content` is valid for as long as the object exists. Second, *Unbounded History, Bounded Work* binds operations that concern a bounded part of a workspace. A free-text query over everything is not such an operation, so a linear scan is conformant; it is also the cost a cache exists to remove, and the rule is the yardstick for whether the cache's maintenance stays bounded.

## Goals / Non-Goals

**Goals:**
- Give `query` a meaning every implementation shares, including one with no model available.
- Let an implementation use embeddings to find subjects the user cannot name, without letting similarity become belief.
- Keep the files the source of truth and the committed index model-free.
- Keep personal-scope content from leaving the machine because a question was asked.

**Non-Goals:**
- Choosing an embedding model, a vector library, a distance metric, or a similarity threshold.
- Ranking results by similarity. Within a particular, order stays lineage order.
- Retrieval over `source.document` bodies or other material the workspace has not made into claims — that is ingestion, and the format leaves it to the harness.
- A wire or file format for the cache. Caches are not exchanged.
- Semantic search across federated feeds. A consumer of a feed may build its own cache from what it fetched, under the same rules; nothing is published for it.

## Decisions

### D1. Two stages: resolve to particulars, then recall structurally

The query resolves to a set of particulars — merge classes, once resolved — and the response is the union of `knowledge_recall(particular_id)` for each, with the caller's `author`, `scope` and `include_retracted` applied in that second stage. Objects that matched in stage one are marked in the response, but every object returned comes from stage two.

*Why particulars and not objects.* Returning matched claims directly is RAG with extra fields: a stale claim that happens to match beats the synthesis that superseded it, and the caller never sees `current`. Mapping a hit to its subject and recalling the subject means the answer to "what about the auth timeout?" is the timeout's lineage, current belief first, whichever object the words happened to land on.

*Alternative considered:* rank objects by similarity and attach each one's `current`. Rejected — it puts two orderings in one response, and the one a model reads first is the similarity order.

### D2. Filters apply in stage two only

Scope, author, retraction and merge classes are evaluated against the files and index exactly as for `particular_id`. Stage one is allowed to be wrong in one direction: it can propose a particular that turns out to have nothing in scope (dropped) or miss one (lost recall). It cannot cause a retracted or out-of-scope object to be returned, because stage one returns no objects. This is what makes the cache safe to be stale.

### D3. A required lexical baseline, always run

Case-insensitive match of the query against particular labels and aliases, and against object `content` — Unicode case folding, substring of the whole query and of each whitespace-separated term, no stemming required. Results carry `resolution`: `label` or `alias` for an exact match of the whole query, `lexical` for content or partial matches, `semantic` for candidates only the cache found. A particular found several ways carries the strongest, in that order.

*Why required.* `conflict_detect` set the precedent: the format defines an LLM-free baseline and leaves judgement to the harness. Without one, two conformant servers given the same workspace and the same query could disagree about whether a particular named in the query exists. With it, an exact name always resolves, whatever the cache holds.

*Why always run, even with a cache.* Embeddings are weak at exact identifiers — a ticket number, an id, a surname. The union means the cache can only add.

*Alternative considered:* BM25 or another ranked lexical method as the baseline. Rejected as a requirement — it needs a corpus statistic the format would then have to define. Implementations may rank however they like inside stage one, because stage-one order never reaches the response.

### D4. The semantic cache: what, where, keyed by what

- **What is embedded:** each particular's label and aliases; each claim's and synthesis's `content`. Not `context`, not `source`, not records. Retracted objects may stay embedded — D2 removes them — so retraction never has to touch the cache.
- **Where:** outside the workspace tree, in the user's cache directory, keyed by `workspace.id`. The spec requires only that it be outside the tree and never committed; the location is a recommendation. Keeping it out of the tree means no `.gitignore` entry to forget and no chance a publisher's static host serves it.
- **Keyed by:** object id and the embedding model's identifier. The cache records one model; on a model mismatch it is not consulted, and the implementation rebuilds it or falls back to the baseline. Immutability means an id's vector never needs recomputing under the same model, so the cache can be checked for completeness without reading files: entries in the index with no vector are the work list.
- **Bounded maintenance:** after a write, the new ids are embedded. After a pull, the ids in the index not in the cache are embedded. In a `dkf/0.2` workspace a sealed month whose segment `count` the cache has already covered needs no attention, by the same argument the drift check uses.

*Alternative considered:* commit the cache beside `index.yaml` so collaborators share the cost. Rejected — vectors are model-specific (a collaborator on another model gets nothing), large (a 1,024-float vector is 4 KB, near the 6.7 KB per entry the index already costs), and derived from content whose scope a static host cannot enforce.

### D5. Remote embedding and the scope ceiling

Embedding locally needs nothing. Embedding through a remote service sends `content` to a third party, so it requires explicit configuration, and the configuration names a scope ceiling — objects whose effective scope is narrower than the ceiling (by default `public` when remote, so only public objects are sent) are not embedded. They remain findable through the baseline. Effective scope includes promotion records, so a claim promoted to public becomes eligible on the next update.

Configuration lives in the implementation, not `dkf.yaml`: `dkf.yaml` travels with the workspace, and whether this machine may call that service is a property of the machine.

### D6. Index entries stay model-free

`index-manifest` lets implementations add entry fields. That stays, with one exclusion: no embedding vectors or other values derived from a model. The index is committed, fetched over HTTP by crawlers, and compared byte-for-byte by drift checks across implementations. A field that depends on which model a writer ran would make two conformant writers produce different indexes for the same workspace — every drift check between them would fail.

## Risks / Trade-offs

- [A stale or partial cache silently loses recall] → The baseline always runs, so exact names never miss; implementations report cache coverage (`semantic: n of m objects`) in the response metadata so a caller can see that recall was partial.
- [Semantic candidates drag in unrelated particulars] → They are marked `semantic`, and `limit` applies to particulars with baseline matches ranked before semantic ones. A harness can ignore `semantic` results entirely.
- [The baseline is linear in history] → Conformant: a free-text query is not a bounded operation. The cache is the remedy, and implementations may additionally keep a lexical index (e.g. an FTS table) under the same uncommitted, derived rules.
- [A cache on disk holds derived personal-scope content] → It is no more sensitive than the workspace it was derived from and sits beside it on the same machine; implementations create it with user-only permissions. The remote case is D5.
- [Mapping hits to particulars loses the specific claim that matched] → The response marks matched objects within each particular's lineage, so the caller sees both the belief and why the particular was returned.

## Migration Plan

None for workspaces. Implementations add the baseline and the `resolution` marker; a cache is optional and can be deleted at any time.

## Open Questions

- Should `knowledge_recall` take a `resolution` filter (e.g. `semantic: false`) so a harness can ask for exact-only recall? Leaning no — the marker suffices — until an implementation needs it.
- Resolved here rather than left open: `particular_resolve(query)` does not gain a semantic stage. It returns null rather than guess, and that is a feature — `recall-query` states it.
