## 1. The evidential

- [ ] 1.1 Add `evidential` to the `DCLAIM` example in README.md and document the three values as answers to what would settle the claim
- [ ] 1.2 State that it is required with no default, and that writers must not choose a value for the caller
- [ ] 1.3 State the reader rule: absence is accepted and reported as `undeclared`, which is not a value, not equivalent to `observed`, and not inferrable from any other field
- [ ] 1.4 Note that `held` is not strictly an evidential — languages mark sources of information, not opinions — so the axis is "what backs this"
- [ ] 1.5 Add `evidential` to the canonical field order for claims

## 2. Confidence

- [ ] 2.1 Define `confidence` in README.md for the first time, as the inverse probability that the claim is mistaken
- [ ] 2.2 State that a `held` claim carries no confidence, and name the condition `confidence_on_held`
- [ ] 2.3 State that no field records strength of conviction, and that it belongs in `content` if it matters
- [ ] 2.4 State that confidence on an undeclared claim is reported as unverified rather than rejected

## 3. Syntheses

- [ ] 3.1 State in the `DSYNTHESIS` section that a synthesis is inferred by construction and declares no evidential
- [ ] 3.2 Document the `method` vocabulary — `reconciliation`, `qualification`, `positions` — replacing the undefined free string
- [ ] 3.3 Note that `positions` is how `unresolved` says a question is not one evidence closes
- [ ] 3.4 Note that marking a claim `held` does not exempt it from reconciliation; it changes what the synthesis does

## 4. Consistency

- [ ] 4.1 Reword the `synthesis-rules` requirement "A synthesis's subject is explicit and never inferred" to remove the collision with `evidential: inferred`
- [ ] 4.2 Review the "Backward compatibility by design" principle, which claims adoption does not require full implementation, against a field now mandatory on every claim
- [ ] 4.3 Update the `claim_assert` row in the tool table to include the evidential
- [ ] 4.4 Update Status: record the v0.1-versus-v0.2 question this change forces

## 5. Review and close out

- [ ] 5.1 Verify each scenario in `specs/` is answered by a normative sentence in README.md
- [ ] 5.2 Confirm no delta modifies a requirement that does not exist in the baseline — in particular, retraction `kind` belongs to the unapplied `verifiable-provenance` change
- [ ] 5.3 Raise separately, not here: `kind: provenance-failure` has no referent on a claim carrying no `source.document`, whatever its evidential. It is a `retraction` constraint, unrelated to this change
- [ ] 5.4 Settle the v0.1-versus-v0.2 question, the only one left open in design.md
- [ ] 5.5 Raise with the reference implementation before applying — this requires a new argument on `claim assert`, a new validation error, and a rewrite of the confidence guidance in its agent skill
