## 1. Sealing on a grace period, in the README

- [x] 1.1 In *Sharding*, replace the sealing sentence and the whole "one rule keeps every write out of a sealed month" passage: a month seals once an id exists two months later; the current month and the one before are open; a branch open across one boundary merges into an open month and clock skew at a boundary lands in an open month; the only guard is "not into a sealed month", which takes a clock more than a month out; a writer mints and dates retractions at its own clock
- [x] 1.2 In *Sharding*, add late merges: a branch open across two or more boundaries adds a file to a sealed month; validation fails naming it; the remedy is to re-mint on the branch before merging; why the grace period was chosen over keying entries by arrival (the segment-equals-directory invariant is what keeps an incremental rebuild cheap)
- [x] 1.3 In *Sharding*, restate the git consequence as the benefit delivered: an old month's tree is rewritten only by a late merge or a retraction
- [x] 1.4 In *Sharding*, replace the far-future paragraph: warn on anything ahead of the validator's clock; fail on an id two or more months ahead, because it would seal the month correct writers are minting into; the pull-request check is a gate; the contagion paragraph goes with the clamp
- [x] 1.5 In *Identifiers*, revert the log-position paragraph: an id's instant is a reading of the clock; the monotonic counter is intra-process; the two-clocks sentence in the assertion-time paragraph goes

## 2. The index, in the README

- [x] 2.1 In *`index.yaml`*, update the examples: `segments` entries carry `path` and `count`; the root's `entries` and `retracted` cover two months; the segment comments say "sealed two months later"
- [x] 2.2 Restate the current-month sentence: the open months are the newest id's month and the one before; rollover moves the older open month out when a mint lands two months after it
- [x] 2.3 Add the count check: a rebuild or drift check compares each sealed month's file count with the recorded count and parses nothing unless they differ; a difference is a late merge
- [x] 2.4 Restate the cache-forever promise: true for a workspace that validates, which is any whose branches merge within a month of a boundary; a workspace that fails the count check has a segment its consumers must refetch, and the changed count in the root is the signal

## 3. Close out

- [x] 3.1 Verify each scenario across the four delta specs is answered by a normative sentence in README.md, including the one-boundary branch, the two-boundary branch, the skewed mint that lands open, the writer more than a month behind, the count check, and the two-months-ahead failure
- [x] 3.2 Confirm every MODIFIED block copies its baseline requirement in full; note deliberately dropped scenarios (the clamp and window scenarios of `sharded-layout-present` and `-clock`) as removals, not omissions
- [x] 3.3 Commented on and closed #29 (2026-09-12, landed as 0595336): grace period accepted with the count check and the hardened validator; the arrival-keyed alternative considered and why rejected; the clock rules deleted and `object-identifiers` reverted as proposed; the dogfood evidence (one of thirty-seven PRs crossed a boundary; #39 is the scenario)
- [x] 3.4 Commented on particulars-cli#11 (2026-09-12): stage 2 simplifies to two open months, counts in `segments`, no clamp, no window; `validate` gains the count check and the two-months-ahead failure; `migrate` writes counts; the three clock comments are superseded
- [x] 3.5 Recorded in particulars-knowledge#39 as clm_01a0928e-5938-713c-b38a-71d0dba1bf6d: a claim recording the grace period and why the three clock changes were answers to the wrong question, qualifying the third and fourth claims of #39
