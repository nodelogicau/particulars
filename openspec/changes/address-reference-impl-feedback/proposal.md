## Why

The `particulars-cli` reference implementation (v0.1.0) surfaced ten places where the DKF v0.1 draft forced an implementer to make a decision the spec does not make — identifier format, how a retraction is represented, what a merge record is, what `conflict_detect` can actually compute without an LLM, which `source` fields are mandatory, and so on. These are tracked as GitHub issues [#1](https://github.com/nodelogicau/particulars/issues/1)–[#10](https://github.com/nodelogicau/particulars/issues/10). The README says feedback on the object model and missing cases is the most valuable contribution before v0.1 is declared; resolving these now, while there is exactly one implementation, avoids baking divergent choices into a second one.

## What Changes

All changes are to the specification text in `README.md`. The object model (particular / claim / synthesis) is unchanged; the changes pin down details it leaves open.

- **Identifiers** (#1): IDs become `<prefix>_` + lowercase canonical UUIDv7. Readers accept any `^(par|clm|syn|mrg)_[A-Za-z0-9-]+$`. The id's embedded time is the minting instant; `timestamp` is the assertion time and may differ. **BREAKING** for the draft's example ids (truncated ULIDs), which are still readable.
- **Retraction representation** (#2, #3): an append-only `retracted` block on the object file (`timestamp`, `reason`, `source`, optional `superseded-by`). It is the only permitted modification to an existing object file and is never removed. Syntheses may be retracted. The reserved signature covers the object minus `retracted` and `signature`.
- **Particular URIs** (#4): `uri` is "globally unique; resolvable once published" rather than "globally resolvable". A minting convention is blessed: `<base-uri><slug>` when the workspace has a base URI, otherwise `urn:dkf:<workspace-id>:<slug>`; the `urn:dkf:` namespace is claimed. A URI may change only while never published; afterwards `particular_merge` is the only path.
- **Workspace configuration** (#5): a `dkf.yaml` at the workspace root is the discovery marker and carries `format`, `workspace.id`, optional `workspace.base-uri`, and `defaults` (scope, source). Unknown keys are ignored.
- **Index is derived** (#6): `index.yaml` is a regenerable cache, never the source of truth; implementations may add entry fields (`scope`, `topics`, `timestamp`, `retracted`, …); a stale or missing index must not produce wrong results locally.
- **Merge record** (#7): a fourth on-disk record type, `mrg_<uuidv7>` under `/merges/`, with `uris`, `source`, `timestamp`, optional `reason`, retractable via the same `retracted` block. Query tools treat the transitive closure of non-retracted merges as one particular. The "three object types" principle is reworded as three *knowledge* objects plus *records* (retraction, merge) that are events about objects.
- **Conflict semantics** (#8): `conflict_detect` is defined structurally — `current`, `unsynthesised`, `stale` — with the semantic judgement of contradiction left to the reasoning harness. This also gives "current belief" a precise meaning and defines the retraction cascade (stale, not mutated).
- **Source requirements** (#9): a `source` (on claims, syntheses, retractions, merges) MUST carry at least one attributing field, `author` or `harness`; `model` and `document` are optional. Agent-only claims with no human in the loop are valid. A synthesis `source` MUST carry `harness`.
- **Synthesis `source`** (#10.1): syntheses carry `source` like any claim; the separate `produced-by` field is removed so that "a consumer that ignores synthesis-specific fields gets a valid claim" holds literally. `synthesis_create`'s `produced_by` parameter becomes `source`. **BREAKING** for the draft example and the reference implementation's field name.
- **`context` required** (#10.2): `context` and `context.scope` MUST be present on disk; tools apply the `personal` default at write time, not read time. `topics` is optional.
- **Cross-particular inputs** (#10.3): a synthesis's inputs MAY have a different `subject` than the synthesis; this is intended and stated.
- **Empty `unresolved`** (#10.4): the literal `None identified` is the conventional value meaning "considered, nothing outstanding".

## Capabilities

### New Capabilities
- `object-identifiers`: ID format (`<prefix>_<uuidv7>`), read-side leniency, minting-time vs assertion-time.
- `retraction`: the `retracted` block, its immutability rules, `superseded-by`, effect on signatures and the index.
- `particular-uris`: URI uniqueness vs resolvability, the minting convention, the `urn:dkf:` namespace, URI change rules.
- `workspace-config`: `dkf.yaml` schema, discovery by walking up, defaults, forward compatibility.
- `index-manifest`: index as derived cache, baseline entry fields, additive fields, rebuild/check behaviour.
- `merge-records`: the `mrg_` record, its fields and location, equivalence-class semantics for query tools, retractability.
- `conflict-semantics`: structural definitions of current / unsynthesised / stale, reporting rule, priority, retraction cascade.
- `source-provenance`: required `source` fields on each object kind; syntheses carry `source` in place of `produced-by`.
- `claim-context`: `context` and `context.scope` presence rules and defaults.
- `synthesis-rules`: cross-particular inputs and the `None identified` convention for `unresolved`.

### Modified Capabilities
<!-- none: openspec/specs/ is empty; this change establishes the first specs -->

## Impact

- `README.md` — every section from "Core Object Types" through "Design Principles" is touched; "MCP Server Tools" gains the renamed `synthesis_create` parameter and a note on `conflict_detect` semantics; "File Layout" gains `/merges/` and `dkf.yaml`.
- GitHub issues #1–#10 — each is resolved (or explicitly answered) by the spec text; they should be closed with a pointer to the relevant section once merged.
- `particulars-cli` reference implementation — will need to follow: `produced-by` → `source` on syntheses, `mrg_` records, `None identified`, and the relaxed `source.author` requirement. No other implementations exist.
- No code in this repository; no dependencies.
