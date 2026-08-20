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

The format defines three object types. Everything else is implementation.

### `DPARTICULAR`

A particular is a specific, identifiable thing in the world — a person,
project, concept, place, or organisation. Claims are anchored to particulars.
The term is used in its philosophical sense: a concrete individual instance,
distinct from a universal or category.

```yaml
id: par_01j9xk2p3q4r5s6t
type: particular
uri: https://example.com/particulars/project-x   # canonical, globally resolvable
label: Project X                                  # human-readable, non-canonical
aliases:
  - ProjectX
  - project_x
```

The `uri` field is what makes cross-source reasoning possible. Two independent
publishers pointing at the same URI are making claims about the same thing,
regardless of local IDs or labels. For well-known subjects, existing URIs —
Wikidata, DBpedia, ORCID — are preferred over minting new ones.

---

### `DCLAIM`

A claim is an assertion about a particular, with full source provenance.

```yaml
id: clm_07m3zp9s2q1r4t8v
type: claim
subject: par_01j9xk2p3q4r5s6t
content: |
  Project X uses a microservices architecture, with separate
  services for auth, billing, and core API.
source:
  author: ben
  harness: claude
  model: claude-sonnet-4-6
  document: https://example.com/docs/architecture.md
context:
  scope: organisation       # personal | organisation | public
  topics:
    - architecture
    - distributed-systems
timestamp: 2024-08-20T09:00:00Z
confidence: 0.9
```

Claims are immutable once created. Correction happens through synthesis, not
overwriting. Retraction is recorded, not deletion — provenance must always be
traversable.

---

### `DSYNTHESIS`

A synthesis is a resolved claim derived from one or more thesis/antithesis
inputs. It extends `DCLAIM` — it is itself a valid claim and may serve as a
thesis or antithesis input to further syntheses. No intermediate derived-claim
object is needed.

```yaml
id: syn_03p7qr2s4t5u6v7w
type: synthesis
subject: par_01j9xk2p3q4r5s6t
content: |
  Project X ran microservices from 2022–2024, with separate services
  for auth, billing, and core API. The architecture was consolidated
  into a monolith in November 2024 to address latency at scale, though
  service boundaries were preserved as internal modules. The auth
  service remains separately deployable for compliance reasons.
inputs:
  - id: clm_07m3zp9s2q1r4t8v
    role: thesis
    weight: primary
  - id: clm_11n4rs6t7u8v9w0x
    role: antithesis
    weight: primary
  - id: clm_15p8vw2x3y4z5a1b
    role: thesis
    weight: qualifying
unresolved: |
  The compliance basis for retaining a separate auth service is
  asserted but not sourced. Flagged for verification.
produced-by:
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

The `unresolved` field is required. A synthesis that makes no acknowledgement
of what it could not reconcile is considered malformed. Consumers that do not
implement synthesis reasoning MUST treat a `DSYNTHESIS` as a `DCLAIM` using
its `content` field, ignoring synthesis-specific fields.

---

## Object Model

```
DPARTICULAR   the anchor — a specific, identifiable thing

DCLAIM        an assertion about a particular
                ← source: who/what asserted it
                ← subject: which particular it concerns

DSYNTHESIS    extends DCLAIM
                ← inputs[]: N claims with role and weight
                ← unresolved: what wasn't fully reconciled
                ← produced-by: harness and model
                → is itself a valid input to further syntheses
```

The lineage graph is a directed acyclic graph of claims. The current belief
about any particular is the most recent synthesis, but the full graph is always
preserved and traversable.

---

## File Layout

```
/particulars/
  par_01j9xk2p3q4r5s6t.yaml

/claims/
  clm_07m3zp9s2q1r4t8v.yaml
  clm_11n4rs6t7u8v9w0x.yaml

/syntheses/
  syn_03p7qr2s4t5u6v7w.yaml

/index.yaml
```

The index is a lightweight manifest of all IDs, types, subjects, and
relationships. It enables recall and conflict detection without parsing every
file.

```yaml
# index.yaml
format: dkf/0.1
entries:
  - id: par_01j9xk2p3q4r5s6t
    type: particular
    uri: https://example.com/particulars/project-x
  - id: clm_07m3zp9s2q1r4t8v
    type: claim
    subject: par_01j9xk2p3q4r5s6t
  - id: syn_03p7qr2s4t5u6v7w
    type: synthesis
    subject: par_01j9xk2p3q4r5s6t
    inputs:
      - clm_07m3zp9s2q1r4t8v
      - clm_11n4rs6t7u8v9w0x
```

---

## MCP Server Tools

A reference MCP server implementation exposes eleven tools grouped into four
areas.

### Particular Tools

| Tool | Description |
|---|---|
| `particular_define(uri, label, aliases[])` | Create or update a particular. Idempotent on URI. |
| `particular_resolve(query)` | Find a particular by ID, URI, label, or alias. Returns null if no match. |

### Claim Tools

| Tool | Description |
|---|---|
| `claim_assert(particular_id, content, source, context, confidence, scope)` | Create a new claim. Scope defaults to personal. |
| `claim_retract(claim_id, reason, source)` | Mark a claim retracted. Never deletes — provenance is preserved. |

### Synthesis Tools

| Tool | Description |
|---|---|
| `synthesis_create(content, inputs[], unresolved, produced_by)` | Record a synthesis the calling LLM has already reasoned. The LLM reasons; this tool stores. |

### Query Tools

| Tool | Description |
|---|---|
| `knowledge_recall(particular_id \| query, scope, include_retracted, limit)` | Retrieve claims and syntheses about a particular or topic. Returns in lineage order. |
| `conflict_detect(particular_id \| claim_ids[])` | Surface unresolved contradictions. Returns conflict pairs and suggested synthesis priority. |
| `lineage_trace(claim_id, depth)` | Traverse the provenance chain of any claim or synthesis. Returns a structured tree. |

### Federation Tools

| Tool | Description |
|---|---|
| `feed_index(uri, topics[])` | Crawl and index an external knowledge source publishing DKF. Topics enable selective crawling. |
| `particular_merge(uri_a, uri_b, source)` | Declare two URIs as the same particular. Produces a merge record without rewriting claims. |
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
Signatures are optional in v0.1 but the field is reserved.

**Citation weight** — a synthesis that cites a claim increases that claim's
standing in downstream reasoning, analogous to PageRank. Consensus across
independent syntheses is a stronger signal than source confidence alone.

**Harness attribution** — every synthesis records the harness and model that
produced it. This enables downstream reasoning about the reliability of a
synthesis chain in a given domain.

**Scope isolation** — claims scoped `personal` or `organisation` are never
surfaced in public feeds. Promotion to `public` is an explicit act recorded
with a source.

---

## Design Principles

**Contradiction is signal, not error.** The format is built around preserving
disagreement, not resolving it silently.

**Provenance is non-negotiable.** Nothing is overwritten. Retraction and
synthesis are the only mutations. The full reasoning chain is always
traversable.

**Minimal spec, layered implementation.** The three object types are the
complete core. Entity types, ontologies, topic taxonomies, and trust
hierarchies are implementation concerns.

**Backward compatibility by design.** A consumer that ignores synthesis-
specific fields gets a valid claim. A consumer that ignores the format
entirely gets readable YAML. Adoption does not require full implementation.

**Files over databases.** The canonical store is a directory of YAML files
in a git repository. Git provides version history, authorship, and diff
visibility for free. Databases are an implementation optimisation, not a
requirement.

---

## Status

This specification is in early draft. The object model and tool list are
stable. Field names, ID formats, and serialisation details are subject to
change before v0.1 is declared.

Feedback on the spec itself — object model, field names, missing cases — is
the most valuable contribution at this stage. Implementation is premature
until the format is stable.

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
