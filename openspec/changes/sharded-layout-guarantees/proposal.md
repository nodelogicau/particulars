## Why

`sharded-layout-grace` added two things beside the grace period, and #30 finds each inconsistent with itself. The count short-circuit says a sealed segment is parsed only when its month's file count differs from the recorded count; a retraction appends a block to a file already counted, so a sealed segment is never parsed for its `retracted` list and the scenario *A retraction dated into a sealed month*, written under that very requirement, cannot be reached. The late-merge check it was added for therefore catches a branch that mints across two boundaries and misses one that retracts. And the validator requirement justifies warning on a future-dated id by "the validator's clock may be the one that is wrong", then fails on an id two months ahead without noticing that the same uncertainty applies; the failure is right, and the reason given for it is not.

The one-clause fix #30 proposes for the first point — parse a sealed segment when the regenerated index carries a retraction dated in that month — is right in effect and hides a cost: finding such a retraction means reading the `retracted` block of every file minted at or before that month, which is the whole-history parse the count check exists to avoid. The fix belongs in the operation that already pays that cost.

## What Changes

- **The two operations guarantee different things, and the spec says so.** The drift check stays bounded: counts for sealed months, full comparison of the open documents and `index/legacy.yaml`. What a matching count guarantees is that no file arrived in that month — no late *mint* — and that is all the count carries; the spec states it. Validation, which parses every object file, additionally regenerates each sealed month's `retracted` list from the files and compares it with the committed segment. A retraction dated into a sealed month, whether a guard violation or a late-merge retraction, is caught there, and the scenario that was unreachable moves under validation, where it is reachable.
- **The validator's failure rule is justified by consequence.** The uncertainty about whose clock is wrong is identical for the warning and the failure. What differs is what each error costs: a validator two months slow fails a healthy workspace, and that is the better error, because the alternative is accepting an id that seals the month every correct writer is using.

Not **BREAKING**: no document shape or write rule changes; two operations are described more precisely.

## Capabilities

### New Capabilities

None.

### Modified Capabilities

- `index-manifest`: the drift-check requirement states what the count guarantees and moves the sealed-month retraction comparison to validation; a new requirement defines what validation compares for sealed segments.
- `workspace-layout`: the validator requirement's rationale for failing on a far-future id is replaced.

## Impact

- `README.md` — *`index.yaml`*: the drift-check paragraph says what a matching count does and does not guarantee, and that `validate` compares every sealed segment's `retracted` against the files; *Sharding*: the far-future sentence gives the consequence-based reason.
- **Closes #30.**
- `particulars-cli#11` — comment: `index --check` stays counts plus open documents; `validate` additionally regenerates each sealed month's tombstone list and compares; nothing else moves.
- Dogfood: the fifth claim in particulars-knowledge#39 describes the count check without this precision; a sixth claim qualifies it. The claim is small; the pattern it completes — six changes, five corrections, all before implementation — is the thing worth recording.
