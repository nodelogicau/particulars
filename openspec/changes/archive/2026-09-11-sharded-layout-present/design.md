## Context

Three changes in two days have refined how `dkf/0.2` seals months. `sharded-layout-clock` settled that one clock drives sealing — the newest id's month — and bounded a retraction's timestamp on both sides. #28 shows the two bounds can leave no legal timestamp at all, and that the same condition refuses mints, so a writer whose clock is behind the workspace can write nothing. The condition is ordinary: two machines, a small skew, a month boundary. The effect is total for as long as the skew lasts, and for a badly wrong clock that is the length of the error.

The reference implementation mints from `time.Now()` and stamps retractions the same way, so it reaches this state only through a skewed system clock on one of two machines sharing a workspace — which is the deployment DKF is for.

## Goals / Non-Goals

**Goals:**
- Every writer can always write, whatever the clocks around it say.
- What a writer records when its clock is behind is the workspace's present, which the files already attest to.
- The one bad case — a far-future id already merged — is named, its two failure modes compared, and the practice that prevents it stated.

**Non-Goals:**
- Detecting clock skew. The format sees files, not clocks.
- Repairing a far-future id inside the format. Files admit one appended block; the id is permanent once merged.
- Reopening single-clock sealing. It is what makes "the workspace's present" a well-defined instant.

## Decisions

### D1. The retraction window is never empty

The lower bound stays: a retraction is not dated earlier than the start of the newest id's month, because that is the earliest instant that lands in an unsealed segment. The upper bound becomes the later of the writer's clock and that same instant. When the writer is ahead of or level with the workspace, this is the old rule. When the writer is behind, it may date the retraction at the start of the newest id's month — the workspace's present — which is what *A retraction dated into a sealed month* already tells a writer to do when forced to redate. Typo protection survives because the permitted instant is one the workspace attests to; a year that no id and no clock suggests is still refused. This is #28's fix as proposed.

### D2. A mint is clamped to the newest id, not refused

#28 leaves mints refused, reasoning that a mint moves the seal and so cannot be exempt from it. A clamped mint does not move the seal: it lands in the newest id's month, which is the current month and open. What it does is take its instant from the workspace rather than the writer's clock, which `object-identifiers` already permits within a process — the monotonic counter exists precisely to move an id off the raw clock so that creation order holds when the clock is not fine enough. Extending that from "within a millisecond, in one process" to "across the workspace" changes the scale of the correction and not its kind. An id's instant is its position in the log, and the log is the workspace. Assertion time is `timestamp`, and consumers were never allowed to require the two to agree.

The alternative is #28's: refuse, and state the lockout as inherent. Rejected because the lockout is total, because it is triggered by a state the format expects (the validator warns on it rather than forbidding it), and because a write that can be made safely should be made. The mint clamp is the mirror of D1 with the same justification: write at the workspace's present.

### D3. With both, no write is refused for a clock disagreement

The claim in the #27 ruling was false for ids dated ahead. D1 and D2 make it true, and the README states it as a property of the design rather than leaving it in an issue comment: a writer behind the workspace writes at the workspace's present; a writer ahead of it writes at its own.

### D4. Contagion is the trade, and the pull-request check is the practice

A far-future id, once in the workspace, is the workspace's present until the calendar reaches it. Under refusal every writer waits; under clamping every later id carries the bad month, and every validator on a sane machine warns on each new object. Neither is good and the difference is whether the team can work, so clamping wins, but the choice should not hide the cost.

The mitigation is not in the format. Nothing dates an id but a clock, so a far-future id is always a bad machine, and every *other* machine's validator flags it the day it appears — the warning is proportionate to the harm precisely here. The README names the practice: objects arrive on a branch, the DKF check on the pull request surfaces the warning, and a reviewer declines to merge a future-dated object. The dogfood workspace already runs `validate` on every pull request. Caught there, the id never becomes a permanent fact; missed there, the workspace has a bad month to live through, working.

### D5. The validator warning is unchanged and still honest

A clamped id is later than the behind writer's clock and no later than the newest id. A validator on the behind machine warns on it, correctly: from where it stands the id is in the future. A validator on the ahead machine sees nothing wrong. Both are right about what they can see, which is why it is a warning.

## Risks / Trade-offs

- [Clamped ids carry a month the writer's clock never saw] → Stated as the trade in D4; visible to every sane validator; bounded by the pull-request practice; and the id's instant is defined as log position, not wall-clock time.
- [A writer far behind the workspace mints many ids in the same clamped millisecond range] → The monotonic counter already handles ordering within a millisecond; clamping just after the newest id and advancing per mint keeps creation order.
- [Two behind writers on separate branches both clamp to the same newest id] → Their ids interleave on merge exactly as two writers minting at the same wall-clock instant would today; ids are unique by their random bits, and the index is regenerated on merge.
- [The dogfood claim that "no write is refused" was recorded before this change made it true] → Qualified by a claim recording this change.
