# Workspace Layout Specification

## Purpose

Defines the bounded-working-set principle, the `dkf/0.2` sharded directory layout and the derivation of a file's path from its id, the format-version gate that makes a change of shape safe, and migration from the flat `dkf/0.1` layout.

## Requirements

### Requirement: The cost of an operation is bounded by its working set
The specification SHALL state that a workspace's history is unbounded and that no operation it defines SHALL require reading data in proportion to that history when the operation concerns a bounded part of it. In particular, reading the objects of a bounded period, appending an object, checking the index for drift, and enumerating what has changed since a point SHALL each be possible in cost proportional to what the operation touches. A proposed layout or index shape that violates this SHALL be judged against it.

#### Scenario: Appending a claim
- **WHEN** a claim is asserted in a workspace holding a million objects
- **THEN** the files written or rewritten are the claim's own file and the index's current-month document, and nothing proportional to the million

#### Scenario: Reading the current month
- **WHEN** a consumer wants every object minted this month
- **THEN** it reads one directory per type and one index document, without parsing any sealed segment

#### Scenario: Enumerating changes since a point
- **WHEN** a remote consumer last read the workspace in a previous month
- **THEN** it can find every object minted since by reading the root index and the segments it has not seen, and nothing it has

### Requirement: Object files are sharded by the minting month of their id
In a `dkf/0.2` workspace, an object or record file SHALL be located at `<type-dir>/<YYYY-MM>/<id>.yaml`, where `<type-dir>` is the directory for the id's prefix (`particulars`, `claims`, `syntheses`, `merges`, `publishes`) and `<YYYY-MM>` is the calendar year and month, in UTC, of the minting instant encoded in the id's UUIDv7 timestamp. The path SHALL be derivable from the id alone: it SHALL NOT depend on any field of the file, on `dkf.yaml`, or on any lookup. Every type directory SHALL be sharded by the same rule. A month directory SHALL contain only files whose ids were minted in that month.

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

### Requirement: A sealed month gains no files
A month directory SHALL be sealed once any id in the workspace was minted in a later month. A sealed directory SHALL gain no files. A file within it MAY change only by the single modification the format permits to any object file, the appending of a `retracted` block. Implementations SHALL NOT mint an id whose month is earlier than that of the newest id in the workspace.

#### Scenario: Retracting into a sealed month
- **WHEN** a claim under `claims/2026-08/` is retracted in October 2026
- **THEN** its file gains a `retracted` block and nothing else in `claims/2026-08/` changes

#### Scenario: A sealed directory in git
- **WHEN** objects are appended for a year after August 2026
- **THEN** no commit in that year rewrites the tree object for `claims/2026-08/` unless a file in it is retracted

### Requirement: A reader reads the layout its declared version names
A reader SHALL determine a workspace's layout from the `format` in its `dkf.yaml` and from the `format` of each index document it opens: `dkf/0.1` names the flat layout, in which every object file sits directly in its type directory and the index is a single document; `dkf/0.2` names the sharded layout defined here. A `dkf/0.2` reader SHALL read both. A reader SHALL NOT infer the layout from the directory contents.

#### Scenario: A flat workspace under a new reader
- **WHEN** a `dkf/0.2` implementation opens a workspace whose `dkf.yaml` says `format: dkf/0.1`
- **THEN** it reads `claims/*.yaml` and a single-document index, and every verb behaves as before

#### Scenario: Layout is not guessed
- **WHEN** a `dkf/0.2` workspace happens to contain a stray `claims/clm_X.yaml` at the top level
- **THEN** the reader does not treat it as an object, and validation reports the file as misplaced

### Requirement: Migration changes nothing an object asserts
Moving a workspace from `dkf/0.1` to `dkf/0.2` SHALL consist of relocating each object and record file to its derived path, regenerating the index in the `dkf/0.2` shape, and rewriting `format` in `dkf.yaml`. No id, field, `source`, `retracted` block, or canonical payload SHALL change. Every signature valid before migration SHALL verify after it.

#### Scenario: Migrating the dogfood workspace
- **WHEN** a workspace with 163 claim files in `claims/` is migrated
- **THEN** each file is moved to `claims/<YYYY-MM>/` by its id, byte-identical, and the workspace validates under `dkf/0.2`

#### Scenario: Signatures survive
- **WHEN** a signed claim is migrated
- **THEN** its signature verifies against the moved file exactly as it did against the original

#### Scenario: Migration is optional
- **WHEN** a `dkf/0.1` workspace is never migrated
- **THEN** it remains valid, and a `dkf/0.2` reader reads it
