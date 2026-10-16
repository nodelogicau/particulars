## 1. README

- [x] 1.1 In *Recall by query*, *The baseline*: terms are runs of non-whitespace; leading and trailing category P is trimmed from each term and from the whole query, interior characters kept, with `timeout?`, `PROJ-1234.` and `v1.2.3` as examples; empty terms are ignored; a query empty after trimming resolves nothing and is not an error
- [x] 1.2 In *The baseline*, state OR: a text matches when the trimmed whole query or any one trimmed term occurs in it, and an object so matched is marked matched; say why AND was rejected
- [x] 1.3 In *`resolution`*: exact means the label or alias occurs in the query with only punctuation around it, with `Project X?`, `"Project X"` and `C#?` matching, `C` not matching `C#`, and why trimming both sides was rejected
- [x] 1.4 In *`resolution`*: the fixed order within `label`, `alias` and `lexical` — whole query first, then distinct terms matched, then particular id — counted over the particular's response, not over objects the caller cannot see; `semantic` order is implementation-defined; `limit` keeps the first in this order
- [x] 1.5 Search the README for any sentence saying stage-one order does not reach the response or that ranking inside stage one is free, and correct it

## 2. Delta spec

- [x] 2.1 Confirm each MODIFIED block in `specs/recall-query/spec.md` is the main-spec requirement verbatim apart from the intended edits and the added scenarios (diff against `openspec/specs/recall-query/spec.md`)
- [x] 2.2 Run `openspec validate recall-query-terms --strict` and fix anything it reports

## 3. Close out

- [x] 3.1 Verify each scenario in the delta spec is answered by a normative sentence in README.md
- [x] 3.2 Comment on particulars-cli#12 with the rule and the new scenarios, so the baseline lands conformant
- [x] 3.3 Comment on #33 linking the change, and close it when the change is archived — commented 2026-10-17; closing is done at archive
- [x] 3.4 Record in particulars-knowledge: `recall-vector-cache` left the term rule, the combination rule and the order within a resolution value unstated, and its design wrongly said stage-one order never reaches the response; found by #33, raised from the reference implementation two days after the change landed — recorded 2026-10-17 in particulars-knowledge#43 on branch knowledge/recall-query-terms as clm_01a14719-6022-77b0-b62e-2b351d9337ce
