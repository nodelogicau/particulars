## MODIFIED Requirements

### Requirement: Index entries carry a baseline and may be extended
Each entry SHALL carry `id` and `type`; particulars SHALL carry `uri`; claims and syntheses SHALL carry `subject`; syntheses SHALL carry `inputs`; claims that carry `basis` SHALL carry `basis`; merges SHALL carry `uris`; publishes SHALL carry `claims` and `scope`. Entries MAY additionally carry `scope`, `topics`, `timestamp`, `author`, and `document-author`, the last two mirroring the object's `source.author` and `source.document.author` as written. In a `dkf/0.1` index entries MAY additionally carry `retracted: true`, and readers of a `dkf/0.1` index SHALL honour it; in a `dkf/0.2` index entries SHALL NOT carry it, retraction being recorded in the root's `retracted` list. Implementations MAY add further fields, except that no field SHALL carry an embedding vector or any other value whose content depends on which model produced it; such values belong in an uncommitted cache as defined in `recall-query`. Future versions of this specification MAY add further entry types; consumers SHALL ignore fields and entries they do not understand. An implementation that rebuilds the index SHALL preserve entries whose `type` it does not recognise, unchanged and in their canonical order, and SHALL preserve, on entries it does regenerate, fields it does not recognise; a drift check SHALL NOT report such entries or fields as differences.

#### Scenario: Scope filtering from the index
- **WHEN** entries carry `scope` and `knowledge_recall` is called with `scope: public`
- **THEN** non-public entries are excluded without opening their files

#### Scenario: Author filtering from the index
- **WHEN** entries carry `author` and `document-author` and `knowledge_recall` is called with `author`
- **THEN** the candidate set is found from the index and the particular entries' `uri` values, without opening claim files

#### Scenario: Staleness from the index
- **WHEN** a claim entry carries `basis` and one of the listed objects is in the root's `retracted` list
- **THEN** a consumer can report the claim as `stale` without opening its file

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

#### Scenario: No embeddings in the index
- **WHEN** an implementation that keeps a semantic cache rebuilds the index
- **THEN** no entry carries an embedding vector or a model identifier, and the rebuilt index is identical to one written by an implementation with no cache
