## 1. Sharding section (README)

- [x] 1.1 Where the README introduces sealed months, state the complete list of permitted modifications to a sealed-month file: append `retracted`; add or extend `redacted` (`dkf/0.3`); update a particular's `label` or `aliases`. Say that none of them changes an index entry, segment or `count`.
- [x] 1.2 Rewrite the git-benefit sentence ("an old month's tree object is rewritten only by a late merge or by a retraction…") to name all four: late merge, retraction, redaction, particular update.

## 2. Retraction and particulars (README)

- [x] 2.1 In the Retraction rules, scope "exactly two permitted modifications" to claims, syntheses, merge records and promotion records, and say that particulars are updated by `particular_define` instead.
- [x] 2.2 Next to the particular object example, state that `label` and `aliases` may be updated by `particular_define`, and that `id`, `type` and `uri` never change.
- [x] 2.3 Check the `ref`/`uri` legacy-alias paragraph ("appending a retraction is the only permitted modification") and reword it so it stays true with redaction. The point that such a file is never rewritten still holds, because redaction never renames a field.

## 3. Semantic cache (README)

- [x] 3.1 Replace "Objects are immutable apart from retraction, so a vector never needs recomputing" with the rule from `recall-query`: claim and synthesis vectors never need recomputing; a particular's label and alias vectors are checked against recorded text or a hash, are never consulted once stale, and are recomputed or deleted at the next update.
- [x] 3.2 Correct "Only `content` is embedded", which concerns redaction, to "Of the redactable fields, only `content` is embedded".
- [x] 3.3 State that the incremental update must reread particulars, because the index does not show a label or alias change.

## 4. Status and errata

- [x] 4.1 Add a v0.2 erratum to the README Status section. It says that the sealed-month rule named only retraction, while `particular_define` already updated particulars in place, and that this change corrects the text without changing the format (#51).
- [ ] 4.2 After merge, add an "Errata" line to the GitHub v0.2 release notes linking to the Status section.

## 5. Verification

- [x] 5.1 Grep README and `openspec/specs` for "only permitted modification", "single modification", "immutable apart from" and "rewritten only by", and confirm none remains in its old form.
- [x] 5.2 Confirm `2026-09-05T01:01:35Z` appears nowhere, and that the corrected instant of `clm_01a0f3c1-4d20-…` agrees with its first 48 bits.
- [x] 5.3 `openspec validate fix-sealed-month-mutations --strict` passes.
