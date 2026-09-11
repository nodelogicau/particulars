## Why

`sharded-layout-clock` bounded a retraction's `timestamp` below by the newest id's month and above by the writer's clock. Each bound is right; their intersection can be empty. Whenever the workspace holds an id dated in a month later than a writer's current month — a machine two days fast minting across a month boundary, the exact state the change's own validator-warning scenario describes — the earliest legal retraction timestamp is later than the writer's clock, and the writer can retract nothing. Its mints are refused by the same condition, since a fresh id would be earlier than the newest one. Every write is closed until its calendar catches up (#28). The upper bound accepted in #27 removed the one exit that had existed, and there is no recovery inside the format because a file admits only an appended block.

## What Changes

- **A writer behind the workspace writes at the workspace's present.** The bound on a retraction's `timestamp` becomes: not earlier than the start of the newest id's month, and not later than the later of the writer's clock and that same instant. The window is never empty; a timestamp that neither the writer's clock nor any id in the workspace attests to is still refused.
- **A mint is clamped, not refused.** An implementation whose clock is behind the newest id in the workspace SHALL mint its id at an instant just after that id rather than refuse. This is the workspace-wide form of the rule `object-identifiers` already has within a process, where a monotonic counter moves an id off the raw clock so that creation order holds. An id's instant is its position in the workspace's log; assertion time lives in `timestamp`, and the two were never required to agree. A clamped mint lands in the current month, which is open, so it does not move the seal.
- **No write is refused because another machine's clock disagrees.** With both rules, the claim made in the #27 ruling becomes true; without the mint clamp it was false for an id dated ahead.
- **The trade is stated, and the practice that bounds it is named.** A far-future id, once merged, becomes the workspace's present until the calendar reaches it: under refusal the workspace freezes, under clamping every later id carries the bad month and every sane validator warns on each. Nothing dates an id but a clock, so a far-future id is always a bad machine, and every other machine's validator flags it the day it appears. The README SHALL say that the pull-request check is where such an id is caught, before it is merged and becomes a permanent fact.

Not **BREAKING**: no implementation has shipped `dkf/0.2`; no document shape changes.

## Capabilities

### New Capabilities

None.

### Modified Capabilities

- `workspace-layout`: the sealed-month requirement's retraction bounds are restated with the non-empty window, the mint clamp replaces the mint refusal, and the validator-warning requirement gains the clamped-id scenario.
- `object-identifiers`: minting SHALL be monotonic across the workspace, not only within a millisecond in one process; the id's instant is defined as its log position, which the writer's clock supplies when it is ahead of the workspace and the newest id supplies otherwise.

## Impact

- `README.md` — *Identifiers*: the monotonic rule extended to the workspace, with the id's instant as log position; *Sharding*: the two guards restated as "write at the workspace's present", the retraction window, the mint clamp, the contagion trade-off, and the pull-request check as the practice.
- **Closes #28.**
- `particulars-cli#11` — comment: `retract` and every minting verb clamp to the newest id when the clock is behind; the refusal paths from the previous comment are withdrawn; the DKF check workflow should surface future-dated warnings prominently.
- Dogfood: the third claim in particulars-knowledge#39 says no write is refused for a clock disagreement, which was untrue for ids; a fourth claim qualifies it. The dogfood CI already runs `validate` on every pull request, so the named practice is in place.
