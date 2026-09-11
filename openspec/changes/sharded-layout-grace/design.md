## Context

`dkf/0.2` seals a month when a later month has an id, and promises that a sealed segment never changes. Three changes in two days refined *which* clock decides "later" and what a writer whose clock disagrees may do. #29 shows the question was wrong: with every clock correct, a branch minted in November and merged in December, after main has sealed November, forces the November segment to change. "The newest id in the workspace" is branch-local; the violation appears at merge, where no write rule runs. It has already happened once in the dogfood repository's thirty-seven pull requests, and the open one holds September mints.

The design has to choose between three properties, of which a branching store gives at most two: the index is a pure function of the files; a sealed document never changes; an object can arrive at any time.

## Goals / Non-Goals

**Goals:**
- Ordinary branching — a pull request open across one month boundary — never touches a sealed segment.
- The clock rules become unnecessary and are removed, not kept as belt-and-braces.
- The rebuild stays a pure function of the files.
- What the grace period does not cover is detected without parsing sealed history, reported loudly, and has a stated remedy.
- The one way a bad clock can now do real damage is turned from a warning into a failure.

**Non-Goals:**
- Covering a branch open across two or more boundaries. It is rare, visible, and made loud. See D2.
- A per-workspace grace width. Fixed at one month for `dkf/0.2`; a `dkf.yaml` key is deferred until a workspace needs it.
- Keying index entries by arrival rather than minting month. Considered and rejected in D2.

## Decisions

### D1. A month seals two months later, and the root holds two months

Month M is sealed once an id exists in M+2 or later. The current month C (the newest id's month) and C−1 are open; the root carries `entries` and `retracted` for both, as flat lists — the rebuild reads the files, so it knows each id's month and each retraction's month without the root saying so. Rebuild remains a pure function of the files: C from the newest id; sealed months below C−1; a segment for each sealed month with entries or retractions; the root for the rest.

What follows. A branch open across one boundary merges into an open month: main minting in December seals October, not November, and Alice's November claim goes into the root. Clock skew of hours or days at a boundary lands in the previous month, open. The hot tail is at most two months, still bounded by nothing that grows. And every rule that was about *which* clock decides becomes moot: a writer mints at its own clock and dates a retraction at its own clock, and the only guard left is the one that was always necessary — do not write into a sealed month — which now takes a clock more than a month out to trip.

### D2. The residual is a late merge, detected by counts, and it fails loudly

A branch open across two or more boundaries still merges into a sealed month. The alternative design closes even that: key index entries by *arrival*, as tombstones already are, so a late-merged object goes into the open root and a sealed segment never changes by construction. Rejected, for a cost that is easy to miss. That design breaks the invariant that segment M holds exactly the files in directory M, and the invariant is what makes an incremental rebuild cheap: without it, placing a new entry requires knowing which ids are already indexed, which is a parse of every sealed segment — the cost the whole shape exists to bound. The grace period keeps the invariant and makes the residual loud instead of silent.

Loud, and cheap to detect. Each `segments` entry records `path` and `count`, the number of entries in the segment, which under the invariant equals the number of files in that month's directories across all types. A rebuild or validation lists each sealed month's directories — a directory listing is names, not parses — and compares the count. Equal means untouched, nothing parsed. Different means a file arrived in a sealed month: validation fails naming the files, found by listing that one month against that one segment's ids. The remedy is DKF's rebase: re-mint the branch's objects before merging. Rare enough — a months-old pull request — to be acceptable, and far better than a consumer silently serving a stale segment.

Grace width is a dial. One month covers every pull request the dogfood repository has ever had by a wide margin (longest open: three days). A workspace with quarter-long branches would want more, and since width affects only sealing and not any file's location, a `dkf.yaml` key could carry it. Deferred until asked for.

### D3. The clock rules are deleted, and `object-identifiers` reverts

Mint clamping, the retraction window, "a writer behind the workspace writes at its present", and the definition of an id's instant as its log position all existed to keep a write out of a sealed month when clocks disagreed by seconds at a boundary. The grace period absorbs a month of disagreement. So: an implementation SHALL NOT mint into a sealed month and SHALL NOT date a retraction into one, and that is all. `object-identifiers` returns to "ids created within the same millisecond sort in creation order", and an id's instant is once again a reading of the writer's clock, which is what every consumer of UUIDv7 assumes. Deleting is preferred to keeping the rules as extra safety because each of them had a failure mode of its own — a locked-out writer, a contaminated log — and none of them is needed.

### D4. A far-future id fails validation

Under clamping a bad clock's id was ugly. Under the grace period it seals real months: an id two months ahead seals the current month, and every correct writer's next mint lands in a sealed month and fails. So the validator keeps its warning on anything ahead of its clock — a few days fast at a month end is ordinary — and SHALL fail on an id whose month is two or more months ahead of the validator's current month. "Two or more" is the grace period: an id one month ahead lands in what will be the next open month and seals nothing that is open. A validator two months behind real time is itself broken, which is why a failure is acceptable here where it was not before. The pull-request check, which the dogfood repository already runs, becomes a gate rather than a suggestion, and the id never merges.

### D5. Directory sealing is a cost, not an invariant

A late merge adds a file to an old directory in any design that derives paths from ids, and a retraction always could. The honest statement is the benefit actually delivered: an old month's git tree is rewritten only by a late merge or a retraction, and never by ordinary appends. Stated so, and no longer a SHALL a merge would break.

### D6. Segment counts also serve migration and remote consumers

A `migrate` writes counts as it builds segments. A remote consumer that has cached a segment and later sees its recorded count change in the root knows the workspace failed validation and can refetch — a cheap signal for the rare case, and a better one than the count being absent.

## Risks / Trade-offs

- [A branch open across two boundaries fails validation at merge] → Named, rare, and the remedy (re-mint before merging) is stated. Preferred to silent divergence.
- [Two open months means one more month of git churn on `claims/`] → On a directory already being written; old months are still untouched.
- [A file count per month is a listing of every sealed month's directories on each rebuild] → Names only, no parse, about twelve listings a year of history. Bounded by calendar, not by objects.
- [A far-future id from a validator's own skewed clock fails validation wrongly] → Only if the validator is two months out, in which case it is the broken machine and the failure is correct.
- [The dogfood claims recording the three clock changes now describe deleted rules] → Qualified by a claim that records why; they were true at their timestamps.
