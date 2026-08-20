## Context

DKF v0.1 is a draft specification expressed entirely as `README.md`. One reference implementation (`particulars-cli` v0.1.0) exists and has published `SPEC-FEEDBACK.md` plus issues #1–#10 describing every point where the draft forced an implementer to guess. The README explicitly invites exactly this feedback and says field names, ID formats and serialisation are open until v0.1 is declared.

Constraints that shape every decision below:

- **Design principles already in the README are load-bearing.** In particular "a consumer that ignores synthesis-specific fields gets a valid claim", "retraction and synthesis are the only mutations", "files over databases", and "the LLM reasons; this tool stores". Proposals are evaluated against these first.
- **Git is the storage layer.** Anything that makes concurrent branches conflict (e.g. an authoritative index) or that rewrites history (e.g. deleting a retracted file) is wrong by construction.
- **Readers should be lenient, writers strict.** Existing workspaces written with draft-era ids must stay readable.
- **There is one implementation.** Breaking the draft is cheap today and expensive after a second implementation appears. Where a cleaner choice exists, take it now and mark it BREAKING.

## Goals / Non-Goals

**Goals:**
- Resolve all ten issues with normative text in `README.md`, so a second implementation could be written without asking the same questions.
- Define the on-disk representation of every mutation and record the tool table implies (retraction, merge).
- Give `conflict_detect` a computable, LLM-free baseline.
- Keep the object model at three knowledge objects.

**Non-Goals:**
- Signing, DID resolution, or the `.well-known` crawling protocol beyond what retraction and merges require.
- A JSON Schema or formal grammar for the format (could follow as its own change).
- Changing the MCP tool list; only `synthesis_create`'s parameter name changes.
- Writing `CONTRIBUTING.md` (referenced but missing; separate concern).
- Updating the reference implementation.

## Decisions

### D1. Identifiers are `<prefix>_<uuidv7>` (#1)

`<prefix>_` + lowercase canonical RFC 9562 UUIDv7, e.g. `clm_019196a5-8b4c-7def-8abc-0123456789ab`. Prefixes: `par`, `clm`, `syn`, `mrg`. Minters SHOULD use a monotonic counter within a millisecond so creation order sorts. Readers MUST accept `^(par|clm|syn|mrg)_[A-Za-z0-9-]+$` so draft-era ULID ids remain readable; validators MAY warn on non-UUIDv7 ids.

The id's embedded time is the *minting* instant; `timestamp` is the *assertion* time and MAY be earlier (e.g. recording a dated document). Consumers MUST NOT require agreement.

*Alternatives:* keep ULID (equally sortable, weaker interop story — no native type in Postgres, Java, Python stdlib); bare UUID without prefix (loses type-at-a-glance in diffs and logs). The prefix is kept because it is what makes `ls claims/` and a PR diff self-describing.

### D2. Retraction is an append-only `retracted` block on the object file (#2)

```yaml
retracted:
  timestamp: 2026-08-21T09:12:00Z
  reason: "Port is 8443, not 443 — deploy/config.yaml:12"
  source: {author: ben}
  superseded-by: clm_…          # optional
```

Rules: it is the only permitted modification to an existing object file; it is never removed; reinstatement is a new claim or synthesis citing the retracted one; syntheses and merge records are retractable by the same mechanism; the index mirrors it as `retracted: true`.

*Why on-file rather than a `ret_` object:* the consumer most at risk of misusing a retracted claim is one that opens only that claim's file. The compatibility principle ("a consumer that ignores the format gets readable YAML") requires the marker to be visible there. It also keeps the knowledge object count at three and yields the clearest diff.

*Signing consequence:* the signed payload is the canonical object **minus** `retracted` and `signature`. A retraction therefore does not invalidate the original signature; the retraction carries its own `source` and may later carry its own signature.

### D3. `superseded-by` is blessed as an optional pointer (#3)

Typo-grade corrections ("8443, not 443") do not warrant a thesis/antithesis synthesis. `superseded-by` MUST reference an existing claim or synthesis id; validators MUST reject dangling targets. It is a convenience pointer for readers and `lineage_trace`; it does not make the target an input of anything and it does not itself count as synthesis for conflict purposes (see D7).

*Alternative:* synthesis-only correction. Rejected: the ceremony cost would push agents toward silently asserting a replacement claim with no link, which is worse provenance than a pointer.

### D4. URIs are "globally unique; resolvable once published", with a minting convention (#4)

- When the workspace has `workspace.base-uri`: `<base-uri><slug>`.
- Otherwise: `urn:dkf:<workspace-id>:<slug>`.
- `slug` = label lower-cased, Unicode NFKD with combining marks stripped, non-`[a-z0-9]` runs collapsed to a single `-`, trimmed. Two labels that slug identically MUST resolve to the same particular (this is what makes `particular_define` idempotent on URI useful).
- Existing global URIs (Wikidata, ORCID, a GitHub URL, DOI) remain preferred when one exists.
- A URI MAY change only while the particular has never been published; afterwards the only path is `particular_merge`.

The spec claims `urn:dkf:` in one sentence. Formal IANA NID registration (RFC 8141) is deferred; the risk is acknowledged in Risks.

*Alternative:* `tag:` URIs (RFC 4151). Rejected because they need a DNS or email authority — i.e. configuration the user must supply before the first particular can be minted — whereas a workspace UUID is generated silently at init.

### D5. `dkf.yaml` is the workspace marker and config (#5)

```yaml
format: dkf/0.1
workspace:
  id: 019196a5-8b4c-7def-8abc-0123456789ab   # bare uuidv7, no prefix
  base-uri: https://example.com/particulars/  # optional; MUST end in '/'
defaults:
  scope: personal
  source:
    author: ben
    harness: claude
```

Discovery: walk up from the working directory until a directory containing `dkf.yaml` is found, exactly like `.git`. `format` and `workspace.id` are required; everything else optional. Unknown keys MUST be ignored. `defaults` are applied by *writers* when a tool call omits a value; they are never applied by readers (see D9).

The workspace id is a bare UUID rather than a prefixed id because it is an identity for a container, not a DKF object, and because it is embedded in URNs where a prefix is noise.

### D6. `index.yaml` is a derived, regenerable cache (#6)

Normative statements: the YAML object files are the source of truth; `index.yaml` MUST be fully reconstructible from them; a local consumer MUST NOT return wrong results because the index is missing or stale (it may be slower); implementations MAY add per-entry fields and consumers MUST ignore unknown ones. The index SHOULD remain committed so HTTP consumers — who cannot list a directory — can enumerate a public workspace; for them it is the enumeration mechanism and MAY lag.

Baseline entry fields stay as in the draft (`id`, `type`, `subject`, `uri`, `inputs`). Blessed optional fields: `scope`, `topics`, `timestamp`, `retracted: true`, and for merges `uris`. Implementations SHOULD provide a rebuild command and a check-for-drift command suitable for CI.

*Why:* two branches that each add a claim both touch the index. If authoritative, every merge is a hand-resolved YAML conflict. If derived, the resolution is "rebuild".

### D7. The merge record (#7)

```yaml
# merges/mrg_019196a5-…yaml
id: mrg_019196a5-8b4c-7def-8abc-0123456789ab
type: merge
uris:
  - https://example.com/particulars/project-x
  - urn:dkf:0191…:projectx
reason: Same project; the URN was minted before the public URI existed.   # optional
source: {author: ben, harness: claude}
timestamp: 2026-08-21T09:30:00Z
```

- Lives under `/merges/`, prefix `mrg_`, `type: merge`. Listed in the index with `uris`.
- Keyed on URIs, not local ids, because a merge routinely spans sources where only one side has a local particular.
- Merges are symmetric and transitive: the set of particulars joined by non-retracted merge records forms an equivalence class. `knowledge_recall`, `conflict_detect` and `lineage_trace` MUST operate over the whole class when given any member. Claims are never rewritten; `subject` keeps pointing at the original particular.
- A merge is retracted via the `retracted` block (D2); retracting it dissolves only that edge.
- Design principle reworded: *three knowledge objects* (particular, claim, synthesis) are the complete core; *retraction* and *merge* are **records** — events about objects, not knowledge — and are the only other things the format defines.

*Alternative:* put `same-as:` on the particular file. Rejected: it mutates a particular (violating "only retraction mutates"), is asymmetric, and cannot carry its own source/retraction.

### D8. Structural conflict semantics (#8)

Per particular (equivalence class, D7):

- **current** — the most recent non-retracted synthesis whose `subject` is in the class, by `timestamp`, ties broken by id.
- **unsynthesised** — non-retracted claims and syntheses with `subject` in the class that are not in the transitive `inputs` of `current`.
- **stale** — non-retracted syntheses with `subject` in the class that cite a retracted input, directly or transitively.

A particular is **reported** when: `current` exists and `unsynthesised` is non-empty; or no `current` exists and `|unsynthesised| ≥ 2`; or `stale` is non-empty. Suggested synthesis priority is `|unsynthesised| + |stale|`. The tool returns these sets; whether any two members actually *contradict* is the harness's job. "The current belief about any particular" is defined as `current` — even when later claims exist — with those later claims visible as `unsynthesised`.

Retraction cascade: retracting an input does not mutate syntheses that cite it (they are immutable and were already reasoned); they become `stale` until a newer synthesis supersedes them. `superseded-by` (D3) does not count as synthesis: a claim whose retraction points at a replacement is simply retracted; the replacement is unsynthesised like any other claim.

Cross-particular inputs (D10): a claim about Y cited by a synthesis about X is *not* thereby synthesised for Y. Membership is computed per class.

### D9. Source requirements, and syntheses carry `source` (#9, #10.1)

A `source` block appears on claims, syntheses, retractions and merges with one shape: `{author?, harness?, model?, document?}`. It MUST contain at least one of `author` or `harness`. `model` and `document` are optional. An agent acting with no human in the loop is a valid source (`{harness, model}`); the format exists for exactly that actor.

A synthesis's `source` MUST additionally contain `harness` (this is the "harness attribution" trust property). `produced-by` is **removed**: a synthesis is a claim and carries `source` like one, so a consumer that ignores synthesis-specific fields genuinely gets a complete claim. `synthesis_create`'s `produced_by` parameter is renamed `source`.

*Why not keep `produced-by` and say it "plays the role of source":* that puts a rule in prose that every naïve consumer must know about, which is the failure mode the compatibility principle exists to prevent. *Why not require `author` everywhere (as the reference implementation does):* it forces a fake author on autonomous runs; `dkf.yaml` defaults make supplying a real one cheap when there is one.

### D10. `context` on disk; cross-particular inputs; `None identified` (#10.2–#10.4)

- **`context` required on disk.** `context` and `context.scope` MUST be present in every claim and synthesis file; `context.topics` is optional. Writers apply `defaults.scope` (or `personal`) at write time. Readers never apply defaults, because scope is a safety property — `knowledge_publish` and public feeds must be able to decide from the file alone, without the workspace config, whether something may be exposed.
- **Cross-particular inputs are intended.** Inputs MAY have a `subject` different from the synthesis's. The spec says so, with the conflict-semantics caveat above.
- **`unresolved: None identified`.** The exact string `None identified` is the conventional value for "considered, nothing outstanding". A literal string rather than `null`/empty is chosen because many YAML loaders conflate a missing key, `null`, and `~`, which would erase the "considered vs forgot" distinction the field exists to preserve. Validators MUST accept it and MUST still reject a missing `unresolved`.

## Risks / Trade-offs

- [`urn:dkf:` is an unregistered URN namespace] → Stated as a claimed-but-unregistered NID; `base-uri` is the recommended path for anyone publishing, and a merge record (D7) exists precisely to join a URN to a later public URI. Formal registration can follow without breaking anything.
- [Renaming `produced-by` → `source` breaks the only implementation] → It is a draft with one implementer who is the author of the feedback; readers of old files can treat `produced-by` as an alias during v0.1. Called out as BREAKING in the proposal.
- [Relaxing `source.author` may reduce human accountability] → Mitigated by `harness` being mandatory where `author` is absent, and by `dkf.yaml` defaults making a real author the path of least resistance.
- [Merge equivalence classes make every query tool transitive] → Classes are small in practice; implementations can cache the class map in the index (additive field). Retracting a bad merge is cheap.
- [Structural conflict detection over-reports] → Deliberate: false positives cost the harness one look; false negatives silently lose contradictions, which is the failure mode the format exists to prevent.
- [`context` required on disk makes hand-written files slightly heavier] → Two lines; the safety argument wins.
- [Slug collisions between genuinely different things with the same label] → Expected and accepted; the remedy is a more specific label or a real URI, same as today. Idempotence on same-label is the feature.

## Open Questions

- Should `retracted.source` be allowed to omit both `author` and `harness` when a signed retraction from a DID is present? Deferred to the signing change; for now the D9 rule applies uniformly.
- Whether `.well-known/knowledge.yaml` `feeds` should list `/knowledge/merges/` by default. This change adds it as an optional example only.
