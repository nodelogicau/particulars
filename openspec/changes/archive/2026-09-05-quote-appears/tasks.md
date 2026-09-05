## 1. The rule, in the README

- [x] 1.1 In *Drift*, after the two-signal paragraph, define *appears*: fold every run of Unicode `White_Space` to one space on both sides, trim the quote, substring; case, punctuation, and Unicode form verbatim; the stored quote never folded. Say in one sentence why whitespace is where the two signals part — the hash asks whether anything changed, the quote whether the words are still there — and that for everything else the two agree about what an edit is
- [x] 1.2 Extend the drift table to the full set of states: the three existing rows; *absent / matches* as quote drift with the never-matched wording; *present / none* as no drift with the hash unverified; *absent / none* as quote drift without the inference. Keep "The middle row is why…" pointing at the right row
- [x] 1.3 State the format-blind limit beside the rule: folding removes no `>`, `//`, or other continuation-line prefix, so a quote across such a wrap is taken from within one line
- [x] 1.4 In the `quote` paragraph of the structured-reference section, add that a writer refuses a quote folding to nothing and a reader treats one as no quote, with a warning, because the file cannot be rewritten
- [x] 1.5 Reread "A quote is content-addressed, so it survives insertion and reformatting" and confirm it is now true as written; adjust only if the new paragraph makes it redundant

## 2. Close out

- [x] 2.1 Verify each scenario in `specs/source-verification/spec.md` is answered by a normative sentence in README.md, including the NBSP, block-scalar, blockquote, and empty-quote scenarios
- [x] 2.2 Confirm both MODIFIED blocks copy their baseline requirement text in full, with every pre-existing scenario retained
- [x] 2.3 Commented on and closed #24 (2026-09-05, landed as 48611fd): accepted; the whitespace set is the `White_Space` property and why; "agrees with the hash" scoped to non-whitespace; the no-hash states named; the empty quote refused on write and read as no quote, and why not invalid; paragraph breaks fold; format-blind stated
- [x] 2.4 Filed as particulars-cli#10: name the property rather than listing whitespace kinds in its delta spec and docs; read a quote that folds to nothing as no quote with a warning rather than reporting `quote_drift`; refuse it at `claim assert` and `claim_assert`
- [x] 2.5 Recorded in particulars-knowledge#38: acceptance claim clm_01a07138-4619-7a06-8c3a-ce9790912425 and qualification synthesis syn_01a07138-4691-7d84-b58f-b6231fd9d752 over the #24 claim and the 2026-08-25 two-signal drift claim
