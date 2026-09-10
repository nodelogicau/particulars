## Why

The CLI-side review of `sharded-layout` (particulars-cli#11) found two holes in the shape it introduced and two errors in the prose that justified it, all before any implementation shipped, which is the moment they are cheapest to fix.

**#25.** `object-identifiers` requires readers to accept ids that carry no UUIDv7 timestamp; `workspace-layout` derives a file's path from that timestamp and forbids any other source. Under `dkf/0.2` a draft-era id has no derived path, so `migrate` has nowhere to put it, the wrong-month check cannot evaluate it, and the only natural home — the type-directory root — is what *Layout is not guessed* reports as misplaced. A conforming implementation cannot both accept the id and place it.

**#26.** The root index carries every retracted id in the workspace, and every append rewrites the root. So an append costs in proportion to the total retractions in history, which *The cost of an operation is bounded by its working set* — in the same change — exists to forbid. The scenario is met by the letter (one file rewritten) and broken in the quantity it was written to bound. A million objects at 5% retracted means every `claim assert` re-serialises fifty thousand ids, and the one document a remote consumer must poll is the one that never stops growing.

**Two corrections.** The README says a pre-0.2 reader "may accept `dkf/0.2` and misread" and that the reference implementation "is updated with the rule". Verified against the released binary: it refuses today, on every verb, naming the version. And the README's per-entry figure describes index parsing only; the CLI's own measurement of a full `index --check` with real object files puts the marginal cost near 29 KB per entry, so a million-object workspace is tens of gigabytes, not seven. The linear behaviour is what both measurements agree on and the case is stronger, but the text claims more than it measured.

## What Changes

- **A reserved `legacy` shard.** An id from which no month derives — one that is not a UUID, or a UUID of a version other than 7 — SHALL live at `<type-dir>/legacy/<id>.yaml`, and its index entry in `index/legacy.yaml`, listed first under `segments`. `legacy` cannot collide with a `YYYY-MM`. The path stays a pure function of the id; the stray-file rule stays absolute; `migrate` gains a target. No conformant writer mints such an id, so the shard is finite and in practice never changes; it is exempt from the sealed-month rule and a change to it is ordinary drift.
- **Tombstones are keyed by the month of the retraction and carried in that month's segment.** A segment carries the entries minted in its month and the ids retracted in its month; the root carries the current month's both; the current month is the month of the newest id or of the newest `retracted.timestamp`, whichever is later, so a rebuild remains a function of the files. No new file kind. Appending and retracting each rewrite the root only. Sealed segments stay byte-immutable. A consumer's "what changed since" is the root plus the segments newer than its last visit, retractions included. Filtering objects minted in month M needs only the segments from M onward, because nothing is retracted before it is minted. Implementations SHALL NOT write a retraction whose timestamp falls in a month earlier than the current one, mirroring the minting guard.
- **README corrected on both points**: the refusal rule is stated as already the reference implementation's behaviour, with the caveat withdrawn; the cost paragraph distinguishes the index-parse figure from the full-check figure and cites the latter.

Not **BREAKING** relative to `dkf/0.2` as published: no implementation has shipped it. Relative to `dkf/0.1`, nothing changes that `sharded-layout` had not already changed.

## Capabilities

### New Capabilities

None.

### Modified Capabilities

- `workspace-layout`: the sharding requirement gains the `legacy` shard and its trigger; the sealed-month requirement exempts it and adds the retraction-timestamp guard; the bounded-cost scenarios cover retraction; migration names the legacy target.
- `index-manifest`: the hot-tail requirement is restated with per-month tombstones and the two-clock current-month rule; `index/legacy.yaml` joins the segments; the drift check compares each document's `retracted` list.
- `retraction`: the index consequence of a retraction is an id in the root's `retracted` for the current month, later sealed into that month's segment.

## Impact

- `README.md` — *Sharding*: the legacy shard and its reason; *`index.yaml`*: the segment shape gains `retracted`, the current-month rule gains the retraction clock, the "why tombstones" paragraph is restated around retraction month, and the filtering rule (segments from M onward) is stated; *`dkf.yaml`*: the refusal caveat replaced; *Unbounded History, Bounded Work*: the numbers corrected and attributed.
- **Closes #25 and #26.**
- `particulars-cli#11` — comment: withdraw the "ship refusal first" premise; tombstones now per segment keyed by retraction month; `legacy/` shard and `index/legacy.yaml`; the current-month rule reads both clocks; the retraction guard.
- Dogfood: unaffected until migration; the claim recording `sharded-layout` (particulars-knowledge#39) is qualified by a claim recording these corrections when they land.
