## Context

`verifiable-provenance` was applied on 2026-08-25 and raised with the reference implementation afterwards rather than before — the first round in this project to take that order, and it cost the implementation a review of something already merged. The review found one requirement it would not ship, and the objection is right.

This change is therefore small and mostly subtractive. It matters more for what it says about where a check may sit than for the text it moves.

## Goals / Non-Goals

**Goals:**
- Remove a check that fires on the ordinary case.
- Replace it with the version of the same instinct that is sound.
- Close the normalisation question with an answer rather than another deferral.
- Rename a field while renaming is still free.

**Non-Goals:**
- Distinguishing living documents from dated ones. See Open Questions — this is what would make the removed check possible, and it is a larger idea than this correction.
- Any change to the drift states, the quote-as-locator rule, or the three retraction kinds.
- The two `claim-evidential` improvements from the same review.

## Decisions

### D1. The cross-check was a category error, not a calibration problem

The three retraction kinds are the three joints in the chain a claim depends on:

```
   claim ─────────▶ source ─────────▶ world
     │                 │                │
  defect      provenance-failure   supersession
     │                 │                │
     └── drift is a signal about ───────┘
              THIS joint only
```

Drift tells you whether the source moved. `supersession` asserts that the *world* moved. Comparing them is only meaningful when the document is a living description of current state, and the format has no way to say which documents those are. So the check does not need tightening or a lower severity — it has no basis at all.

The failure is worth recording because the design doc justified it by analogy: "declared value, mechanical cross-check — the same division of labour used for conflict detection." The analogy broke because in every other case in this format the tool and the declaration are about the same thing. `scope_wider_than_inputs` compares scope against scope. `conflict_detect` computes over the same graph the synthesis claims to reconcile. Here the tool was measuring one joint and the declaration was about another.

*Empirically:* both this repository and the reference implementation's workspace cite commit-pinned blob URLs for most claims written in the last week. Those documents can never drift. Every honest supersession against one would have warned in perpetuity.

### D2. The sound check runs the other way

A `defect` says the claim misread its source. If the document has since drifted, the text the author is said to have misread is no longer the text a reviewer can read — so the declaration cannot be checked, and saying so is useful.

```
declared kind   document drifted?   what an implementation can say
──────────────────────────────────────────────────────────────────
defect          no                  the claim can be checked against the source
defect          yes                 unverifiable — the misread text is gone
supersession    either              nothing; drift says nothing about the world
provenance-fail either              nothing; requires judging the source itself
```

This is a fact about what is checkable rather than an inference about intent, which is the distinction that separates every warning this format keeps from the one it is removing.

### D3. Normalise CRLF to LF, and nothing else

The previous round recorded this as open and asked the implementation for a view, on the grounds that they would hit it first. Their answer, adopted here: normalise what is an artefact of the transport, leave what is an edit.

Line endings differ systematically by platform, so hashing raw bytes means a Windows checkout reports drift on every claim in a workspace — the cries-wolf failure arriving through a back door. Trailing whitespace, by contrast, differs because somebody edited the file; normalising it would blind the check to a class of real change. Every additional normalisation buys tolerance at the cost of sight, and the line-ending case is the only one where the difference is not an edit at all.

It belongs in the definition of the hash rather than in a label or a companion field. A label would mean two hashes for one document and every reader trying both.

### D4. `ref`, not `uri`

The mapping form requires `uri`, but the reference an agent usually has is a repository-relative path — which is not a URI, and is also the case where verification is free, since hashing a local file needs no network and git already knows what changed. Refusing relative paths would push agents back to bare strings, which is worse provenance than the mapping exists to provide; accepting them under a field called `uri` would make the field's name a lie.

`ref` holds either. `uri` keeps meaning a URI everywhere else in the format, which is what `DPARTICULAR` needs it to go on meaning.

This is only free because the mapping shipped yesterday and no implementation has written one. That is the whole argument for doing it now rather than documenting an exception forever.

## Risks / Trade-offs

- [Renaming a field that has already shipped in a specification] → Free in practice today and not next month. The reference implementation has not yet written a mapping and has said so on the issue; there is no second implementation.
- [Pinning LF is a break for anyone already hashing raw bytes] → Nobody is. It is stated as breaking because it would be, and because a silent change to what a hash covers is the worst kind.
- [Removing a check leaves a declared `kind` unvalidated in most cases] → Correct and intended. `kind` was always a declaration; the previous round overstated how much of it could be mechanically confirmed, and D2 keeps the part that can.
- [Reporting drift alongside a declared kind still risks noise] → It is reported as fact rather than as suspicion, and the reader decides. That is the same treatment `scope_wider_than_inputs` gets, which the implementation has already shipped and found workable.

## Open Questions

- **Should the format distinguish a living document from a dated one?** This is what would make the removed check sound: against a document that promises to describe current state, an unchanged hash really is evidence that nothing moved. It might be as small as a flag on the reference, or it might be recognising that a commit-pinned URL is self-evidently dated. It is a genuine idea rather than a loose end, and it is deliberately not attempted here — this change exists to remove an unsound rule, not to make it sound.
- **Should `hash` say which algorithms a consumer must understand?** Unchanged from the previous round, where it was noted and not settled.
