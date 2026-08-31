## 1. The tolerance, restated

- [x] 1.1 Rewrite the tolerance paragraph in the `index.yaml` section of README.md: the check exists to catch the index lagging changes; a presence difference in a field mirroring an immutable property is not drift, in either direction; `retracted` mirrors the only mutable property and is compared as present, absent meaning `false`; differing values and missing or extra entries are drift
- [x] 1.2 List the MAY fields with their classification once, so the next field classifies itself, and say why the criterion is immutability rather than "absence carries a value"

## 2. Rebuild preserves fields

- [x] 2.1 Widen the "MUST preserve entries whose type it does not recognise" sentence to cover fields it does not recognise on entries it regenerates, with the same reasoning as #16 and the note that the stakes are speed, not truth

## 3. Close out

- [x] 3.1 Verify each scenario in `specs/` is answered by a normative sentence in README.md
- [x] 3.2 Confirm both MODIFIED blocks copy their baseline text in full
- [ ] 3.3 Comment on and close #22 when archived
- [ ] 3.4 Add to `particulars-cli#7`: the masking form of the check and unknown-field preservation on rebuild
- [ ] 3.5 Record in the dogfood workspace
