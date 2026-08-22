## Why

Four issues opened against the spec on 2026-08-22 ([#11](https://github.com/nodelogicau/particulars/issues/11)–[#14](https://github.com/nodelogicau/particulars/issues/14)) each identify a place where the resolved v0.1 text is self-contradictory or incomplete, found while `particulars-cli` grew from a CLI into an MCP server and a Microsoft Graph export. Two are contradictions the last round introduced (`synthesis_create` lost its subject when cross-particular inputs were blessed; scope promotion became impossible when claims became immutable), and one — canonical field order — blocks the signing story that v0.1 still owes. They are folded into one change because #11 must settle before #14 can define a new record's serialisation, and #13 and #14 edit the same tool table.

## What Changes

All changes are to the specification text in `README.md` and the baseline specs under `openspec/specs/`.

- **Canonical field order** (#11): the README's per-type field order becomes the canonical writing order — writers SHOULD emit it, readers MUST accept any order, extension fields go last. The `merge-records` prose is corrected to match the README example (`id, type, uris, reason, source, timestamp`), which mirrors `DCLAIM`'s payload-before-`source` shape and is what the reference implementation already writes. The undefined term "canonical object" in the signing paragraph is given a referent, and the writer-SHOULD is noted as becoming a MUST when signing is specified.
- **`.dkf` pointer file** (#12): an optional discovery convention for tools that start *above* a workspace (the `knowledge/` subdirectory case, an agent session at a repository root). First non-blank, non-comment line names the workspace root; `dkf.yaml` wins at the same level; pointers do not chain; a pointer to a directory without `dkf.yaml` is an error naming both paths. The pointer is not a workspace marker and carries no configuration. Discovery precedence — explicit configuration, then walk-up — is stated for the first time.
- **`synthesis_create` takes a subject** (#13): the signature becomes `synthesis_create(particular_id, content, inputs[], unresolved, source)`, accepting an id, URI, label, or alias as `claim_assert` does. Implementations MUST NOT infer a synthesis's subject from its inputs, which the cross-particular-inputs rule makes unsafe. A requirement that every claim and synthesis carries exactly one explicit `subject` is added.
- **Scope promotion becomes a record** (#14): `knowledge_publish` writes `publishes/pub_<uuidv7>.yaml` naming the promoted claims, the target scope, `source`, `timestamp`, and an optional `reason`. A claim's **effective scope** is the widest non-retracted promotion covering it, defaulting to its own `context.scope`. **Promotion may only widen, never narrow** — narrowing is retraction — so a naive consumer reading only the claim file under-shares rather than leaks. **Promotion does not cascade to a synthesis's inputs.** Promotion records are retractable, are indexed, and are ignored by conflict detection. **BREAKING** for implementations: a third record type and a new id prefix.
- **`knowledge_publish` records its source** (#14, found while specifying it): the signature becomes `knowledge_publish(claim_ids[], scope, source, reason?)`. It currently cannot record the source that "Promotion to `public` is an explicit act recorded with a source" requires of it.
- **`pub` joins the id grammar** (#14): prefixes become `par|clm|syn|mrg|pub` for both minting and the lenient read regex.

## Capabilities

### New Capabilities
- `scope-promotion`: the publish record, effective-scope computation, the widen-only and no-cascade rules, retraction of a promotion, and what promotion cannot undo.
- `canonical-serialisation`: canonical field order per object type, the writer/reader asymmetry, placement of extension fields, and the relationship to the reserved signature payload.

### Modified Capabilities
- `merge-records`: field order in the storage requirement corrected to match the README example.
- `workspace-config`: discovery gains the `.dkf` pointer and an explicit precedence rule.
- `synthesis-rules`: a synthesis's `subject` is explicit and MUST NOT be inferred from inputs.
- `object-identifiers`: `pub` added to the minted prefixes and the lenient read regex.
- `index-manifest`: publish records get index entries with their claims and target scope.
- `conflict-semantics`: publish records are not knowledge and do not affect `current` / `unsynthesised` / `stale`.
- `claim-context`: `context.scope` is the claim's *asserted* scope; effective scope is asserted scope widened by promotion records, and is still never taken from configuration.

## Impact

- `README.md` — Core Object Types gains a canonical-order note and a publish-record subsection; File Layout gains `/publishes/` and `.dkf`; the MCP tool table changes two signatures; Trust and Provenance gains effective scope and a defined "canonical object"; Scope isolation is rewritten.
- `openspec/specs/` — two new capabilities, seven modified.
- Issues #11–#14 — each resolved by spec text; close with a pointer to the resolving section.
- `particulars-cli` (v0.5.0) — needs `pub_` records, effective-scope filtering in its feed and Graph export, `particular_id` on the MCP `synthesis_create`, and `source` on `knowledge_publish`. Its `.dkf` support (v0.3.0) and merge field order already match. Its 38-claim `personal` workspace becomes publishable without re-assertion, which is the concrete motivation for #14.
- No code in this repository; no dependencies.
