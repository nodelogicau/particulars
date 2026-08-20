# Dialectical Knowledge Format (DKF)

An open format for portable, interoperable knowledge — designed to work across
AI harnesses, applications, and the public internet.

---

## The Problem

AI assistants are increasingly how people capture, organise, and reason over
knowledge. But every harness — Claude, ChatGPT, Gemini, and others — stores
what it learns in a proprietary silo. Knowledge shared with one is invisible to
another. There is no equivalent of `.ics` for calendar data: no open, portable
format that any application can publish, consume, and reason over.

Existing memory frameworks solve parts of this — persistence within a harness,
cross-session recall, vector search — but none address the deeper problem: that
knowledge evolves through contradiction, and current formats treat contradiction
as an error to eliminate rather than signal to preserve.

---

## The Approach

DKF draws on the structure of Hegelian dialectic: a **thesis** is confronted by
an **antithesis**, and their reconciliation produces a **synthesis** — a richer
claim that carries the reasoning that produced it. That synthesis becomes the
new thesis, available to be contradicted and refined again.

This makes contradiction a first-class citizen of the format. Rather than
silently overwriting a stale fact, DKF records what was believed, what
challenged it, how it was resolved, and what remains unresolved. Any harness
consuming the result inherits not just the conclusion but the reasoning chain.

The approach is analogous to what OpenSpec does for code: rather than storing
the current state of knowledge, DKF records the process by which knowledge
was formed — making it portable, inspectable, and trustworthy across systems.

---

## Core Object Types

The format defines three knowledge object types — particular, claim, and
synthesis — and two record types that describe events about them: retraction
and merge. Everything else is implementation.

### Identifiers

Every object and record id is `<prefix>_` followed by a lowercase canonical
UUID version 7 ([RFC 9562](https://www.rfc-editor.org/rfc/rfc9562)):

| Prefix | Type |
|---|---|
| `par_` | particular |
| `clm_` | claim |
| `syn_` | synthesis |
| `mrg_` | merge record |

```
clm_01916f03-b680-71a3-974f-9401ba374e1f
```

UUIDv7 is time-ordered, so `ls claims/` is a chronological log and new files
cluster at the end of a diff. Implementations MUST mint with a monotonic
counter so that ids created within the same millisecond still sort in creation
order.

The time embedded in an id is the **minting** instant. The `timestamp` field on
an object is the **assertion** time and may be earlier — for example when
recording a dated document. Consumers MUST NOT require the two to agree.

Readers MUST accept any id matching `^(par|clm|syn|mrg)_[A-Za-z0-9-]+$`, so
that workspaces written with other schemes (including earlier drafts of this
specification) remain readable. Validators MAY warn on ids that are not
UUIDv7.

### Source

Claims, syntheses, retractions, and merge records all carry a `source` block
of the same shape:

```yaml
source:
  author: ben                 # a person
  harness: claude             # the AI harness, if one was involved
  model: claude-sonnet-4-6    # the model, if known
  document: https://…         # what was read to make the assertion
```

All four fields are optional individually, but a `source` MUST contain at
least one of `author` or `harness`. An agent acting with no human in the loop
is a valid source (`{harness, model}`); a person working without an assistant
is a valid source (`{author}`). A `source` with neither is malformed.
Syntheses additionally require `source.harness` — see below.

---

### `DPARTICULAR`

A particular is a specific, identifiable thing in the world — a person,
project, concept, place, or organisation. Claims are anchored to particulars.
The term is used in its philosophical sense: a concrete individual instance,
distinct from a universal or category.

```yaml
id: par_01916f03-b680-71a2-bad4-40b49d5a5a6d
type: particular
uri: https://example.com/particulars/project-x   # globally unique; resolvable once published
label: Project X                                  # human-readable, non-canonical
aliases:
  - ProjectX
  - project_x
```

The `uri` field is what makes cross-source reasoning possible. Two independent
publishers pointing at the same URI are making claims about the same thing,
regardless of local IDs or labels. For well-known subjects, existing URIs —
Wikidata, DBpedia, ORCID, a DOI, a GitHub URL — are preferred over minting new
ones.

A URI must be **globally unique**. It is not required to be resolvable until
the particular is published to `public` scope: most things an agent learns
about — a module, a decision, an internal service — have no public URL.

#### Minting URIs

When `particular_define` is called without a `uri`, the implementation mints
one:

- `<base-uri><slug>` when the workspace declares a `base-uri` (see
  [`dkf.yaml`](#dkfyaml)), e.g. `https://example.com/particulars/project-x`;
- otherwise `urn:dkf:<workspace-id>:<slug>`, e.g.
  `urn:dkf:01916cb5-32a0-7001-90a6-6195d31a5bb6:project-x`.

`slug` is derived from the label: lower-case it, apply Unicode NFKD and strip
combining marks, collapse every run of characters outside `[a-z0-9]` to a
single `-`, and trim leading and trailing `-`. `Café Société` becomes
`cafe-societe`. Because `particular_define` is idempotent on URI, two labels
that slug identically resolve to the same particular — which is what stops an
agent re-inventing a subject under a slightly different name each session.

This specification claims the `urn:dkf:` namespace for this purpose. Formal
registration of the NID is deferred; publishers are encouraged to configure a
`base-uri` instead, and a merge record can later join a URN to a public URI.

A particular's `uri` may change only while the particular has never been
published. After publication, the only way to join two URIs is a
[merge record](#merge-records).

---

### `DCLAIM`

A claim is an assertion about a particular, with full source provenance.

```yaml
id: clm_01916f03-b680-71a3-974f-9401ba374e1f
type: claim
subject: par_01916f03-b680-71a2-bad4-40b49d5a5a6d
content: |
  Project X uses a microservices architecture, with separate
  services for auth, billing, and core API.
source:
  author: ben
  harness: claude
  model: claude-sonnet-4-6
  document: https://example.com/docs/architecture.md
context:
  scope: organisation       # personal | organisation | public — required
  topics:                   # optional
    - architecture
    - distributed-systems
timestamp: 2024-08-20T09:00:00Z
confidence: 0.9
```

`context` and `context.scope` are **required on disk** for every claim and
synthesis. `context.topics` is optional and defaults to empty. When a caller
omits scope, the *writer* applies the workspace default (or `personal`) before
the file is written. Readers never infer a scope: whether an object may appear
in a public feed must be decidable from the file alone, without reference to
workspace configuration.

Claims are immutable once created. Correction happens through synthesis or
retraction, never overwriting. Retraction is recorded, not deletion —
provenance must always be traversable.

---

### `DSYNTHESIS`

A synthesis is a resolved claim derived from one or more thesis/antithesis
inputs. It extends `DCLAIM` — it is itself a valid claim and may serve as a
thesis or antithesis input to further syntheses. No intermediate derived-claim
object is needed.

```yaml
id: syn_01933034-b1a0-705f-b788-2c7c58c46e29
type: synthesis
subject: par_01916f03-b680-71a2-bad4-40b49d5a5a6d
content: |
  Project X ran microservices from 2022–2024, with separate services
  for auth, billing, and core API. The architecture was consolidated
  into a monolith in November 2024 to address latency at scale, though
  service boundaries were preserved as internal modules. The auth
  service remains separately deployable for compliance reasons.
inputs:
  - id: clm_01916f03-b680-71a3-974f-9401ba374e1f
    role: thesis
    weight: primary
  - id: clm_01932b8b-c300-70c4-b1f5-270e927328ce
    role: antithesis
    weight: primary
  - id: clm_01932f48-7ce0-72e1-8c4e-af7596e72997
    role: thesis
    weight: qualifying
unresolved: |
  The compliance basis for retaining a separate auth service is
  asserted but not sourced. Flagged for verification.
source:
  harness: claude
  model: claude-sonnet-4-6
method: reconciliation
timestamp: 2024-11-15T14:23:00Z
context:
  scope: organisation
  topics:
    - architecture
    - distributed-systems
confidence: 0.85
```

A synthesis carries `source` exactly as a claim does, and `source.harness` is
required: every synthesis records the harness that produced it. (Earlier
drafts used a separate `produced-by` field. Readers MAY treat a legacy
`produced-by` block as `source` during v0.1 and SHOULD warn.)

Inputs MAY have a different `subject` than the synthesis. A claim about a
library can legitimately inform a synthesis about the project that uses it.
Note that citing it does not count as synthesising it for the library's own
particular — see [Conflict semantics](#conflict-semantics).

The `unresolved` field is required. A synthesis that makes no acknowledgement
of what it could not reconcile is considered malformed. When the producer
considered the question and found nothing outstanding, the conventional value
is the exact string `None identified`; this lets tooling distinguish
"considered and empty" from "forgotten". A missing, null, or empty
`unresolved` is invalid.

Consumers that do not implement synthesis reasoning MUST treat a `DSYNTHESIS`
as a `DCLAIM` using its `content` field, ignoring synthesis-specific fields.

---

### Retraction

Retraction is recorded by appending a `retracted` block to the retracted
object's own file:

```yaml
# claims/clm_01a01ed5-c040-73b0-ba7b-da8a27ab53a6.yaml
id: clm_01a01ed5-c040-73b0-ba7b-da8a27ab53a6
type: claim
subject: par_01916f03-b680-71a2-bad4-40b49d5a5a6d
content: The billing service listens on port 443.
source: {author: ben, harness: claude}
context: {scope: organisation}
timestamp: 2026-08-20T11:02:00Z
retracted:
  timestamp: 2026-08-21T09:12:00Z
  reason: "Port is 8443, not 443 — deploy/config.yaml:12"
  source: {author: ben}
  superseded-by: clm_01a02396-7ca0-718d-9a6e-86fd10508af1   # optional
```

Rules:

- Adding a `retracted` block is the **only permitted modification** to an
  existing object file. `timestamp`, `reason`, and `source` are required.
- It is never removed. Reinstatement is a new claim or synthesis that cites
  the retracted object.
- Syntheses are claims and may be retracted. Merge records may be retracted.
- The index mirrors it as `retracted: true`.

The marker lives on the file rather than in a separate object because the
consumer most likely to misuse a retracted claim is one that opens only that
claim's file. A reader that ignores the format entirely still sees the
retraction beneath the claim.

**`superseded-by`** is an optional pointer for typo-grade corrections where a
full thesis/antithesis synthesis would be ceremony. It MUST reference an
existing claim or synthesis; validators reject a dangling target. It is
informational — for readers and `lineage_trace` — and does not make the target
an input of anything, nor does it count as synthesis for conflict detection.

---

### Merge records

`particular_merge` declares that two URIs denote the same particular. It
produces a merge record and rewrites nothing:

```yaml
# merges/mrg_01a023a7-e1c0-70a7-9232-ad5090460a2d.yaml
id: mrg_01a023a7-e1c0-70a7-9232-ad5090460a2d
type: merge
uris:
  - https://example.com/particulars/project-x
  - urn:dkf:01916cb5-32a0-7001-90a6-6195d31a5bb6:projectx
reason: Same project; the URN was minted before the public URI existed.  # optional
source: {author: ben, harness: claude}
timestamp: 2026-08-21T09:30:00Z
```

`uris` contains exactly two URIs. Merges are keyed on URIs rather than local
ids because a merge routinely spans sources where only one side has a local
particular.

Non-retracted merge records are **symmetric and transitive**: the particulars
they join form an equivalence class. `knowledge_recall`, `conflict_detect`,
and `lineage_trace`, given any member of a class, operate over the whole
class. Claims keep their original `subject`; nothing is moved or rewritten. A
merge is undone by retracting it, which removes only that edge.

---

## Object Model

```
DPARTICULAR   the anchor — a specific, identifiable thing

DCLAIM        an assertion about a particular
                ← source: who/what asserted it
                ← subject: which particular it concerns
                ← context: scope (required) and topics

DSYNTHESIS    extends DCLAIM
                ← inputs[]: N claims with role and weight
                ← unresolved: what wasn't fully reconciled
                ← source.harness: required
                → is itself a valid input to further syntheses

records       retraction — a block appended to any of the above
              merge      — joins two particular URIs
```

The lineage graph is a directed acyclic graph of claims. The full graph is
always preserved and traversable.

### Conflict semantics

Without an LLM in the loop, "contradiction" is not computable. What *is*
computable is what has not been reconciled, and every consumer can rely on
that. For a particular (or merge equivalence class):

- **current** — the most recent non-retracted synthesis whose `subject` is in
  the class, ordered by `timestamp`, ties broken by id.
- **unsynthesised** — non-retracted claims and syntheses with `subject` in the
  class that are not in the transitive `inputs` of `current`.
- **stale** — non-retracted syntheses with `subject` in the class that cite a
  retracted input, directly or transitively.

**The current belief about a particular is `current`**, even when claims
post-date it. Those later claims are not silently the new belief; they are
surfaced as `unsynthesised` until a synthesis absorbs them.

`conflict_detect` reports a particular when:

- `current` exists and `unsynthesised` is non-empty; or
- `current` does not exist and `unsynthesised` has two or more members; or
- `stale` is non-empty.

The suggested synthesis priority is `|unsynthesised| + |stale|`. Whether any
two members actually contradict is the reasoning harness's judgement, not the
tool's.

Two consequences follow:

- **Retraction does not cascade by mutation.** Retracting an input leaves the
  syntheses that cite it untouched — they are immutable and were already
  reasoned. They are reported as `stale` until a newer synthesis supersedes
  them. A `superseded-by` pointer is not synthesis: the replacement object is
  `unsynthesised` like any other.
- **Cross-particular inputs are per class.** A claim about Y cited by a
  synthesis about X is not thereby synthesised for Y.

---

## File Layout

```
/dkf.yaml                      workspace marker and configuration

/particulars/
  par_01916f03-b680-71a2-bad4-40b49d5a5a6d.yaml

/claims/
  clm_01916f03-b680-71a3-974f-9401ba374e1f.yaml
  clm_01932b8b-c300-70c4-b1f5-270e927328ce.yaml

/syntheses/
  syn_01933034-b1a0-705f-b788-2c7c58c46e29.yaml

/merges/
  mrg_01a023a7-e1c0-70a7-9232-ad5090460a2d.yaml

/index.yaml                    derived cache — see below
```

### `dkf.yaml`

A workspace is identified by a `dkf.yaml` at its root. Implementations find
the workspace by walking up from the working directory until they encounter
one, exactly as git finds `.git`.

```yaml
format: dkf/0.1
workspace:
  id: 01916cb5-32a0-7001-90a6-6195d31a5bb6   # bare uuidv7; used in urn:dkf: URIs
  base-uri: https://example.com/particulars/  # optional; MUST end in '/'
defaults:                                     # optional
  scope: personal
  source:
    author: ben
    harness: claude
```

`format` and `workspace.id` are required; everything else is optional.
Implementations MUST ignore unknown keys so the file can be extended.

`defaults` are applied by **writers only**, when a tool call omits a value:
`scope` fills `context.scope`; `source` fields fill an incomplete `source`.
Readers never consult `defaults` — every object file is interpretable on its
own.

### `index.yaml`

The index is a lightweight manifest of all IDs, types, subjects, and
relationships. It enables recall and conflict detection without parsing every
file.

The object and record files are the **source of truth**. The index is a
derived, regenerable cache: it MUST be fully reconstructible from the files,
and a local consumer MUST NOT return wrong results because it is missing or
stale (it may be slower). Two branches that each add a claim will both touch
`index.yaml`; the conflict is resolved by regenerating it, never by hand.

The index nonetheless stays committed, because HTTP consumers cannot list a
directory — for them it is the enumeration mechanism, and they should treat it
as potentially lagging the files.

```yaml
# index.yaml
format: dkf/0.1
entries:
  - id: par_01916f03-b680-71a2-bad4-40b49d5a5a6d
    type: particular
    uri: https://example.com/particulars/project-x
  - id: clm_01916f03-b680-71a3-974f-9401ba374e1f
    type: claim
    subject: par_01916f03-b680-71a2-bad4-40b49d5a5a6d
    scope: organisation
    topics: [architecture, distributed-systems]
    timestamp: 2024-08-20T09:00:00Z
  - id: clm_01a01ed5-c040-73b0-ba7b-da8a27ab53a6
    type: claim
    subject: par_01916f03-b680-71a2-bad4-40b49d5a5a6d
    scope: organisation
    timestamp: 2026-08-20T11:02:00Z
    retracted: true
  - id: syn_01933034-b1a0-705f-b788-2c7c58c46e29
    type: synthesis
    subject: par_01916f03-b680-71a2-bad4-40b49d5a5a6d
    inputs:
      - clm_01916f03-b680-71a3-974f-9401ba374e1f
      - clm_01932b8b-c300-70c4-b1f5-270e927328ce
      - clm_01932f48-7ce0-72e1-8c4e-af7596e72997
    scope: organisation
    timestamp: 2024-11-15T14:23:00Z
  - id: mrg_01a023a7-e1c0-70a7-9232-ad5090460a2d
    type: merge
    uris:
      - https://example.com/particulars/project-x
      - urn:dkf:01916cb5-32a0-7001-90a6-6195d31a5bb6:projectx
```

Baseline fields: every entry has `id` and `type`; particulars have `uri`;
claims and syntheses have `subject`; syntheses have `inputs`; merges have
`uris`. Entries MAY also carry `scope`, `topics`, `timestamp`, and
`retracted: true` so that `knowledge_recall` can filter without opening files.
Implementations MAY add further fields; consumers MUST ignore fields they do
not understand.

Implementations are expected to provide an operation that rebuilds the index
from the files, and a check that reports — without modifying anything —
whether the committed index has drifted from the files, suitable for CI.

---

## MCP Server Tools

A reference MCP server implementation exposes eleven tools grouped into four
areas.

### Particular Tools

| Tool | Description |
|---|---|
| `particular_define(uri?, label, aliases[])` | Create or update a particular. Idempotent on URI. When `uri` is omitted one is minted from the label (see [Minting URIs](#minting-uris)). |
| `particular_resolve(query)` | Find a particular by ID, URI, label, or alias. Returns null if no match. |

### Claim Tools

| Tool | Description |
|---|---|
| `claim_assert(particular_id, content, source, context, confidence, scope)` | Create a new claim. If scope is omitted the workspace default (or `personal`) is written into the file. |
| `claim_retract(claim_id, reason, source)` | Append a `retracted` block to a claim or synthesis. Never deletes — provenance is preserved. |

### Synthesis Tools

| Tool | Description |
|---|---|
| `synthesis_create(content, inputs[], unresolved, source)` | Record a synthesis the calling LLM has already reasoned. `source.harness` is required. The LLM reasons; this tool stores. |

### Query Tools

| Tool | Description |
|---|---|
| `knowledge_recall(particular_id \| query, scope, include_retracted, limit)` | Retrieve claims and syntheses about a particular or topic. Returns in lineage order, identifying `current`. Operates across merged particulars. |
| `conflict_detect(particular_id \| claim_ids[])` | Return the structural `current` / `unsynthesised` / `stale` sets and a suggested synthesis priority (see [Conflict semantics](#conflict-semantics)). Judging actual contradiction is left to the harness. |
| `lineage_trace(claim_id, depth)` | Traverse the provenance chain of any claim or synthesis, including `superseded-by` successors. Returns a structured tree. |

### Federation Tools

| Tool | Description |
|---|---|
| `feed_index(uri, topics[])` | Crawl and index an external knowledge source publishing DKF. Topics enable selective crawling. |
| `particular_merge(uri_a, uri_b, source)` | Declare two URIs as the same particular. Writes a [merge record](#merge-records) without rewriting claims. |
| `knowledge_publish(claim_ids[], scope)` | Promote claims from personal or organisation scope to public. Explicit and deliberate — not a default. |

The typical LLM reasoning loop is:

```
particular_resolve → knowledge_recall → conflict_detect
  → [reason internally] → synthesis_create
```

---

## Public Discovery

Publishers exposing DKF knowledge on the public internet place a manifest at
a well-known path:

```yaml
# https://example.com/.well-known/knowledge.yaml
format: dkf/0.1
index: /knowledge/index.yaml
feeds:
  - /knowledge/claims/
  - /knowledge/syntheses/
  - /knowledge/merges/        # optional
topics:
  - distributed-systems
  - knowledge-management
publisher:
  uri: did:web:example.com
  label: Example Organisation
```

Crawlers discover feeds via this manifest. The `topics` field enables targeted
crawling — a reasoning task scoped to a domain only fetches sources that
declare relevance. Scope must be `public` for a claim to appear in a public
feed.

---

## Trust and Provenance

**Cryptographic signing** — claims may be signed with the publisher's DID.
Signatures are optional in v0.1 but the field is reserved. The signed payload
is the canonical object **minus** the `retracted` and `signature` fields, so a
later retraction does not invalidate the original signature; the retraction
carries its own `source`.

**Citation weight** — a synthesis that cites a claim increases that claim's
standing in downstream reasoning, analogous to PageRank. Consensus across
independent syntheses is a stronger signal than source confidence alone.

**Harness attribution** — every synthesis records the harness that produced
it in `source.harness`, and the model in `source.model` where known. This
enables downstream reasoning about the reliability of a synthesis chain in a
given domain.

**Scope isolation** — claims scoped `personal` or `organisation` are never
surfaced in public feeds. Promotion to `public` is an explicit act recorded
with a source. Scope is always present in the file itself, so the decision
never depends on workspace configuration.

---

## Design Principles

**Contradiction is signal, not error.** The format is built around preserving
disagreement, not resolving it silently.

**Provenance is non-negotiable.** Nothing is overwritten. Appending a
retraction is the only modification to an existing file; synthesis is the
only way to change what is believed. The full reasoning chain is always
traversable.

**Minimal spec, layered implementation.** Three knowledge objects —
particular, claim, synthesis — are the complete core, plus two records —
retraction and merge — that are events about objects rather than knowledge.
Entity types, ontologies, topic taxonomies, and trust hierarchies are
implementation concerns.

**Backward compatibility by design.** A consumer that ignores synthesis-
specific fields gets a valid claim. A consumer that ignores `/merges/` still
reads every claim correctly. A consumer that ignores the format entirely gets
readable YAML. Adoption does not require full implementation.

**Files over databases.** The canonical store is a directory of YAML files
in a git repository. Git provides version history, authorship, and diff
visibility for free. The index is a cache of the files, never the reverse.
Databases are an implementation optimisation, not a requirement.

---

## Status

This specification is in early draft. The object model, tool list, identifier
format, retraction and merge representations, and the structural conflict
semantics are stable. Field names and serialisation details for signing and
public crawling remain subject to change before v0.1 is declared.

A reference implementation,
[`particulars-cli`](https://github.com/nodelogicau/particulars-cli), exists
and its feedback shaped the current text.

Feedback on the spec itself — object model, field names, missing cases — is
the most valuable contribution at this stage.

---

## Contributing

Open an issue to discuss changes to the object model or field definitions
before submitting a pull request. The spec is a human document first;
implementation follows from it, not the other way around.

See [CONTRIBUTING.md](CONTRIBUTING.md) for guidance on proposing changes,
the RFC process for breaking changes, and how to submit a reference
implementation.

---

## License

The specification is released under [CC0 1.0 Universal](LICENSE). Reference
implementations are released under the MIT License. You are free to implement
the format without restriction.
