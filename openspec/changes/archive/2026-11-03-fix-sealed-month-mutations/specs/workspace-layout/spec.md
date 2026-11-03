## MODIFIED Requirements

### Requirement: Object files are sharded by the minting month of their id
In a `dkf/0.2` workspace, an object or record file SHALL be located at `<type-dir>/<YYYY-MM>/<id>.yaml`, where `<type-dir>` is the directory for the id's prefix (`particulars`, `claims`, `syntheses`, `merges`, `publishes`) and `<YYYY-MM>` is the calendar year and month, in UTC, of the minting instant encoded in the id's UUIDv7 timestamp. An id from which no month derives — one whose identifier part is not a UUID, or is a UUID of a version other than 7 — SHALL be located at `<type-dir>/legacy/<id>.yaml`. The path SHALL be derivable from the id alone: it SHALL NOT depend on any field of the file, on `dkf.yaml`, or on any lookup. Every type directory SHALL be sharded by the same rule. A month directory SHALL contain only files whose ids were minted in that month, and the `legacy` directory only files whose ids derive no month.

#### Scenario: Deriving a path
- **WHEN** a claim's id is `clm_01a0f3c1-4d20-7b8e-9a11-6c2f4e7d9b03` and its UUIDv7 timestamp, the first 48 bits `01a0f3c14d20`, is 1790795926816 ms, which is 2026-09-30T19:18:46.816Z
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
A month SHALL be sealed once any id in the workspace was minted two or more months after it; the current month and the month before it are open. An implementation SHALL NOT mint an id whose month is sealed, and SHALL NOT write a retraction whose `timestamp` falls in a sealed month; it mints and dates retractions at its own clock, and with a month of grace only a clock more than a month out can trip either guard. A file within a sealed month MAY change only by one of these modifications, which are every modification the format permits to an existing file: the appending of a `retracted` block (`retraction`); the adding or extending of a `redacted` block, with the removal of the fields it lists (`redaction`, `dkf/0.3` only); and the updating of a particular's `label` or `aliases` by `particular_define`, which SHALL NOT change its `id`, `type` or `uri`. None of these changes an index entry, a segment, or a segment's `count`, so none rewrites a sealed segment. A file arriving in a sealed month's directory by a merge — a branch open across two or more month boundaries — is a late merge: validation SHALL fail naming the file, and the remedy is to re-mint the branch's objects before merging. The specification SHALL state the git consequence as the benefit delivered rather than as a rule: an old month's tree object is rewritten only by a late merge, a retraction, a redaction, or an update to a particular's label or aliases, never by an ordinary append. The `legacy` directory is not a month: it is never sealed, no conformant writer adds to it, and a rebuild that finds it changed reports the difference as drift.

#### Scenario: Retracting into a sealed month
- **WHEN** a claim under `claims/2026-08/` is retracted in November 2026
- **THEN** its file gains a `retracted` block and nothing else in `claims/2026-08/` changes

#### Scenario: Adding an alias to a particular in a sealed month
- **WHEN** `particular_define` adds an alias to a particular under `particulars/2026-08/` in November 2026
- **THEN** the particular's file gains the alias, its `id`, `type` and `uri` are unchanged, no index document changes, and validation passes

#### Scenario: Redacting into a sealed month
- **WHEN** a claim under `claims/2026-08/` in a `dkf/0.3` workspace has its `source.document.quote` redacted in November 2026
- **THEN** its file loses the quote and gains a `redacted` block dated November, and nothing else in `claims/2026-08/` changes

#### Scenario: Any other change to a sealed-month file
- **WHEN** a claim's `content` under `claims/2026-08/` is rewritten in place
- **THEN** it is not a permitted modification, as it would not be in an open month, and the sealed month grants no further exception

#### Scenario: A sealed directory in git
- **WHEN** objects are appended for a year after August 2026
- **THEN** no commit in that year rewrites the tree object for `claims/2026-08/` unless a file in it is retracted or redacted or a late merge adds one

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
