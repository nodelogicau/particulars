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

### D4. `ref`, not `uri`, and it holds three things rather than two

The mapping form requires `uri`, but the reference an agent usually has is a repository-relative path — which is not a URI, and is also the case where verification is free, since hashing a local file needs no network and git already knows what changed.

The review surfaced a third case that settles the argument. Roughly 7% of the reference implementation's corpus cites a conversation or an assistant session: sources the specification already calls legitimate, and which a bare string was the only way to record. But **an unfetchable source can still carry a quote** — quoting what someone said in a meeting, with nothing to fetch and no hash, is a good use of the mapping and produces provenance a reviewer can weigh. Under `uri` that means writing `chat session 2026-08-22` into a field called `uri`.

So `ref` is not a tidier name for the same thing; it is the only one of the two that can hold what a third of this specification's own examples describe. Resolution is best-effort, in keeping with the rest of verification: an implementation MAY try to resolve a `ref` as a URI or as a workspace-relative path, and where it resolves as neither the reference is simply unverifiable — a state the format already has.

`uri` keeps meaning a URI everywhere else, which is what `DPARTICULAR` needs it to go on meaning.

*On cost:* this was written as free on the argument that no implementation had written a mapping. That was very nearly true and is no longer exactly true — the reference implementation released `uri` a day before this change. It remains cheap, and the mitigation is the pattern the format already uses for `produced-by`: write `ref`, accept `uri` on read, warn. The warning earns its place here for a reason specific to this format rather than out of tidiness — a file carrying `uri` **can never be rewritten**, since appending a retraction is the only permitted modification, so readers must accept it in perpetuity and a warning is the only way anyone learns it is there.

### D5. Writers converge on sha256; readers stay open and honest about it

The previous round left the algorithm question open. Left open, it permits two conformant implementations that cannot check each other's hashes, which defeats the point of recording one.

Writers SHOULD write `sha256`. Readers SHALL accept any `<algorithm>:<digest>` and SHALL report an unrecognised algorithm as **unverified** rather than invalid. Convergence where it matters for interoperability, agility where it costs nothing, and the failure mode is the one this change is otherwise built on: an honest "cannot check" instead of a confident wrong answer.

### D6. Verification covers retracted objects

The unverifiable-defect finding is *about* a retraction, so it can only be produced by examining the document of an object that has been retracted. That inverts a natural assumption — the reference implementation's verification loop skips retracted objects on the reasonable grounds that a withdrawn claim's provenance is nobody's problem, and other implementations are likely to have reached the same place independently. The specification states it rather than leaving each one to discover it.

## Risks / Trade-offs

- [Renaming a field that has already shipped in a specification] → Free in practice today and not next month. The reference implementation has not yet written a mapping and has said so on the issue; there is no second implementation.
- [Pinning LF is a break for anyone already hashing raw bytes] → Nobody is. It is stated as breaking because it would be, and because a silent change to what a hash covers is the worst kind.
- [Removing a check leaves a declared `kind` unvalidated in most cases] → Correct and intended. `kind` was always a declaration; the previous round overstated how much of it could be mechanically confirmed, and D2 keeps the part that can.
- [Reporting drift alongside a declared kind still risks noise] → It is reported as fact rather than as suspicion, and the reader decides. That is the same treatment `scope_wider_than_inputs` gets, which the implementation has already shipped and found workable.

## Open Questions

*Both questions the previous round left open are now closed.* The algorithm question is answered by D5.

**Should the format distinguish a living document from a dated one?** Asked as the residue of the removed check, and answered **no**, on evidence from the reference implementation rather than from first principles.

Two findings, and the second is the decisive one. Classifying 76 real documents, a hand-written heuristic matching commit-pinned and release-tagged URLs misclassified about a fifth of them on the first pass, missing tag-pinned blobs and bare commit URLs — written by someone who knew the corpus. "A commit-pinned URL is self-evidently dated" is self-evident to a person and fiddly to a matcher, and a matcher quietly wrong about datedness would make the check wrong in a new way rather than sound.

More importantly, the distinction does not rescue the check even where the classification is right. Against a genuinely living document — a vendor's documentation page — the ordinary way a documented fact goes stale is that **reality moves and the documentation lags**. The world has moved, the claim is genuinely superseded, and the page has not changed yet: unchanged hash, honest supersession, and the check misfires exactly as it does against a dated document. When it *would* fire correctly, what it has detected is that the source is now wrong, which is what `provenance-failure` already says.

So the flag would buy a check that is still wrong most of the time, at the cost of a field on every reference that agents must judge and reviewers must audit. Not attempted, and if a use for the distinction appears later it will not be this one.
