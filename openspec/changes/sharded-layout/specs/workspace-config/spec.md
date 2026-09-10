## MODIFIED Requirements

### Requirement: `dkf.yaml` marks and configures a workspace
A DKF workspace SHALL be identified by a `dkf.yaml` file at its root containing at minimum `format` and `workspace.id` (a bare lowercase UUIDv7). `format` SHALL be `dkf/0.1`, naming the flat layout, or `dkf/0.2`, naming the sharded layout defined in `workspace-layout`. A reader SHALL refuse to open a workspace whose `format` names a version it does not implement, and SHALL report the version it found; it SHALL NOT open the workspace and read what it can. It MAY contain `workspace.base-uri` (which, if present, SHALL end in `/`), `workspace.conventions` (a relative path inside the workspace naming the conventions document defined in `agent-guidance`), and a `defaults` block with `scope` and `source`. Implementations SHALL ignore unknown keys. The validity of `workspace.conventions` SHALL be checked lexically on the cleaned path: an absolute path, or one whose first segment is `..`, is invalid. An invalid value SHALL be treated as if the key were absent and reported as a warning; it SHALL NOT make the workspace invalid.

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

#### Scenario: A `dkf/0.2` workspace
- **WHEN** `dkf.yaml` says `format: dkf/0.2` and the reader implements it
- **THEN** the workspace opens with the sharded layout

#### Scenario: A version the reader does not implement
- **WHEN** `dkf.yaml` says `format: dkf/0.3` and the reader implements only `dkf/0.1` and `dkf/0.2`
- **THEN** the reader refuses to open the workspace and its error names `dkf/0.3`

#### Scenario: A `dkf/0.1` workspace remains valid
- **WHEN** `dkf.yaml` says `format: dkf/0.1`
- **THEN** a reader implementing `dkf/0.2` opens it with the flat layout, and nothing requires it to migrate
