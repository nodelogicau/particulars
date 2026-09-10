## Why

`sharded-layout-corrections` bounded mints by one quantity and retractions by another. Minting may not go earlier than the newest id's month; a retraction may not be dated earlier than the *current* month, which is the later of the newest id's month and the newest retraction's month. Whenever a retraction is dated into a month with no mints yet — a state the change explicitly contemplates in *A month of retractions only* — the current month runs ahead of the newest id, and a mint into the gap passes its guard while producing an entry whose only home is a sealed segment. A correct rebuild must then either rewrite a sealed segment or disagree with the files, and drift can never clear (#27). Honest clocks never reach it; two machines at a month boundary, or a retraction timestamp typo'd a year ahead, do — and the typo seals twelve months at a stroke, because nothing bounds a retraction timestamp from above.

The same review found the README summary "filtering is bounded by the period filtered" claims more than the design delivers: checking one August object five years on reads sixty-one tombstone lists. The bound is real, but it is elapsed calendar months, not the period.

## What Changes

- **One clock seals.** The current month is the month of the newest id in the workspace, and nothing else. The root carries the entries of that month and every retraction whose `timestamp` month is that month *or later*; a segment carries its month's entries and its month's retractions, as now. Sealing is driven by mints alone, so no mint that passes its guard can land in a sealed month, and the two guards bound against the same quantity. A retraction dated ahead simply waits in the root until a mint passes its month. Nothing is ever refused because another machine's clock is wrong.
- **A retraction is not dated into the future.** A writer SHALL NOT write a retraction whose `timestamp` is later than its own clock. It is the mirror of the existing lower bound, and it stops the one plausible way of opening the hole that the single clock does not already close.
- **A validator warns on time it cannot have seen.** An id minted, or an object or retraction timestamp dated, later than the validator's own clock SHOULD be reported as a warning naming the object. Writer rules cannot reach a hand-edited file or another implementation; this can.
- **The README says what the filtering bound is:** the period filtered plus the months elapsed since it, about twelve reads a year and independent of how many objects exist.

Not **BREAKING**: no implementation has shipped `dkf/0.2`; the shape of every document is unchanged, only which retractions the root holds while a later month has no mints.

## Capabilities

### New Capabilities

None.

### Modified Capabilities

- `index-manifest`: the current month is defined by the newest id alone; the root's `retracted` holds retractions dated in the current month or later; the deterministic-rebuild and retractions-only scenarios restated.
- `workspace-layout`: the retraction guard is bounded by the newest id's month, gains an upper bound at the writer's clock, and a validator warning for future-dated ids and timestamps is added.
- `retraction`: the index consequence uses the same clock; the timestamp bounds are stated on the retraction itself.

## Impact

- `README.md` — *Sharding*: the retraction guard restated against the newest id's month, with the upper bound and the validator warning; *`index.yaml`*: the current-month sentence and the rollover sentence, the root's `retracted` scope, and the filtering-bound sentence.
- **Closes #27.**
- `particulars-cli#11` — comment: stage 2's current-month rule is now single-clock; `retract` refuses a future timestamp; `validate` warns on future-dated ids and timestamps.
- Dogfood: the 2026-09-11 corrections claim in particulars-knowledge#39 describes the two-clock rule; a claim recording this change qualifies it.
