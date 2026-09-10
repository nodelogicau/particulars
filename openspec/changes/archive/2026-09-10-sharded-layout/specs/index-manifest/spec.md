## ADDED Requirements

### Requirement: The index is a hot tail, sealed segments, and a tombstone list
In a `dkf/0.2` workspace, `index.yaml` SHALL carry `format`, `segments` (a list of paths, relative to `index.yaml`, one per sealed month in ascending order), `entries` (the entries for the current month only), and `retracted` (the ids of every retracted object in the workspace, sorted, whether their entries are in the tail or in a segment). Each segment SHALL be at `index/<YYYY-MM>.yaml` and SHALL carry `format` and `entries` for that month only. The current month SHALL be the month of the newest id in the workspace, so that a rebuild is a function of the files alone. A sealed segment SHALL NOT change once written. Entries SHALL NOT carry `retracted`; the tombstone list is the sole index record of retraction.

#### Scenario: Shape of the root index
- **WHEN** a workspace holds objects minted in August and September 2026 and the newest id is from September
- **THEN** `index.yaml` lists `index/2026-08.yaml` under `segments`, carries September's entries under `entries`, and its `retracted` list names every retracted id

#### Scenario: Month rollover
- **WHEN** the first object of October 2026 is minted and the index is rebuilt
- **THEN** September's entries move into a new `index/2026-09.yaml`, `segments` gains that path, and `entries` holds only October

#### Scenario: A rebuild is deterministic
- **WHEN** two implementations rebuild the index of the same files on different days
- **THEN** they produce the same root document and the same segments, because the current month follows the newest id and not the clock

#### Scenario: A retraction touches only the root
- **WHEN** a claim whose entry is in `index/2026-08.yaml` is retracted
- **THEN** its id is added to `retracted` in `index.yaml` and `index/2026-08.yaml` is byte-identical to before

#### Scenario: Filtering retracted objects from the index
- **WHEN** `knowledge_recall` is called with `include_retracted: false`
- **THEN** retracted objects are excluded using the `retracted` list alone, without opening files

#### Scenario: A segment is a valid index document
- **WHEN** a tool that understands index entries opens `index/2026-08.yaml` on its own
- **THEN** it reads `format` and a list of entries in the shape defined by this specification, and nothing else

#### Scenario: A remote consumer caches sealed segments
- **WHEN** a consumer has fetched `index/2026-08.yaml` once
- **THEN** it never needs to fetch it again, and learns of later retractions from the root's `retracted` list

## MODIFIED Requirements

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

### Requirement: Implementations provide rebuild and drift-check operations
Implementations SHALL provide an operation that regenerates the index from the files and an operation that reports, without modifying anything, whether the committed index differs from a regenerated one. In a `dkf/0.2` workspace the drift check SHALL compare each committed document — the root's `entries`, each segment, and the root's `retracted` list — against its regenerated counterpart. A drift check exists to report the index lagging changes to the workspace, and its tolerance follows from that: for a MAY field that mirrors an immutable property of the object — `scope`, `topics`, `timestamp`, `author`, `document-author` — a field present on one side and absent from the other SHALL NOT be reported, in either direction, because the object cannot have changed and the difference can only mean one writer predated the field. Retraction, the only mutable property, SHALL be compared through the `retracted` list in a `dkf/0.2` index — an id present in one list and absent from the other SHALL be reported — and through the entry field in a `dkf/0.1` index, compared as present with the meaning its absence carries, absent being `false`. A MAY field present on both sides with differing values, any missing or extra entry, and any missing or extra segment SHALL be reported.

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
- **WHEN** an object is retracted after the root index was committed, so the regenerated `retracted` list carries an id the committed one lacks
- **THEN** the check reports the id, because the object was retracted after the index was committed

#### Scenario: A workspace's first retraction
- **WHEN** the committed `retracted` list is empty and one object is then retracted
- **THEN** the check reports that id, regardless of how many entries exist

#### Scenario: A MAY field that changed
- **WHEN** a committed entry carries `scope: personal` and the regenerated entry carries `scope: organisation`
- **THEN** the check reports the entry, because the field is present on both sides and differs

#### Scenario: A sealed segment is unchanged
- **WHEN** objects are appended in October 2026 and the check runs
- **THEN** `index/2026-08.yaml` compares equal without being regenerated from more than its month's files

#### Scenario: A missing segment
- **WHEN** the root lists `index/2026-08.yaml` under `segments` and the file is absent
- **THEN** the check reports the segment
