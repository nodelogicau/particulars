## Why

Issue [#51](https://github.com/nodelogicau/particulars/issues/51) found that `workspace-layout` lets a sealed-month file change only by appending a `retracted` block. But `particular_define` updates a particular's `label` and `aliases` in place, and since `add-redaction` a redaction rewrites a claim or synthesis file too. So the requirement and its git-benefit sentence are both wrong on `main`. The semantic cache rests on the same false premise: it assumes objects are "immutable apart from retraction", so it never recomputes the label and alias vectors of a particular that has changed. The issue also found that the worked example of path derivation states the wrong instant.

## What Changes

- `workspace-layout`, *A sealed month gains no files*: list every modification permitted to a file in a sealed month. These are appending a `retracted` block, adding or extending a `redacted` block (`dkf/0.3`), and updating a particular's `label` and `aliases`. State that none of them changes an index entry or a segment. Rewrite the git-benefit sentence and its scenario to name the same set. Add scenarios for an alias update and a redaction in a sealed month.
- `workspace-layout`, *Deriving a path*: correct the stated instant of `clm_01a0f3c1-4d20-…` from 2026-09-05T01:01:35Z to 2026-09-30T19:18:46.816Z. The derived path is unchanged.
- `retraction`: narrow "exactly two permitted modifications to an existing object file" to the files that can be retracted, and name the particular update as the separate rule it is.
- `recall-query`, semantic cache: a particular's label and alias vectors SHALL be recomputed when its `label` or `aliases` change. The change is detected against what the cache recorded, not from the index, which does not mirror those fields. The README's "immutable apart from retraction" and "Only `content` is embedded" are corrected.
- README Status: record the particular-update exception as a **v0.2 erratum**. It describes behaviour v0.2 already had, so it is not a format change and does not bump `format`.

None of these is breaking. No file is read differently, and no writer that conformed to v0.2's actual behaviour becomes non-conformant.

## Capabilities

### New Capabilities

None.

### Modified Capabilities

- `workspace-layout`: the sealed-month requirement enumerates the permitted modifications and corrects the git-benefit statement; the path-derivation scenario's instant is corrected.
- `retraction`: the "exactly two permitted modifications" rule is scoped to retractable files, with particulars named as governed by `particular_define`.
- `recall-query`: the semantic cache recomputes a particular's vectors when its label or aliases change.

## Impact

- `README.md`: the Sharding section's git-benefit sentence, the Retraction rules, the semantic-cache bullets, and the Status section (erratum).
- `openspec/specs/workspace-layout`, `retraction`, `recall-query`.
- particulars-cli: no behaviour change needed. Its `particular define` already updates particulars in sealed months without writing an index document (particulars-cli#24, #25). A semantic cache, if it is implemented, must follow the new recompute rule.
