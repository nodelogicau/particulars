## 1. Structured document references

- [x] 1.1 Extend the Source subsection in README.md with the structured `document` form (`uri`, optional `hash`, optional `quote`) alongside the existing string, stating that both are valid
- [x] 1.2 State that the locator is a verbatim quote and give the reason offsets are excluded — insertion elsewhere moves an offset without changing what it points at
- [x] 1.3 Note that a quote lets a reviewer audit a claim against its source in a pull request with no tooling
- [x] 1.4 Add `document` to the canonical field order for the structured form, so serialisation stays deterministic

## 2. Drift

- [x] 2.1 Define the three drift states — none, context drift, quote drift — as a table in the Source subsection or a short subsection beneath it
- [x] 2.2 Give the worked example that motivates context drift ("In staging" → "In production" leaving the quote untouched)
- [x] 2.3 State that drift is a condition for a reader to resolve and never a validation failure
- [x] 2.4 State that verification is best-effort: unfetchable, unhashable and undocumented sources stay fully valid and are reported as unverified

## 3. Retraction kind

- [x] 3.1 Add optional `kind` to the `retracted` block example and field list in the Retraction subsection
- [x] 3.2 Document the three values as the three joints in `claim → source → world`, not as a taxonomy
- [x] 3.3 State that `kind` is declared and MUST NOT be inferred from `superseded-by`, which answers a different question
- [x] 3.4 Document the cross-check: a `supersession` against an unchanged document hash warns, and an unverifiable source leaves the kind standing

## 4. Harness attribution

- [x] 4.1 Rewrite the Harness attribution paragraph under Trust and Provenance to say what the assessment is computed from — `defect` counts against a harness, `supersession` does not, `provenance-failure` counts against the document
- [x] 4.2 Note that claims sharing a document with a `provenance-failure` retraction are candidates for review

## 5. Disclosure

- [x] 5.1 State in the Source subsection that a `quote` reproduces source text verbatim inside the claim file, so the claim's effective scope governs that text's exposure
- [x] 5.2 Recommend the same treatment as `scope_wider_than_inputs` — warn, do not forbid — and note that a quote discloses completely where a synthesis summarises

## 6. Review and close out

- [x] 6.1 Verify each scenario in `specs/` is answered by a normative sentence in README.md
- [x] 6.2 Confirm both MODIFIED requirement headers still match their baselines exactly so archiving merges rather than duplicates
- [x] 6.3 Read the Source and Retraction subsections end to end for consistency with the canonical field order and with effective scope
- [ ] 6.4 Raise the change with the reference implementation before applying — it originates from a design review rather than reported feedback, and `validate` would gain two optional network-dependent checks
- [x] 6.5 Resolve the normalisation question from design.md, or record it in Status as open, before v0.1 is declared
