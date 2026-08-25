## MODIFIED Requirements

### Requirement: Index entries carry a baseline and may be extended
Each entry SHALL carry `id` and `type`; particulars SHALL carry `uri`; claims and syntheses SHALL carry `subject`; syntheses SHALL carry `inputs`; merges SHALL carry `uris`; publishes SHALL carry `claims` and `scope`. Entries MAY additionally carry `scope`, `topics`, `timestamp`, and `retracted: true`. Implementations MAY add further fields, and future versions of this specification MAY add further entry types; consumers SHALL ignore fields and entries they do not understand. An implementation that rebuilds the index SHALL preserve entries whose `type` it does not recognise, unchanged and in their canonical order, and a drift check SHALL NOT report such entries as differences.

#### Scenario: Scope filtering from the index
- **WHEN** entries carry `scope` and `knowledge_recall` is called with `scope: public`
- **THEN** non-public entries are excluded without opening their files

#### Scenario: Unknown entry field
- **WHEN** an entry contains a field not listed in this specification
- **THEN** consumers ignore it

#### Scenario: Unknown entry type survives a rebuild
- **WHEN** an implementation that predates promotion records rebuilds the index of a workspace containing `type: publish` entries
- **THEN** the rebuilt index still contains those entries unchanged

#### Scenario: Drift check across a version boundary
- **WHEN** an older implementation runs a drift check against an index containing entry types it does not recognise
- **THEN** the check does not report those entries as drift, and a workspace written by a newer conforming implementation passes

#### Scenario: Effective scope from the index
- **WHEN** a feed generator reads the index of a workspace containing promotion records
- **THEN** it can compute effective scope from the claim entries and the publish entries without opening every file
