## 1. Spec

- [x] 1.1 Add `standalone-conformance`: no field requires another format's identifier; no rule constrains another format; the Conformance section states what is normative, including prose rules
- [x] 1.2 Modify *The specification states its relationship to intentions* in `format-purpose`: standing alone is stated before the family

## 2. README

- [x] 2.1 Add a Conformance section after The Approach
- [x] 2.2 In *Purpose*, state that DKF is complete on its own, then describe the family, and say a log of what happened *can be kept* in episodes

## 3. Verify

- [x] 3.1 Run `openspec validate standalone-spec --strict` and fix any findings
- [x] 3.2 Check *Purpose* still contains no capitalised requirement keyword
