## MODIFIED Requirements

### Requirement: The index is a hot tail, sealed segments, and a tombstone list
In a `dkf/0.2` workspace, `index.yaml` SHALL carry `format`, `segments` (a list of mappings, each with `path` relative to `index.yaml` and `count`, the number of entries in that segment: `index/legacy.yaml` first if it exists, then one per sealed month in ascending order), `entries` (the entries of objects minted in either open month), and `retracted` (the ids, sorted, of objects whose `retracted.timestamp` falls in either open month or any later month, whatever month they were minted in). The current month SHALL be the month of the newest id in the workspace; the open months SHALL be the current month and the month before it; a month SHALL be sealed once any id in the workspace was minted two or more months after it. Each sealed month's segment SHALL be at `index/<YYYY-MM>.yaml` and SHALL carry `format`, `entries` for objects minted in that month, and `retracted` for objects retracted in that month; its `count` in the root SHALL equal the number of its entries, which SHALL equal the number of files in that month's directories across every type. `index/legacy.yaml` SHALL carry `format` and `entries` for objects whose ids derive no month, and no `retracted`. A rebuild SHALL be a function of the files alone; a sealed month with retractions and no mints yields a segment with an empty `entries`, and a month with neither yields no segment. A sealed segment SHALL NOT change once written; `index/legacy.yaml` is not sealed and a change to it is drift. Entries SHALL NOT carry `retracted`; the per-month lists are the sole index record of retraction. Because an object cannot be retracted before it is minted, an object minted in month M is retracted if and only if its id appears in `retracted` of the root or of a segment for month M or later, a check whose cost is proportional to the months elapsed since M.

#### Scenario: Shape of the root index
- **WHEN** a workspace holds objects minted in August, September and October 2026, the newest id is from October, and one August object was retracted in September
- **THEN** `index.yaml` lists `index/2026-08.yaml` with its count under `segments`, carries September's and October's entries under `entries`, and its `retracted` names the August object

#### Scenario: Month rollover
- **WHEN** the first object of November 2026 is minted and the index is rebuilt
- **THEN** September's entries and September's retractions move into a new `index/2026-09.yaml`, `segments` gains its path and count, and the root holds October and November

#### Scenario: A rebuild is deterministic
- **WHEN** two implementations rebuild the index of the same files on different days
- **THEN** they produce the same root document and the same segments, because the open months follow the newest id and not the clock

#### Scenario: A retraction touches only the root
- **WHEN** a claim whose entry is in `index/2026-08.yaml` is retracted in October 2026
- **THEN** its id is added to `retracted` in `index.yaml`, `index/2026-08.yaml` is byte-identical to before, and the root holds only retractions dated in an open month or later

#### Scenario: Filtering retracted objects from the index
- **WHEN** `knowledge_recall` is called with `include_retracted: false` over objects minted in August 2026
- **THEN** retracted objects are excluded using the `retracted` lists of the root and of the segments for August and later, without opening files

#### Scenario: Filtering the current month
- **WHEN** `knowledge_recall` is called with `include_retracted: false` over objects minted in the current month
- **THEN** the root's `retracted` list alone decides

#### Scenario: A segment is a valid index document
- **WHEN** a tool that understands index entries opens `index/2026-08.yaml` on its own
- **THEN** it reads `format`, a list of entries, and a list of retracted ids in the shape defined by this specification, and nothing else

#### Scenario: A remote consumer caches sealed segments
- **WHEN** a consumer has fetched `index/2026-08.yaml` once and the workspace validates
- **THEN** it never needs to fetch it again, and learns of every later retraction from the root and from segments newer than August

#### Scenario: A month of retractions only
- **WHEN** objects are retracted in November 2026 and none are minted, and the index is rebuilt after a January 2027 mint
- **THEN** `index/2026-11.yaml` exists with an empty `entries` and November's `retracted`

#### Scenario: The legacy segment
- **WHEN** a workspace holds a claim with id `clm_07m3zp9s2q1r4t8v`
- **THEN** its entry is in `index/legacy.yaml`, which is the first path under `segments`, and if it is retracted its id is in the `retracted` list of the month of its retraction

#### Scenario: A branch merged across one month boundary
- **WHEN** a claim minted on a branch on 28 November 2026 is merged on 5 December, after main has minted in December
- **THEN** November is still open, the claim's entry goes into the root, and no segment changes

#### Scenario: A retraction dated ahead of the newest mint
- **WHEN** the newest id is from October 2026 and a retraction is dated in December 2026 by a writer whose clock is ahead
- **THEN** the root's `retracted` carries it, and it seals into `index/2026-12.yaml` only when an id is minted in February 2027 or later

### Requirement: Implementations provide rebuild and drift-check operations
Implementations SHALL provide an operation that regenerates the index from the files and an operation that reports, without modifying anything, whether the committed index differs from a regenerated one. In a `dkf/0.2` workspace the drift check SHALL first compare, for each sealed month, the number of files in that month's directories against the segment's recorded `count`, and SHALL parse a sealed segment only when they differ; a difference SHALL be reported as a late merge naming the files present in the directories and absent from the segment. It SHALL then compare each committed document whose count matched or which is open — the root, `index/legacy.yaml`, and any differing segment — against its regenerated counterpart, `entries` and `retracted` both. A drift check exists to report the index lagging changes to the workspace, and its tolerance follows from that: for a MAY field that mirrors an immutable property of the object — `scope`, `topics`, `timestamp`, `author`, `document-author` — a field present on one side and absent from the other SHALL NOT be reported, in either direction, because the object cannot have changed and the difference can only mean one writer predated the field. Retraction, the only mutable property, SHALL be compared through the `retracted` lists in a `dkf/0.2` index — an id present in one document's list and absent from the other's SHALL be reported — and through the entry field in a `dkf/0.1` index, compared as present with the meaning its absence carries, absent being `false`. A MAY field present on both sides with differing values, any missing or extra entry, and any missing or extra segment SHALL be reported.

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

#### Scenario: A retraction dated into a sealed month
- **WHEN** a file under `claims/2026-08/` carries a `retracted.timestamp` in August 2026 and the committed `index/2026-08.yaml` does not list it
- **THEN** the check reports the segment, and the retraction is treated as written in violation of the guard

#### Scenario: A late merge into a sealed month
- **WHEN** a branch open since August 2026 is merged in November 2026, adding `claims/2026-08/clm_X.yaml`, and `index/2026-08.yaml` records a count one less than the files now present
- **THEN** the count check reports a late merge naming `clm_X`, and validation fails
