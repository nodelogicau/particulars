## MODIFIED Requirements

### Requirement: Index entries carry a baseline and may be extended
Each entry SHALL carry `id` and `type`; particulars SHALL carry `uri`; claims and syntheses SHALL carry `subject`; syntheses SHALL carry `inputs`; merges SHALL carry `uris`; publishes SHALL carry `claims` and `scope`. Entries MAY additionally carry `scope`, `topics`, `timestamp`, `retracted: true`, `author`, and `document-author`, the last two mirroring the object's `source.author` and `source.document.author` as written. Implementations MAY add further fields, and future versions of this specification MAY add further entry types; consumers SHALL ignore fields and entries they do not understand. An implementation that rebuilds the index SHALL preserve entries whose `type` it does not recognise, unchanged and in their canonical order, and SHALL preserve, on entries it does regenerate, fields it does not recognise; a drift check SHALL NOT report such entries or fields as differences.

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

### Requirement: Implementations provide rebuild and drift-check operations
Implementations SHALL provide an operation that regenerates `index.yaml` from the files and an operation that reports, without modifying anything, whether the committed index differs from a regenerated one. A drift check exists to report the index lagging changes to the workspace, and its tolerance follows from that: for a MAY field that mirrors an immutable property of the object — `scope`, `topics`, `timestamp`, `author`, `document-author` — a field present on one side and absent from the other SHALL NOT be reported, in either direction, because the object cannot have changed and the difference can only mean one writer predated the field. A MAY field that mirrors a mutable property — `retracted`, the only one — SHALL be compared as present with the meaning its absence carries, absent being `false`. A MAY field present on both sides with differing values, and any missing or extra entry, SHALL be reported.

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
- **WHEN** a committed entry carries no `retracted` field and the regenerated entry carries `retracted: true`
- **THEN** the check reports the entry, because the object was retracted after the index was committed

#### Scenario: A workspace's first retraction
- **WHEN** no committed entry carries `retracted` and one object is then retracted
- **THEN** the check reports that entry, regardless of how many entries lack the field

#### Scenario: A MAY field that changed
- **WHEN** a committed entry carries `scope: personal` and the regenerated entry carries `scope: organisation`
- **THEN** the check reports the entry, because the field is present on both sides and differs
