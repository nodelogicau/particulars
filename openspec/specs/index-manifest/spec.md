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
Each entry SHALL carry `id` and `type`; particulars SHALL carry `uri`; claims and syntheses SHALL carry `subject`; syntheses SHALL carry `inputs`; merges SHALL carry `uris`. Entries MAY additionally carry `scope`, `topics`, `timestamp`, and `retracted: true`. Implementations MAY add further fields; consumers SHALL ignore fields they do not understand.

#### Scenario: Scope filtering from the index
- **WHEN** entries carry `scope` and `knowledge_recall` is called with `scope: public`
- **THEN** non-public entries are excluded without opening their files

#### Scenario: Unknown entry field
- **WHEN** an entry contains a field not listed in this specification
- **THEN** consumers ignore it

### Requirement: The index remains committed for remote consumers
Publishers SHALL commit `index.yaml` so that HTTP consumers, who cannot list directories, can enumerate a workspace. Remote consumers SHALL treat it as potentially lagging the object files.

#### Scenario: Fetching over HTTP
- **WHEN** a crawler reads `/knowledge/index.yaml` from a public publisher
- **THEN** it can enumerate every published object without directory listing

### Requirement: Implementations provide rebuild and drift-check operations
Implementations SHALL provide an operation that regenerates `index.yaml` from the files and an operation that reports, without modifying anything, whether the committed index differs from a regenerated one.

#### Scenario: CI drift check
- **WHEN** the drift check runs against a workspace whose index is stale
- **THEN** it exits non-zero and lists the differing entries
