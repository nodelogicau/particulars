## 1. README

- [x] 1.1 In *Recall by query*, under *The baseline*:
  - whitespace is trimmed from the edges of the whole query along with category P, using the same `White_Space` property the split uses;
  - interior whitespace is kept;
  - a query of whitespace alone resolves nothing and is not an error.
- [x] 1.2 In *`resolution`*:
  - exact allows punctuation or whitespace around the occurrence, so `Project X ?` and a line of input with a trailing newline are exact;
  - `Project  X` (two spaces) is not.
- [x] 1.3 In *`resolution`*, add the longest-exact-first key within `label` and `alias`, with the `C`/`C#` example. Say why the exact rule isn't tightened instead: it would make one particular's `resolution` depend on which others exist.

## 2. Delta spec

- [x] 2.1 Confirm each MODIFIED block in `specs/recall-query/spec.md` is the main-spec requirement verbatim apart from the intended edits and the added scenarios. Check by diffing against `openspec/specs/recall-query/spec.md`.
- [x] 2.2 Run `openspec validate recall-query-whitespace --strict` and fix anything it reports.

## 3. Close out

- [x] 3.1 Verify each scenario in the delta spec is answered by a normative sentence in README.md.
- [x] 3.2 Comment on particulars-cli#12 with the changes: `isEdge` gains `White_Space`, the exact check accepts whitespace outside the occurrence, and longest-exact ordering applies within `label` and `alias`. Include the new scenarios.
- [x] 3.3 Comment on #37 linking the change, and close it when the change is archived. Commented 2026-10-24; closing happens at archive.
- [x] 3.4 Add a comment on #38 noting that a term which trims to a single letter (`C#` → `c`) matches nearly every object. That belongs to the response-size and weighting question.
- [x] 3.5 Record in particulars-knowledge: `recall-query-terms` trimmed punctuation but not whitespace from the whole query, and its ordering keys couldn't separate `C` from `C#`. #37 found both, from the reference implementation. Recorded 2026-10-24 on branch knowledge/recall-query-whitespace as clm_01a16bef-35bc-733c-815f-1cf5d45a2af8.
