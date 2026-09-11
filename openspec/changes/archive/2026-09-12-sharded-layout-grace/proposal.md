## Why

Sealed-segment immutability is the promise the `dkf/0.2` index is built on: git leaves an old tree alone, and a remote consumer fetches a segment once and caches it forever. Ordinary git branching breaks it with every clock correct (#29). A claim minted on a branch on 28 November, merged on 5 December after main has minted in December and sealed November, must be indexed in `index/2026-11.yaml` — the rebuild is a function of the files — and that segment was sealed, committed, and by then cached by anyone who took the specification at its word. No write rule can see this: every guard since `sharded-layout-corrections` was bounded by "the newest id in the workspace", and on a branch that quantity is branch-local, with the violation appearing only at merge, where nobody is minting. The dogfood repository has already done it once in thirty-seven pull requests (opened 31 August, merged 2 September), and its open pull request holds September mints.

The three clock changes of 10–11 September were each a correct answer to the wrong question, which assumed one linear history in a format that is git-native. This change answers the right one, and in doing so deletes them.

## What Changes

- **A month seals on a grace period.** A month M is sealed once an id exists in month M+2 or later. The current month and the month before it are open; the root carries the entries and retractions of both. A branch open across one month boundary merges into an open month, and clock skew of hours at a boundary lands in the previous month, still open.
- **The clock rules go.** No mint clamp, no retraction window, no "writer behind the workspace". A writer mints at its own clock and dates a retraction at its own clock; the only guard is that neither may land in a sealed month, which with the grace period takes a clock more than a month out. `object-identifiers` reverts to its intra-process monotonic rule and an id's instant is once again a reading of the clock.
- **Each segment records its entry count.** `segments` becomes a list of `path` and `count`. A rebuild or validation compares the number of files in a sealed month's directories with the recorded count and parses nothing unless they differ. A difference is a late merge — a branch open across two or more boundaries — reported as a validation failure naming the files, whose remedy is to re-mint on the branch before merging. Loud, not silent.
- **A far-future id fails validation, not just warns.** A validator still warns on any id or timestamp ahead of its clock; it SHALL fail on an id two or more months ahead, because such an id now seals real months and every correct writer would then be minting into sealed ones. The pull-request check becomes a gate.
- **Directory sealing is a cost statement.** An old month's git tree is rewritten only by a late merge or a retraction; that is the benefit delivered, and it is no longer stated as a SHALL a merge could break.

Not **BREAKING**: no implementation has shipped `dkf/0.2`. Relative to the shape as published yesterday, the root holds two months and `segments` entries gain a count.

## Capabilities

### New Capabilities

None.

### Modified Capabilities

- `index-manifest`: the root carries two open months; `segments` entries carry `path` and `count`; sealing is two months later; the drift check compares counts before parsing and reports a late merge.
- `workspace-layout`: the sealed-month requirement restated with the grace period and the single "not into a sealed month" guard, the clamp and window deleted, late merges named with their remedy, directory churn restated as cost; the validator requirement gains the two-months-ahead failure.
- `object-identifiers`: reverted to the intra-process monotonic rule; the log-position definition and the workspace-wide clamp removed.
- `retraction`: a retraction is dated at the writer's clock and refused only into a sealed month; the root holds retractions dated in either open month or later.

## Impact

- `README.md` — *Identifiers*: the clamp paragraph reverted; *Sharding*: sealing on a grace period, the one guard, late merges and their remedy, the count check, the hardened validator rule, directory churn as cost; *`index.yaml`*: the root's two months, `segments` with counts, the current-month sentence, the cache-forever promise stated as true for any branch open across at most one boundary and loud beyond that.
- **Closes #29.**
- `particulars-cli#11` — comment: stage 2 simplifies — two open months, counts in `segments`, no clamp, no window; `validate` gains the count check and the two-months-ahead failure; `migrate` writes counts.
- Dogfood: the third and fourth claims in particulars-knowledge#39 describe rules this change deletes; a fifth claim records why. Pull request #39 itself is the scenario: opened 10 September with September mints, it merges into an open month under this rule whenever it merges before November.
- Grace width is fixed at one month for `dkf/0.2`; a `dkf.yaml` key widening it is deferred until a workspace with quarter-long branches asks.
