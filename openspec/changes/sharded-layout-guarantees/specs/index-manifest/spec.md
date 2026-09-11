## MODIFIED Requirements

### Requirement: Implementations provide rebuild and drift-check operations
Implementations SHALL provide an operation that regenerates the index from the files and an operation that reports, without modifying anything, whether the committed index differs from a regenerated one. In a `dkf/0.2` workspace the drift check SHALL first compare, for each sealed month, the number of files in that month's directories against the segment's recorded `count`, and SHALL parse a sealed segment only when they differ; a difference SHALL be reported as a late merge naming the files present in the directories and absent from the segment. A matching count guarantees that no file arrived in that month since the segment was written, and nothing more: the drift check SHALL NOT be relied on to detect a retraction dated into a sealed month, which validation detects. It SHALL then compare each committed document whose count matched or which is open — the root, `index/legacy.yaml`, and any differing segment — against its regenerated counterpart, `entries` and `retracted` both. A drift check exists to report the index lagging changes to the workspace, and its tolerance follows from that: for a MAY field that mirrors an immutable property of the object — `scope`, `topics`, `timestamp`, `author`, `document-author` — a field present on one side and absent from the other SHALL NOT be reported, in either direction, because the object cannot have changed and the difference can only mean one writer predated the field. Retraction, the only mutable property, SHALL be compared through the `retracted` lists in a `dkf/0.2` index — an id present in one document's list and absent from the other's SHALL be reported — and through the entry field in a `dkf/0.1` index, compared as present with the meaning its absence carries, absent being `false`. A MAY field present on both sides with differing values, any missing or extra entry, and any missing or extra segment SHALL be reported.

#### Scenario: CI drift check
- **WHEN** the drift check runs against a workspace whose index is stale
- **THEN** it exits non-zero and lists the differing entries

#### Scenario: A newer implementation against an older index
- **WHEN** an implementation that writes `author` into entries checks an index committed before that field existed, and nothing else differs
- **THEN** the check passes

#### Scenario: An older implementation against a newer index
- **WHEN** an implementation that does not write `author` checks an index whose entries carry it, and nothing else differs
- **THEN** the check passes

#### Scenario: A retraction after the index was committed
- **WHEN** an object is retracted after the root index was committed, so the regenerated root's `retracted` carries an id the committed one lacks
- **THEN** the check reports the id, because the object was retracted after the index was committed

#### Scenario: A workspace's first retraction
- **WHEN** no committed document carries a `retracted` id and one object is then retracted
- **THEN** the check reports that id, regardless of how many entries exist

#### Scenario: A MAY field that changed
- **WHEN** a committed entry carries `scope: personal` and the regenerated entry carries `scope: organisation`
- **THEN** the check reports the entry, because the field is present on both sides and differs

#### Scenario: A sealed segment is unchanged
- **WHEN** objects are appended and retracted in October 2026 and the check runs
- **THEN** `index/2026-08.yaml` compares equal by its count, without being parsed

#### Scenario: A missing segment
- **WHEN** the root lists `index/2026-08.yaml` under `segments` and the file is absent
- **THEN** the check reports the segment

#### Scenario: A late merge into a sealed month
- **WHEN** a branch open since August 2026 is merged in November 2026, adding `claims/2026-08/clm_X.yaml`, and `index/2026-08.yaml` records a count one less than the files now present
- **THEN** the count check reports a late merge naming `clm_X`, and validation fails

#### Scenario: The drift check does not see a sealed-month retraction
- **WHEN** a file under `claims/2026-08/` gains a `retracted` block dated in August 2026, August is sealed, and its file count is unchanged
- **THEN** the drift check compares `index/2026-08.yaml` by count and reports nothing, and the specification says validation is where this is caught

## ADDED Requirements

### Requirement: Validation compares sealed segments against the files
Because validation reads every object file, in a `dkf/0.2` workspace it SHALL regenerate each sealed month's `retracted` list from the files and compare it with the committed segment's list, and SHALL report an id present in one and absent from the other, naming the object and the segment. A retraction whose `timestamp` falls in a sealed month — whether written in violation of the guard or merged from a branch open across two or more boundaries — is a validation failure. Validation SHALL also perform the drift check's count comparison. The specification SHALL state that "a workspace that validates" therefore means one in which no sealed segment has gained a mint or a retraction since it was written, which is the condition under which a remote consumer may cache a sealed segment indefinitely.

#### Scenario: A retraction dated into a sealed month
- **WHEN** a file under `claims/2026-08/` carries a `retracted.timestamp` in August 2026, August is sealed, and the committed `index/2026-08.yaml` does not list it
- **THEN** validation fails naming the object and the segment, and the retraction is treated as written in violation of the guard

#### Scenario: A late-merge retraction
- **WHEN** a branch open since August 2026 retracts an object with a `timestamp` in August and merges in November 2026, after August has sealed
- **THEN** the file count is unchanged, the drift check reports nothing, and validation fails naming the object and `index/2026-08.yaml`

#### Scenario: A sealed segment's retractions match
- **WHEN** every retraction dated in August 2026 is listed in the committed `index/2026-08.yaml`
- **THEN** validation reports nothing for that segment

#### Scenario: What "validates" promises a consumer
- **WHEN** a remote consumer asks whether it may cache `index/2026-08.yaml` indefinitely
- **THEN** the answer is yes for a workspace that validates, because validation has checked both that no file arrived in August and that no retraction was dated into it
