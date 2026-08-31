## MODIFIED Requirements

### Requirement: Implementations provide rebuild and drift-check operations
Implementations SHALL provide an operation that regenerates `index.yaml` from the files and an operation that reports, without modifying anything, whether the committed index differs from a regenerated one. The drift check SHALL NOT report, as a difference, a field this specification marks as MAY that is absent from an entry in the committed index; a MAY field present on both sides with differing values, and any missing or extra entry, SHALL still be reported.

#### Scenario: CI drift check
- **WHEN** the drift check runs against a workspace whose index is stale
- **THEN** it exits non-zero and lists the differing entries

#### Scenario: A newer implementation against an older index
- **WHEN** an implementation that writes `author` into entries checks an index committed before that field existed, and nothing else differs
- **THEN** the check passes

#### Scenario: A MAY field that changed
- **WHEN** a committed entry carries `scope: personal` and the regenerated entry carries `scope: organisation`
- **THEN** the check reports the entry, because the field is present on both sides and differs
