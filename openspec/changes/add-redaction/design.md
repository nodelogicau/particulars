## Context

Today an object file can change in exactly one way: a `retracted` block is appended to it (README *Retraction*; `retraction` spec). The format's principles say "nothing is overwritten" and "nothing is deleted". The index (`dkf/0.2`) depends on that immutability. Sealed segments are byte-immutable, and the only mutable property, retraction, is tracked through per-month `retracted` lists keyed by when the retraction happened.

Redaction needs a second, narrower exception. Its use cases are a true but sensitive claim, a quote that discloses too much, and a retraction reason that restates what it retracts. The maintainer has scoped this to hiding and hygiene: YAML stays readable, and access to history is a property of the implementation. A git workspace keeps history, and a database-backed implementation can restrict it.

## Goals / Non-Goals

**Goals:**
- Define a redaction that removes text from an object's current file and keeps the object's id, its place in the lineage graph, and a record of who redacted it, when, and why.
- Keep every sealed index segment byte-immutable.
- Ensure every consumer that understands the format treats a content-redacted object as gone, and that every consumer that doesn't understand it refuses the workspace rather than misreading it.
- State honestly what redaction does not do.

**Non-Goals:**
- Erasure from version history, clones, crawlers or caches already fetched (legal erasure).
- Encryption or crypto-shredding.
- Redacting particulars (labels, aliases, minted URIs), merge or promotion `reason`s, `topics`, or `document.author`.
- Deciding automatically whether one object's text restates another's.

## Decisions

### D1. A separate `redacted` block, not a retraction `kind`

Retraction and redaction answer different questions ("is it true?" and "should it be readable?"), so they combine freely. `kind` feeds harness and author reliability: a `defect` counts against the producer. Folding redaction into `kind` would either count a redaction against a harness that did nothing wrong, or need a fourth value. The retraction diagram argues there should be no fourth value, because there is no fourth joint.

*Alternative considered:* `kind: redaction` on a retraction. Rejected for the reliability reason, and because it would force every redaction to also be a retraction, which is wrong for evidence-only redaction.

### D2. The block lists what it removed

```yaml
redacted:
  timestamp: 2026-11-02T10:00:00Z
  reason: Third party's medical detail
  source: {author: ben}
  fields: [content, source.document.quote]
```

`fields` holds dotted paths from a closed set: `content`, `unresolved`, `source.document.ref`, `source.document.quote`, `source.document.hash`, `retracted.reason`. The set is closed because each field has a defined consequence (D3, D5). An open set would mean a validator could not tell a redacted field from a missing required one. A listed field SHALL be absent from the file. A required field that is listed is valid when absent, and that is the only way a required field may be missing.

A bare-string `document` is its `ref`. Redacting `source.document.ref` from a bare-string document removes `document` altogether. On a mapping, the other members stay, so `author` survives as an index-mirrored field must.

A file carries at most one `redacted` block. A later redaction of more fields replaces `timestamp`, `reason` and `source`, and takes the union of `fields`. *Alternative considered:* a list of blocks, which preserves each redaction's own record. Rejected for v1 because the common case is a single redaction, and a list makes canonical order and the index month ambiguous. Revisit if a real workspace needs two. (Open question 1.)

### D3. Redacting `content` withdraws the object, while evidence-only redaction does not

An object whose `content` is gone carries no belief, so it is treated exactly as a retracted object is: out of recall, never `current`, and making citers `stale`. **Withdrawn** names "retracted or content-redacted". The README defines it once, and conflict semantics, recall and author relations use it. Every existing "non-retracted" rule therefore reads as "non-withdrawn" through one definition, without each spec being edited.

Redacting `quote`, `ref` or `hash` leaves the assertion intact. The claim stays live and its evidence becomes unverifiable. This case is common: a quote reproduces its source verbatim and travels with promotion.

Redacting `unresolved` alone leaves a synthesis `current`-eligible. Its belief is its `content`.

### D4. Only fields the index does not mirror are redactable

Index entries mirror `subject`, `scope`, `topics`, `timestamp`, `author` and `document-author`, and sealed segments never change. Restricting redaction to unmirrored fields means no entry ever changes. Withdrawal is the only index-visible effect, and it is carried as tombstones.

*Cost:* `topics` such as `health` can be revealing, and `document.author` names the person reported from. Both are left for a later change, which would need entry masking.

### D5. A `redacted` list in the index, keyed by the redaction's month

The `redacted` list mirrors the `retracted` mechanism exactly: the root holds open-month and later redactions, sealed segments hold their own month's, and the same guard and validation apply. It holds **withdrawn-by-redaction ids only**, since evidence-only redactions change nothing the index mirrors. A separate list keeps "retracted" meaning "judged wrong". An object both retracted and content-redacted appears in both lists.

*Alternative considered:* reusing `retracted`. Rejected because it would make the index lie about why an object left recall, and `kind` statistics computed from the index would count redactions.

### D6. Irreversible and never inferred

The content is gone, so there is nothing to restore. As with retraction, reinstatement is a new object. The `redacted` block is never removed. No operation redacts as a side effect: publishing, retracting and merging never redact.

### D7. No cascade, and candidates are reported as `restates_redacted`

When X's `content` is redacted, three things may repeat it: syntheses citing X through `inputs`, inferred claims citing X through `basis`, and the `superseded-by` successor of X. They are already `stale` (except the successor). Staleness says "re-reason". `restates_redacted` says something different: "this text may contain what was removed; a person should look". It is a per-object finding, because the action, redacting it or not, happens at that object. It clears when the candidate is itself content-redacted or when a person records a decision. (Open question 2: how a "looked, it's fine" decision is recorded without mutating the candidate.)

The redaction `reason` must not restate what it removed. This is guidance only, since no tool can check it.

### D8. Signatures

The payload excludes `retracted`, `redacted` and `signature`. Once a covered field is removed, the original signature cannot verify. This is reported as the corpus fact `signature_redacted`, not as invalid, because nothing about the object is untrustworthy that the `redacted` block does not already say. Signature suites are still reserved, so the practical stakes are low.

### D9. `dkf/0.3`, and writers refuse to redact in older workspaces

A `dkf/0.2` reader meeting a claim with no `content` either rejects the workspace or recalls an empty belief. The second is a silent misread. Workspace-config already makes readers refuse a `format` they do not implement, so a version bump converts every misread into a refusal. `dkf/0.3` is `dkf/0.2` plus redaction. Migrating from `dkf/0.2` rewrites `format` only. No file moves and no payload changes, so every signature still verifies. A `dkf/0.1` workspace migrates to `dkf/0.2` first. A writer refuses `redact` in an older workspace and names the migration.

*Alternative considered:* no bump, with redaction as an additive field. Rejected because readers must ignore unknown fields, so an old reader would ignore `redacted` and trip on the missing `content`. That is exactly the misread the refusal rule exists to prevent.

### D10. What is promised, stated in the spec

Redaction removes text from the object's current file and from what a conformant implementation reads, recalls, serves and embeds. It makes no claim about history, clones, crawlers, or consumers who already fetched the object. A git-backed implementation SHALL say so in its output when it redacts. An implementation whose store controls access to prior versions MAY restrict them, and nothing in the format depends on whether it does.

## Risks / Trade-offs

- [The text stays in git history, and users may believe it is gone] → D10 makes the warning normative for git implementations, and the README says it plainly.
- [`topics` and `document.author` can still reveal sensitive content] → stated as out of scope. A later change can add entry masking.
- [Synthesis content may restate a redacted claim] → `restates_redacted` makes the candidates visible, and a person decides. Nothing cascades.
- [Readers that ignore `fields` mistake a redacted required field for a malformed file] → the `dkf/0.3` bump means such a reader refuses the workspace instead.
- [Redaction is a second exception to immutability, which weakens the "nothing is overwritten" story] → the exception is narrow (removal only, from a closed set, recorded in the file itself), and the Design Principles are restated to say exactly that, rather than keeping a slogan that is no longer literally true.
- [A reason that restates the redacted content] → guidance in the skill and conventions. Unverifiable.

## Migration Plan

1. Spec: README edits as listed in the proposal. Tag `dkf/0.3` when this change archives.
2. `particulars-cli`: implement `migrate --to dkf/0.3` (rewrite `format`), `redact`, the index list, `restates_redacted`, and the cache drop. Until it ships, nothing can write a redaction, so existing workspaces are unaffected.
3. Rollback: a `dkf/0.3` workspace with no `redacted` blocks can be set back to `dkf/0.2` by rewriting `format`. One with redactions cannot, because that is the point of the bump.

## Open Questions

All three were resolved on 2026-11-03 by the maintainer accepting the draft answers:

1. **One block or a list?** One `redacted` block per file, with `fields` taken as the union across redactions (D2). Revisit if a real workspace needs each redaction's own record.
2. **How does `restates_redacted` clear?** It is reported until the candidate is itself withdrawn. There is no dismissal record. This is noisy but honest, and a dismissal record can be added later as a new record type if the noise proves costly.
3. **Must content redaction follow a retraction?** No. Removing `content` already withdraws the object.
