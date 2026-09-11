# Workspace Layout Specification

## Purpose

Defines the bounded-working-set principle, the `dkf/0.2` sharded directory layout and the derivation of a file's path from its id, the format-version gate that makes a change of shape safe, and migration from the flat `dkf/0.1` layout.

## Requirements

### Requirement: The cost of an operation is bounded by its working set
The specification SHALL state that a workspace's history is unbounded and that no operation it defines SHALL require reading data in proportion to that history when the operation concerns a bounded part of it. In particular, reading the objects of a bounded period, appending an object, retracting an object, checking the index for drift, and enumerating what has changed since a point SHALL each be possible in cost proportional to what the operation touches. Nothing an append or a retraction rewrites SHALL grow with the workspace's history. A proposed layout or index shape that violates this SHALL be judged against it.

#### Scenario: Appending a claim
- **WHEN** a claim is asserted in a workspace holding a million objects
- **THEN** the files written or rewritten are the claim's own file and the index's current-month document, and nothing proportional to the million

#### Scenario: Reading the current month
- **WHEN** a consumer wants every object minted this month
- **THEN** it reads one directory per type and one index document, without parsing any sealed segment

#### Scenario: Enumerating changes since a point
- **WHEN** a remote consumer last read the workspace in a previous month
- **THEN** it can find every object minted since and every object retracted since by reading the root index and the segments it has not seen, and nothing it has

#### Scenario: Retracting in a workspace with many retractions
- **WHEN** an object is retracted in a workspace whose history holds fifty thousand retractions
- **THEN** the index documents rewritten are the root alone, and the root holds only the current month's retractions
### Requirement: Object files are sharded by the minting month of their id
In a `dkf/0.2` workspace, an object or record file SHALL be located at `<type-dir>/<YYYY-MM>/<id>.yaml`, where `<type-dir>` is the directory for the id's prefix (`particulars`, `claims`, `syntheses`, `merges`, `publishes`) and `<YYYY-MM>` is the calendar year and month, in UTC, of the minting instant encoded in the id's UUIDv7 timestamp. An id from which no month derives — one whose identifier part is not a UUID, or is a UUID of a version other than 7 — SHALL be located at `<type-dir>/legacy/<id>.yaml`. The path SHALL be derivable from the id alone: it SHALL NOT depend on any field of the file, on `dkf.yaml`, or on any lookup. Every type directory SHALL be sharded by the same rule. A month directory SHALL contain only files whose ids were minted in that month, and the `legacy` directory only files whose ids derive no month.

#### Scenario: Deriving a path
- **WHEN** a claim's id is `clm_01a0f3c1-4d20-7b8e-9a11-6c2f4e7d9b03` and its UUIDv7 timestamp falls on 2026-09-05T01:01:35Z
- **THEN** its file is `claims/2026-09/clm_01a0f3c1-4d20-7b8e-9a11-6c2f4e7d9b03.yaml`

#### Scenario: Assertion time does not move a file
- **WHEN** a claim carrying `timestamp: 2019-03-01T00:00:00Z` is minted in September 2026
- **THEN** its file is under `claims/2026-09/`, because the shard follows the id, not the assertion time

#### Scenario: Particulars are sharded like everything else
- **WHEN** a particular is defined in August 2026
- **THEN** its file is `particulars/2026-08/<id>.yaml`

#### Scenario: A file in the wrong month
- **WHEN** a validator finds `claims/2026-08/clm_X.yaml` and `clm_X`'s id was minted in September 2026
- **THEN** validation fails, naming the file and the month its id derives

#### Scenario: A draft-era id
- **WHEN** a `dkf/0.2` workspace holds a claim with id `clm_07m3zp9s2q1r4t8v`
- **THEN** its file is `claims/legacy/clm_07m3zp9s2q1r4t8v.yaml`, and a reader accepts it as `object-identifiers` requires

#### Scenario: A UUID that is not version 7
- **WHEN** an id's identifier part is a canonical UUID of version 4
- **THEN** no month derives from it and its file is under `<type-dir>/legacy/`

#### Scenario: A legacy id in a month directory
- **WHEN** a validator finds `claims/2026-08/clm_07m3zp9s2q1r4t8v.yaml`
- **THEN** validation fails, naming the file and `claims/legacy/` as its derived location
### Requirement: A sealed month gains no files
A month SHALL be sealed once any id in the workspace was minted two or more months after it; the current month and the month before it are open. An implementation SHALL NOT mint an id whose month is sealed, and SHALL NOT write a retraction whose `timestamp` falls in a sealed month; it mints and dates retractions at its own clock, and with a month of grace only a clock more than a month out can trip either guard. A file within a sealed month MAY change only by the single modification the format permits to any object file, the appending of a `retracted` block. A file arriving in a sealed month's directory by a merge — a branch open across two or more month boundaries — is a late merge: validation SHALL fail naming the file, and the remedy is to re-mint the branch's objects before merging. The specification SHALL state the git consequence as the benefit delivered rather than as a rule: an old month's tree object is rewritten only by a late merge or a retraction, never by an ordinary append. The `legacy` directory is not a month: it is never sealed, no conformant writer adds to it, and a rebuild that finds it changed reports the difference as drift.

#### Scenario: Retracting into a sealed month
- **WHEN** a claim under `claims/2026-08/` is retracted in November 2026
- **THEN** its file gains a `retracted` block and nothing else in `claims/2026-08/` changes

#### Scenario: A sealed directory in git
- **WHEN** objects are appended for a year after August 2026
- **THEN** no commit in that year rewrites the tree object for `claims/2026-08/` unless a file in it is retracted or a late merge adds one

#### Scenario: A retraction dated into a sealed month
- **WHEN** an implementation is asked in November 2026 to write a retraction with `timestamp` in August 2026, and the newest id is from November
- **THEN** it refuses, and the writer records the retraction with a current timestamp and a `reason` that says when it was decided

#### Scenario: The legacy directory is not sealed
- **WHEN** a file is copied into `claims/legacy/` after the workspace has objects minted in later months
- **THEN** no sealed-month rule is violated, and the next drift check reports the index as lagging

#### Scenario: A retraction dated into the future
- **WHEN** an implementation whose clock reads 2026-11-03 writes a retraction
- **THEN** it dates it 2026-11-03, its own clock, and the timestamp lands in an open month

#### Scenario: A branch open across one boundary
- **WHEN** a claim is minted on a branch on 28 November 2026 and merged on 5 December after main has minted in December
- **THEN** the file lands under `claims/2026-11/`, November is open, and validation passes

#### Scenario: A branch open across two boundaries
- **WHEN** a claim minted on a branch in August 2026 is merged in November 2026 after main has minted in October or later
- **THEN** the file lands under `claims/2026-08/`, which is sealed, and validation fails naming it as a late merge

#### Scenario: Clock skew at a month boundary
- **WHEN** a machine two days slow mints on what it believes is 30 November 2026 while the newest id is from 2 December
- **THEN** the id lands under `claims/2026-11/`, which is open, and nothing is refused

#### Scenario: A writer more than a month behind
- **WHEN** the newest id in the workspace is from December 2026 and a machine whose clock reads September 2026 tries to mint
- **THEN** it refuses, because September is sealed, and names the sealed month
### Requirement: A reader reads the layout its declared version names
A reader SHALL determine a workspace's layout from the `format` in its `dkf.yaml` and from the `format` of each index document it opens: `dkf/0.1` names the flat layout, in which every object file sits directly in its type directory and the index is a single document; `dkf/0.2` names the sharded layout defined here. A `dkf/0.2` reader SHALL read both. A reader SHALL NOT infer the layout from the directory contents.

#### Scenario: A flat workspace under a new reader
- **WHEN** a `dkf/0.2` implementation opens a workspace whose `dkf.yaml` says `format: dkf/0.1`
- **THEN** it reads `claims/*.yaml` and a single-document index, and every verb behaves as before

#### Scenario: Layout is not guessed
- **WHEN** a `dkf/0.2` workspace happens to contain a stray `claims/clm_X.yaml` at the top level
- **THEN** the reader does not treat it as an object, and validation reports the file as misplaced
### Requirement: Migration changes nothing an object asserts
Moving a workspace from `dkf/0.1` to `dkf/0.2` SHALL consist of relocating each object and record file to its derived path — a month directory, or `legacy` for an id from which no month derives — regenerating the index in the `dkf/0.2` shape, and rewriting `format` in `dkf.yaml`. No id, field, `source`, `retracted` block, or canonical payload SHALL change. Every signature valid before migration SHALL verify after it.

#### Scenario: Migrating the dogfood workspace
- **WHEN** a workspace with 163 claim files in `claims/` is migrated
- **THEN** each file is moved to `claims/<YYYY-MM>/` by its id, byte-identical, and the workspace validates under `dkf/0.2`

#### Scenario: Signatures survive
- **WHEN** a signed claim is migrated
- **THEN** its signature verifies against the moved file exactly as it did against the original

#### Scenario: Migration is optional
- **WHEN** a `dkf/0.1` workspace is never migrated
- **THEN** it remains valid, and a `dkf/0.2` reader reads it

#### Scenario: Migrating a workspace with a draft-era id
- **WHEN** a `dkf/0.1` workspace holding `claims/clm_07m3zp9s2q1r4t8v.yaml` is migrated
- **THEN** that file moves to `claims/legacy/`, its id unchanged, and the workspace validates under `dkf/0.2`

### Requirement: A validator warns on time it cannot have seen
A validator SHOULD report, as a warning naming the object, any id whose minting instant is later than the validator's own clock, and any object or retraction `timestamp` later than it; such a warning SHALL NOT fail validation, because a clock a few days fast at a month end is ordinary and the validator's clock may be the one that is wrong. A validator SHALL fail on an id whose month is two or more months later than the validator's current month. The uncertainty is the same in both cases — a validator two months slow cannot tell itself from an id two months fast — and the rule rests on the asymmetry of consequence, not of confidence: a validator whose own clock is two months slow fails a healthy workspace once, loudly, on a machine that is itself broken, and that is the better error, because the alternative is accepting an id that seals the month every correct writer is minting into, which cannot be undone. The specification SHALL state that an id can only be dated ahead by a clock, that every validator on a correctly set machine will therefore flag it, and that the place to catch it is a pull-request check before the object is merged.

#### Scenario: A future-dated retraction in a hand-edited file
- **WHEN** a claim file carries `retracted.timestamp: 2027-11-03T10:00:00Z` and the validator runs on 2026-11-04
- **THEN** validation warns naming the claim, and exits successfully if nothing else is wrong

#### Scenario: An id minted on a skewed clock
- **WHEN** an id's UUIDv7 timestamp is two days later than the validator's clock
- **THEN** validation warns naming the object, and the object's file is still expected at the month its id derives

#### Scenario: Honest time
- **WHEN** every id and timestamp in the workspace is at or before the validator's clock
- **THEN** nothing is reported

#### Scenario: An id one month ahead
- **WHEN** an id's month is the month after the validator's current month
- **THEN** validation warns and does not fail, because that month is the next open one and seals nothing

#### Scenario: A far-future id
- **WHEN** an id's month is two or more months after the validator's current month
- **THEN** validation fails naming the object, because the id would seal the month correct writers are minting into

#### Scenario: A far-future id caught at review
- **WHEN** a machine a year fast mints an object on a branch and opens a pull request, and the check runs `validate` on a correctly set machine
- **THEN** the check fails naming the object, and the object is not merged

#### Scenario: A validator two months slow
- **WHEN** a validator's own clock is two months behind and it checks a healthy workspace whose newest id is from the real current month
- **THEN** it fails naming that object, and the failure is the intended error: the machine running the validator is the one to fix
