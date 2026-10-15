## Why

`knowledge_recall` takes `particular_id | query`, and nothing in the README or any spec says what a `query` is or how it matches. Recall by particular is defined to the scenario: across merge classes, by author, by scope, with retracted objects excluded from the index alone, in lineage order with `current` identified. Recall by query is one word in a tool signature. An agent that does not already know the subject — "what did we decide about the auth timeout?" — has no specified route in, and every implementation will invent one. The natural invention is a vector store, and the natural mistake is to let it answer: top-k chunks by cosine similarity, a stale claim outranking its synthesis, a retracted one returned because its embedding was never evicted, personal-scope content embedded into a file someone commits. The format exists to stop that — "current formats treat contradiction as an error to eliminate rather than signal to preserve" — and it should say where similarity search belongs before an implementation decides for it.

The answer is that similarity search may *find* the subject and must never *say what is true about it*. Resolution and recall are two stages. The first turns free text into particulars; the second is the structural recall the specification already defines, unchanged. A vector cache, if an implementation keeps one, serves the first stage only, is derived from the files, is never committed or published, and cannot cause a wrong answer — only a missed candidate, which the always-run lexical baseline bounds.

## What Changes

- **Query resolution is specified.** `knowledge_recall(query)` resolves the query to a set of particulars (and the objects that matched), then answers exactly as `knowledge_recall(particular_id)` would for each, with every filter — scope, author, `include_retracted`, merge classes — applied in the second stage from the files and the index. Each result carries how its particular was found: `label`, `alias`, `lexical`, or `semantic`.
- **An LLM-free lexical baseline is required.** Every conformant implementation matches the query against particular labels and aliases and against object `content`, case-insensitively, without a model — the same posture `conflict_detect` takes. The baseline always runs; a semantic stage may add candidates, never remove them.
- **A semantic side cache is permitted and bounded.** An implementation MAY keep embeddings of particular labels and aliases and of claim and synthesis `content`. The cache is derived, regenerable, tagged with the embedding model that produced it, stored outside the workspace tree, never committed, never published, and never read by a validator. A cache from a different model is not used. A missing or stale cache makes recall less complete, never wrong.
- **Content leaves the machine only by configuration.** An implementation SHALL NOT send object content to a remote embedding service unless explicitly configured to, and SHALL NOT embed objects above a configured scope ceiling — so a personal-scope claim is never shipped to a third party because someone typed a question.
- **The index stays as it is.** Embeddings are not index fields. The index extension rule gains one exclusion: implementations SHALL NOT write vectors or model-derived values into index entries, which are committed and fetched over HTTP.

Not **BREAKING**: no file, field, or tool signature changes. An implementation whose `query` already does case-insensitive matching on labels, aliases and content conforms with the addition of the `resolution` marker.

## Capabilities

### New Capabilities

- `recall-query`: two-stage free-text recall — resolution to particulars, then structural recall — the required lexical baseline, the optional semantic side cache and its rules (derived, model-tagged, uncommitted, unpublished, scope-ceilinged, non-authoritative), and the `resolution` marker on results.

### Modified Capabilities

- `index-manifest`: the requirement that index entries may be extended gains an exclusion — no embedding vectors or other model-derived values in entries.

## Impact

- `README.md` — *Query Tools*: the `knowledge_recall` row says a `query` is resolved to particulars and then recalled structurally, and that each result says how it was found; a new subsection *Recall by query* after *Query Tools* states the two stages, the baseline, and the side cache rules; *`index.yaml`*: one sentence that entries carry no model-derived values; *Design Principles*: *Files over databases* gains the sentence that a vector store, like a database, is an optimisation that finds, never one that answers.
- `particulars-cli` — check what `recall --query` does today; it likely already does some form of substring match. Open an issue for the baseline (labels, aliases, content, case-insensitive), the `resolution` marker, and — separately, as optional — a semantic cache under the user cache directory keyed by `workspace.id`.
- Dogfood: a claim in particulars-knowledge that `query` was unspecified from the first draft, and that the gap surfaced from comparing DKF with a RAG vector store — the comparison located where similarity belongs in a format whose point is that ranking is not belief.
