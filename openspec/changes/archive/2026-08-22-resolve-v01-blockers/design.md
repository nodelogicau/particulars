## Context

The 2026-08-21 change (`address-reference-impl-feedback`, archived) resolved the first ten pieces of reference-implementation feedback and produced the ten baseline specs under `openspec/specs/`. `particulars-cli` then implemented all of it in v0.2.0 and kept going — v0.3.0 added workspace pointers, v0.4.x an MCP server, v0.5.0 a Microsoft Graph export. Building those surfaced four more problems, filed as #11–#14.

Two of the four are contradictions the last change introduced, which is worth stating plainly because it shapes how much benefit of the doubt the current text gets:

- **#13** — blessing cross-particular synthesis inputs (issue #10.3) made a synthesis's subject underivable, but the tool signature was not updated to supply it.
- **#14** — making claims immutable (#2) and forbidding readers from inferring scope (#10.2) removed every mechanism by which `knowledge_publish` could do what the tool table says it does.

The constraints from the previous design still hold and are used to adjudicate below: the README's design principles are load-bearing; git is the storage layer; readers lenient, writers strict; and breaking the draft is cheap now and expensive after a second implementation appears. One constraint is newer: there is now a **live workspace of real knowledge** (38 claims, all `personal`) whose owner cannot publish it, so #14 is not hypothetical.

## Goals / Non-Goals

**Goals:**
- Remove both self-contradictions so that the spec text is implementable as written.
- Give "canonical object" a referent, unblocking a future signing specification.
- Define scope promotion in a way that cannot turn a naive consumer into a leak.
- Keep the record count honest: say "three knowledge objects plus records" rather than pretending the core is still three files.

**Non-Goals:**
- Specifying signing itself (canonicalisation is a prerequisite, not the deliverable).
- The `.well-known` crawling protocol beyond what effective scope requires.
- A JSON Schema or formal grammar.
- Access control, encryption, or revocation of already-fetched public data — out of scope by construction (see D4).
- Updating `particulars-cli`.

## Decisions

### D1. Canonical field order is writer-SHOULD, reader-MUST-accept (#11)

The order shown for each type in the README is the canonical order. Writers SHOULD emit exactly it; readers MUST accept any order; fields an implementation adds beyond the specification go after all specified fields, preserving their relative order.

The `merge-records` prose is corrected to the README example's order — `id, type, uris, reason, source, timestamp` — rather than the example being corrected to the prose. Three reasons: it mirrors `DCLAIM`, where the payload field (`content`) precedes `source`, and `reason` is a merge's payload; a concrete artifact is less ambiguous than a sentence, so it is the better source of truth to standardise on; and the reference implementation already writes it, so the fix costs nobody a migration.

*Why not simply "field order is not normative":* the spec already depends on canonicalisation without admitting it. [Trust and Provenance](../../../README.md#trust-and-provenance) defines the signed payload as "the **canonical** object minus `retracted` and `signature`" — a term with no referent in the document. Two writers disagreeing on order produce different bytes for the same object and therefore different signatures. Order must be pinned before signing can be written, and this is the cheapest moment to pin it.

*Why not writer-MUST:* it would make a conformant writer impossible in languages whose default YAML emitters sort keys, for no benefit that SHOULD does not already deliver in the git-review workflow. When signing is specified, the signed payload's order becomes a MUST *for signing*, which is where determinism is actually load-bearing. Stated as such so implementers can see it coming.

### D2. `.dkf` is blessed as an additive discovery convention (#12)

At each ancestor directory, in order: a `dkf.yaml` makes that directory the workspace; otherwise a `.dkf` file redirects to the path named on its first non-blank, non-comment line, resolved relative to the pointer's directory or taken as absolute. Pointers do not chain — the target MUST contain `dkf.yaml`, and a target that does not is an error naming both paths. The pointer is not a workspace marker: it carries no configuration, is not a `dkf.yaml`, and a workspace MUST remain discoverable from inside it without one.

The issue's argument for a separate filename over a `root:` key in a root `dkf.yaml` is correct and worth preserving in the spec: that file *is* the workspace marker to every conformant reader, so a redirect written that way makes the repository root look like an empty workspace.

Discovery precedence is stated for the first time: explicit configuration (a `--workspace`-style argument, then an environment variable) wins over discovery entirely. The spec has never acknowledged that tools offer an override, which left the interaction with discovery undefined.

*Alternatives:* searching *downward* for a `dkf.yaml` (ambiguous with multiple workspaces, slow on large trees, and silently picks a workspace the user did not name); blessing the directory name `knowledge/` (magic, and fails the moment anyone renames it); saying only that tools MAY offer "equivalent redirection" (invites every implementation to invent its own filename, which is the outcome the issue is trying to prevent).

### D3. Scope promotion is a record, and may only widen (#14)

`knowledge_publish` writes:

```yaml
# publishes/pub_019196a5-…yaml
id: pub_019196a5-8b4c-7def-8abc-0123456789ab
type: publish
claims:
  - clm_01916f03-b680-71a3-974f-9401ba374e1f
  - syn_01933034-b1a0-705f-b788-2c7c58c46e29
scope: public
reason: Architecture history cleared for the public docs site.   # optional
source: {author: ben, harness: claude}
timestamp: 2026-08-22T09:30:00Z
```

A claim's **effective scope** is the widest non-retracted promotion naming it, or its own `context.scope` if none does, where `personal < organisation < public`. Feed eligibility reads the claim file plus the promotion records — never configuration, which is the property `claim-context` was protecting.

**Promotion may only widen.** A record naming a scope narrower than a claim's asserted scope is invalid. This is the decision that makes the design safe rather than merely expressive: with widen-only, a naive consumer that reads a claim file and honours `context.scope` refuses to publish something that was in fact authorised — it under-shares. If narrowing were expressible, the same naive consumer would read `public` on a file that had since been restricted and leak it. Under-sharing is a bug report; leaking is a breach. Narrowing is expressed by retracting the promotion (or the claim), which a naive consumer *does* see, because `retracted` is on the file it already opens.

**Promotion does not cascade.** Promoting a synthesis does not promote its inputs. A public consumer may therefore receive a synthesis citing input ids it cannot resolve, and that is the correct default: cascading would silently widen an entire lineage — exactly the "explicit and deliberate, not a default" property the tool table demands. Publishers wanting a traversable public chain promote the inputs too, and tooling SHOULD warn when a promoted synthesis has unpromoted inputs.

*Why a record rather than rewriting `context.scope`:* rewriting contradicts "adding a `retracted` block is the only permitted modification to an existing object file", which is the rule the whole provenance story rests on.

*Why a record rather than re-asserting at the wider scope:* a new claim has a new id, so existing syntheses, `superseded-by` pointers, and merge records still cite the narrower original. The lineage splits, which is the failure the format exists to prevent.

*Why a record rather than a feed-level allowlist* (a list of served ids in `.well-known` or a `feeds.yaml`): an allowlist is configuration, not provenance — no author, no timestamp, no retraction trail — and the README already promises that "promotion to `public` is an explicit act recorded with a source". A record is what that sentence describes.

*Why not option 2 from the issue* (scope fixed at assertion; `knowledge_publish` merely selects among already-`public` claims): it is cheaper and internally consistent, but it makes `defaults.scope: personal` — the spec's own default — a one-way door, and it contradicts the promotion language already in the tool table and in Scope isolation. If it were chosen, the spec would have to warn that scope is irrevocable at assertion and that tools SHOULD force an explicit scope on every write, which is a worse experience than one extra record type.

### D4. What promotion cannot do

Retracting a promotion ends *future* feed eligibility. It cannot recall what a crawler already fetched, and the spec says so rather than implying otherwise. This is a property of publishing anything, not a deficiency of the record, but a format that stores knowledge for agents should not leave an implementer to discover it.

### D5. `synthesis_create` takes `particular_id` (#13)

`synthesis_create(particular_id, content, inputs[], unresolved, source)`, accepting an id, URI, label, or alias exactly as `claim_assert` and `particular_resolve` do. Implementations MUST NOT infer a synthesis's subject from its inputs: first-input, most-common-input, and all-inputs-agree each give the wrong answer for a synthesis about project X citing a claim about library Y, which `synthesis-rules` explicitly permits. A general requirement is added — every claim and synthesis carries exactly one `subject`, supplied explicitly — because the specs currently assert this nowhere, having inherited it from the README's examples.

### D6. Records are now three, and the id grammar grows

`pub` joins `par|clm|syn|mrg` for minting and in the lenient read regex. The "three knowledge objects plus two records" phrasing from the last change becomes "plus records (retraction, merge, publish)", worded so that a fourth record does not require re-litigating the sentence. Publish records are indexed (id, type, claims, scope) so a feed generator can filter without opening every record, and are ignored by conflict detection: unlike merges, they are not knowledge and form no equivalence class.

## Risks / Trade-offs

- [A third record type strains "minimal spec, layered implementation"] → The principle's actual content is that *entity types, ontologies, and trust hierarchies* are implementation concerns; records that make an existing promised operation possible are not the same kind of growth. Mitigated by wording the principle so records are an open, named list.
- [Effective scope means a claim file no longer tells the whole story] → Deliberate, and bounded by widen-only (D3): the file alone is always *safe*, just sometimes conservative. A consumer that ignores `/publishes/` never leaks.
- [#14 is a second breaking round for `particulars-cli` days after v0.2.0 shipped the first] → Real cost, but the alternative is leaving a live 38-claim workspace unpublishable. The change is additive at the file level (new directory, new prefix); no existing file changes shape.
- [Widen-only forbids a legitimate "I published this by mistake, narrow it"] → That is retraction of the promotion, which is expressible and visible. The lost case is narrowing an *asserted* scope, which was never possible anyway.
- [Canonical order as SHOULD will drift in practice] → Accepted for now; implementations that care can offer a canonical-form check, as the reference implementation does for the index. Signing will convert it to a MUST where it matters.
- [`.dkf` adds a second file tools must know about] → Optional, additive, and already shipped in the reference implementation; the alternative is each implementation inventing a different one.

## Open Questions

- Should a promotion be able to name a *particular* ("publish everything about X, including future claims") rather than an explicit claim list? Powerful and dangerous: it would widen objects that do not exist yet, which reads as a standing grant rather than an explicit act. Deferred; the record's `claims[]` is a list of ids only.
- Does a public feed serve a promoted synthesis's unresolvable input ids as opaque strings, or omit `inputs` entirely? Belongs with the `.well-known` crawling protocol, which remains unspecified.
- Whether the signed payload should be defined over the canonical YAML bytes or over a serialisation-independent form (e.g. canonical JSON). D1 only guarantees the former is well-defined; the choice belongs to the signing change.
