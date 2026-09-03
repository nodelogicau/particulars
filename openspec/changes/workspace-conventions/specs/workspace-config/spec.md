## MODIFIED Requirements

### Requirement: `dkf.yaml` marks and configures a workspace
A DKF workspace SHALL be identified by a `dkf.yaml` file at its root containing at minimum `format: dkf/0.1` and `workspace.id` (a bare lowercase UUIDv7). It MAY contain `workspace.base-uri` (which, if present, SHALL end in `/`), `workspace.conventions` (a relative path inside the workspace naming the conventions document defined in `agent-guidance`), and a `defaults` block with `scope` and `source`. Implementations SHALL ignore unknown keys. The validity of `workspace.conventions` SHALL be checked lexically on the cleaned path: an absolute path, or one whose first segment is `..`, is invalid. An invalid value SHALL be treated as if the key were absent and reported as a warning; it SHALL NOT make the workspace invalid.

#### Scenario: Minimal workspace file
- **WHEN** `dkf.yaml` contains only `format` and `workspace.id`
- **THEN** the workspace is valid

#### Scenario: Unknown keys
- **WHEN** `dkf.yaml` contains a key not defined by this specification
- **THEN** the implementation ignores it without error

#### Scenario: Base URI without trailing slash
- **WHEN** `workspace.base-uri` does not end in `/`
- **THEN** validation fails

#### Scenario: Conventions path inside the workspace
- **WHEN** `workspace.conventions` is `docs/TOPICS.md`
- **THEN** the workspace is valid and `<root>/docs/TOPICS.md` is its conventions document

#### Scenario: Conventions path escaping the workspace
- **WHEN** `workspace.conventions` is `../secrets.md` or `/etc/motd`
- **THEN** the workspace is valid, the key is treated as absent, and the implementation warns naming the value

#### Scenario: An older reader and a newer reader agree
- **WHEN** `workspace.conventions` is invalid and the workspace is opened by an implementation that predates the key and by one that implements it
- **THEN** both open the workspace
