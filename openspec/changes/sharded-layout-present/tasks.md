## 1. The workspace's present, in the README

- [x] 1.1 In *Identifiers*, extend the monotonic sentence: an id's instant is its position in the workspace's log, not a reading of the clock; an implementation never mints earlier than the newest id in the workspace and advances the instant when its clock is behind; assertion time is `timestamp` and the two need not agree
- [x] 1.2 In *Sharding*, restate the guards as one rule — a writer behind the workspace writes at the workspace's present, a writer ahead writes at its own: the retraction window (not earlier than the start of the newest id's month, not later than the later of the writer's clock and that instant, so never empty); the mint clamp (just after the newest id, landing in the open month, not moving the seal); no write refused because another clock disagreed; why the typo protection survives
- [x] 1.3 In *Sharding*, state the trade and the practice: a far-future id, once merged, is the workspace's present until the calendar reaches it, under refusal a frozen workspace and under clamping a bad month every later id carries; only a clock dates an id, so every correctly set validator flags it the day it appears; the pull-request check is where it is caught, before it is merged
- [x] 1.4 Reconcile the validator-warning paragraph with the clamp: a clamped id warns on the behind machine, correctly, and does not fail

## 2. Close out

- [x] 2.1 Verify each scenario across the two delta specs is answered by a normative sentence in README.md, including behind-writer retraction, behind-writer mint, writer ahead, clamped-id warning, and far-future id caught at review
- [x] 2.2 Confirm both MODIFIED blocks copy their baseline requirement text in full with every pre-existing scenario retained
- [ ] 2.3 Comment on and close #28: retraction window as proposed; mint clamped rather than refused, and why (the workspace-wide form of the monotonic counter; a clamped mint does not move the seal); the contagion trade and the pull-request practice; the #27 "no write refused" claim now true
- [x] 2.4 Commented on particulars-cli#11 (2026-09-11): every minting verb and `retract` clamp to the newest id when the clock is behind; the refusal paths from the previous two comments are withdrawn except the sealed-month and no-attestation cases; the DKF check should surface future-dated warnings where a reviewer sees them
- [ ] 2.5 Record in particulars-knowledge: a claim qualifying the third claim of #39 — no write is refused for a clock disagreement is now true, and how
