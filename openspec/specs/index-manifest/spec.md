# Index Manifest Specification

## Purpose

Defines `index.yaml` as a derived, regenerable cache of the object files: its baseline and optional entry fields, how local and remote consumers must treat it, and the rebuild and drift-check operations implementations provide.

## Requirements

### Requirement: The index is a derived, regenerable cache
The object and record YAML files SHALL be the source of truth. `index.yaml` SHALL be fully reconstructible from them and SHALL never be treated as authoritative by a local consumer. A local consumer SHALL NOT return incorrect results because the index is missing or stale; it MAY be slower.

#### Scenario: Missing index
- **WHEN** `knowledge_recall` runs in a workspace with no `index.yaml`
- **THEN** it returns the same results as with a fresh index, by reading object files

#### Scenario: Conflicting index after a git merge
- **WHEN** two branches each added a claim and `index.yaml` conflicts on merge
- **THEN** the conflict is resolved by regenerating the index, with no hand-editing

### Requirement: Index entries carry a baseline and may be extended
Each entry SHALL carry `id` and `type`; particulars SHALL carry `uri`; claims and syntheses SHALL carry `subject`; syntheses SHALL carry `inputs`; merges SHALL carry `uris`; publishes SHALL carry `claims` and `scope`. Entries MAY additionally carry `scope`, `topics`, `timestamp`, `author`, and `document-author`, the last two mirroring the object's `source.author` and `source.document.author` as written. In a `dkf/0.1` index entries MAY additionally carry `retracted: true`, and readers of a `dkf/0.1` index SHALL honour it; in a `dkf/0.2` index entries SHALL NOT carry it, retraction being recorded in the root's `retracted` list. Implementations MAY add further fields, and future versions of this specification MAY add further entry types; consumers SHALL ignore fields and entries they do not understand. An implementation that rebuilds the index SHALL preserve entries whose `type` it does not recognise, unchanged and in their canonical order, and SHALL preserve, on entries it does regenerate, fields it does not recognise; a drift check SHALL NOT report such entries or fields as differences.

#### Scenario: Scope filtering from the index
- **WHEN** entries carry `scope` and `knowledge_recall` is called with `scope: public`
- **THEN** non-public entries are excluded without opening their files

#### Scenario: Author filtering from the index
- **WHEN** entries carry `author` and `document-author` and `knowledge_recall` is called with `author`
- **THEN** the candidate set is found from the index and the particular entries' `uri` values, without opening claim files

#### Scenario: Unknown entry field
- **WHEN** an entry contains a field not listed in this specification
- **THEN** consumers ignore it

#### Scenario: Unknown entry type survives a rebuild
- **WHEN** an implementation that predates promotion records rebuilds the index of a workspace containing `type: publish` entries
- **THEN** the rebuilt index still contains those entries unchanged

#### Scenario: Unknown entry field survives a rebuild
- **WHEN** an implementation that predates the `author` entry field rebuilds an index whose entries carry it
- **THEN** the rebuilt entries still carry `author` with its committed values

#### Scenario: Drift check across a version boundary
- **WHEN** an older implementation runs a drift check against an index containing entry types it does not recognise
- **THEN** the check does not report those entries as drift, and a workspace written by a newer conforming implementation passes

#### Scenario: Effective scope from the index
- **WHEN** a feed generator reads the index of a workspace containing promotion records
- **THEN** it can compute effective scope from the claim entries and the publish entries without opening every file

#### Scenario: A `dkf/0.1` entry flagged retracted
- **WHEN** a `dkf/0.2` reader opens a `dkf/0.1` index whose entry carries `retracted: true`
- **THEN** it treats the object as retracted, exactly as a `dkf/0.1` reader would
### Requirement: The index remains committed for remote consumers
Publishers SHALL commit `index.yaml` so that HTTP consumers, who cannot list directories, can enumerate a workspace. Remote consumers SHALL treat it as potentially lagging the object files.

#### Scenario: Fetching over HTTP
- **WHEN** a crawler reads `/knowledge/index.yaml` from a public publisher
- **THEN** it can enumerate every published object without directory listing

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
