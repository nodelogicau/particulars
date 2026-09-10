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
A month directory SHALL be sealed once any id in the workspace was minted in a later month. A sealed directory SHALL gain no files. A file within it MAY change only by the single modification the format permits to any object file, the appending of a `retracted` block. Implementations SHALL NOT mint an id whose month is earlier than that of the newest id in the workspace, and SHALL NOT write a retraction whose `timestamp` falls in a month earlier than that of the newest id in the workspace — the same bound, so that a write which passes its guard always has an unsealed home in the index. Implementations SHALL NOT write a retraction whose `timestamp` is later than the writer's own clock. The `legacy` directory is not a month: it is never sealed, no conformant writer adds to it, and a rebuild that finds it changed reports the difference as drift.

#### Scenario: Retracting into a sealed month
- **WHEN** a claim under `claims/2026-08/` is retracted in October 2026
- **THEN** its file gains a `retracted` block and nothing else in `claims/2026-08/` changes

#### Scenario: A sealed directory in git
- **WHEN** objects are appended for a year after August 2026
- **THEN** no commit in that year rewrites the tree object for `claims/2026-08/` unless a file in it is retracted

#### Scenario: A retraction dated into a sealed month
- **WHEN** an implementation is asked in October 2026 to write a retraction with `timestamp` in September 2026, and the newest id is from October
- **THEN** it refuses, and the writer records the retraction with a current timestamp and a `reason` that says when it was decided

#### Scenario: The legacy directory is not sealed
- **WHEN** a file is copied into `claims/legacy/` after the workspace has objects minted in later months
- **THEN** no sealed-month rule is violated, and the next drift check reports the index as lagging

#### Scenario: A retraction dated into the future
- **WHEN** an implementation whose clock reads 2026-11-03 is asked to write a retraction with `timestamp: 2027-11-03T10:00:00Z`
- **THEN** it refuses, naming the timestamp and its own clock

#### Scenario: A mint after a retraction dated ahead
- **WHEN** the newest id is from October 2026, a retraction has been dated in December 2026, and an implementation mints in November 2026
- **THEN** the mint is permitted, because the bound is the newest id's month and not the retraction's
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
A validator SHOULD report, as a warning naming the object, any id whose minting instant is later than the validator's own clock, and any object or retraction `timestamp` later than it. The warning SHALL NOT fail validation: the validator's clock may be the one that is wrong, and under the single sealing clock a future-dated object still has exactly one derived home.

#### Scenario: A future-dated retraction in a hand-edited file
- **WHEN** a claim file carries `retracted.timestamp: 2027-11-03T10:00:00Z` and the validator runs on 2026-11-04
- **THEN** validation warns naming the claim, and exits successfully if nothing else is wrong

#### Scenario: An id minted on a skewed clock
- **WHEN** an id's UUIDv7 timestamp is two days later than the validator's clock
- **THEN** validation warns naming the object, and the object's file is still expected at the month its id derives

#### Scenario: Honest time
- **WHEN** every id and timestamp in the workspace is at or before the validator's clock
- **THEN** nothing is reported
