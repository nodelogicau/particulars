## 1. The evidential

- [x] 1.1 Add `evidential` to the `DCLAIM` example in README.md and document the three values as answers to what would settle the claim
- [x] 1.2 State that it is required with no default, and that writers must not choose a value for the caller
- [x] 1.3 State the reader rule: absence is accepted and reported as `undeclared`, which is not a value, not equivalent to `observed`, and not inferrable from any other field
- [x] 1.4 Note that `held` is not strictly an evidential — languages mark sources of information, not opinions — so the axis is "what backs this"
- [x] 1.5 Add `evidential` to the canonical field order for claims

## 2. Confidence

- [x] 2.1 Define `confidence` in README.md for the first time, as the inverse probability that the claim is mistaken
- [x] 2.2 State that a `held` claim carries no confidence, and name the condition `confidence_on_held`
- [x] 2.3 State that no field records strength of conviction, and that it belongs in `content` if it matters
- [x] 2.4 State that confidence on an undeclared claim is reported as unverified rather than rejected

## 3. Syntheses

- [x] 3.1 State in the `DSYNTHESIS` section that a synthesis is inferred by construction and declares no evidential
- [x] 3.2 Document the `method` vocabulary — `reconciliation`, `qualification`, `positions` — replacing the undefined free string
- [x] 3.3 Note that `positions` is how `unresolved` says a question is not one evidence closes
- [x] 3.4 Note that marking a claim `held` does not exempt it from reconciliation; it changes what the synthesis does

## 4. Consistency

- [x] 4.1 Reword the `synthesis-rules` requirement "A synthesis's subject is explicit and never inferred" to remove the collision with `evidential: inferred`
- [x] 4.2 Review the "Backward compatibility by design" principle, which claims adoption does not require full implementation, against a field now mandatory on every claim
- [x] 4.3 Update the `claim_assert` row in the tool table to include the evidential
- [x] 4.4 Update Status: record the v0.1-versus-v0.2 question this change forces

## 5. Review and close out

- [x] 5.1 Verify each scenario in `specs/` is answered by a normative sentence in README.md
- [x] 5.2 Confirm no delta modifies a requirement that does not exist in the baseline — in particular, retraction `kind` belongs to the unapplied `verifiable-provenance` change
- [x] 5.3 Raise separately, not here: `kind: provenance-failure` has no referent on a claim carrying no `source.document`, whatever its evidential. It is a `retraction` constraint, unrelated to this change
- [x] 5.4 v0.1-versus-v0.2 settled: folded in before v0.1, recorded in Status
- [ ] 5.5 Raise with the reference implementation before applying — this requires a new argument on `claim assert`, a new validation error, and a rewrite of the confidence guidance in its agent skill
