## 1. One clock, in the README

- [x] 1.1 In *`index.yaml`*, restate the current-month sentence: the month of the newest id and nothing else; the root's `retracted` holds every retraction dated in that month or later; a retraction dated ahead waits in the root until a mint passes its month; sealing is driven by mints alone, which is what makes both guards agree
- [x] 1.2 In *Sharding*, restate the retraction guard against the newest id's month — the same bound as minting, and why the same bound matters — and add the upper bound: no retraction dated later than the writer's clock
- [x] 1.3 In *Sharding*, add the validator warning: an id or timestamp later than the validator's clock is reported per object as a warning, never an error, and why a warning

## 2. The filtering bound, in the README

- [x] 2.1 Replace "filtering is bounded by the period filtered" with the bound the design delivers: the period filtered plus the months elapsed since it, about twelve reads a year, independent of how many objects exist; say why the alternative (tombstones by minting month) was and remains rejected

## 3. Close out

- [x] 3.1 Verify each scenario across the three delta specs is answered by a normative sentence in README.md, including the retraction-dated-ahead, mint-between, future-dated-retraction, and skewed-id scenarios
- [x] 3.2 Confirm every MODIFIED block copies its baseline requirement text in full with every pre-existing scenario retained; confirm the ADDED requirement has scenarios
- [ ] 3.3 Comment on and close #27: single clock rather than bounding mints by the current month, and why (no refusal for another machine's clock; a typo degrades to a visible wait rather than a sealed year); upper bound on retraction timestamps taken; validator warning added; README bound corrected
- [x] 3.4 Commented on particulars-cli#11 (2026-09-11): stage 2's current-month rule is single-clock; `retract` refuses a future timestamp; `validate` warns on future-dated ids and timestamps
- [ ] 3.5 Record in particulars-knowledge: a claim qualifying the 2026-09-11 corrections claim with the single-clock rule and the two bounds
