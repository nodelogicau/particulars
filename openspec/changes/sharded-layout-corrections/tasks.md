## 1. The legacy shard, in the README

- [x] 1.1 In *Sharding*, add the `legacy` shard: an id from which no month derives — not a UUID, or a UUID of a version other than 7 — lives at `<type-dir>/legacy/<id>.yaml`; the path stays a function of the id and the stray-file rule stays absolute; the directory is never sealed and no conformant writer adds to it; why `legacy` over `unknown`
- [x] 1.2 Add `legacy/` to the File Layout tree under one type directory and `index/legacy.yaml` under `index/`, marked as present only when such ids exist
- [x] 1.3 In *Migration*, name the legacy target and state that a draft-era id migrates with its id unchanged

## 2. Tombstones by retraction month, in the README

- [x] 2.1 Rewrite the index examples: the segment carries `retracted` for objects retracted in its month; the root's `retracted` holds the current month's only; `index/legacy.yaml` first under `segments`
- [x] 2.2 Restate the current-month rule: the later of the newest id's month and the newest `retracted.timestamp`'s month; a month with retractions and no mints yields a segment with empty `entries`
- [x] 2.3 Rewrite the "`retracted` is why" paragraph around the retraction month: append and retract touch the root only and nothing rewritten grows with history; sealed segments byte-immutable without exception; "what changed since" is the root plus newer segments, retractions included; an object minted in M is retracted iff its id is in a `retracted` list of M or later, so filtering is bounded by the period filtered; legacy objects need every list
- [x] 2.4 Add the retraction guard beside the minting guard in *Sharding*: no retraction timestamp into an earlier month than the current; a late retraction carries a current timestamp and a `reason` that says when
- [x] 2.5 Update the drift-check paragraph: each document's `retracted` compared by id, `index/legacy.yaml` included

## 3. Corrections to what was claimed

- [x] 3.1 In the `dkf.yaml` section, replace the "may accept `dkf/0.2` and misread … one such reader exists and is updated" passage: the reference implementation has refused an unknown `format` on every verb since its first commit, naming the version; the rule is stated as the behaviour every reader must share, and the caveat is withdrawn
- [x] 3.2 In *Unbounded History, Bounded Work*, say the 1.3 s / 700 MB / ~6.7 KB figure is index parsing alone; add the full `index --check` measurement over real object files (~29 KB per entry marginal, tens of gigabytes at a million objects), attributed to particulars-cli#11; keep the conclusion both support, that cost is linear in history
- [x] 3.3 Fix the CLI issue's premise in particulars-cli#11 by comment: withdraw "ship refusal first"; describe the per-segment tombstones keyed by retraction month, the two-clock current-month rule, the retraction guard, and the `legacy/` shard and `index/legacy.yaml`

## 4. Close out

- [x] 4.1 Verify each scenario across the three delta specs is answered by a normative sentence in README.md, including the draft-era id, the retraction-only month, the retraction dated into a sealed month, and the legacy-object filtering cost
- [x] 4.2 Confirm every MODIFIED block copies its baseline requirement text in full with every pre-existing scenario retained
- [ ] 4.3 Comment on and close #25 (reserved `legacy` shard and segment, trigger "no month derives") and #26 (tombstones keyed by retraction month, carried in that month's segment; why over per-minting-month or a stated ceiling)
- [ ] 4.4 Record in particulars-knowledge: a claim qualifying the `sharded-layout` claim of 2026-09-10 with the corrected tombstone shape, the legacy shard, and the two withdrawn statements
