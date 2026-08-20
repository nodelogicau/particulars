## ADDED Requirements

### Requirement: `dkf.yaml` marks and configures a workspace
A DKF workspace SHALL be identified by a `dkf.yaml` file at its root containing at minimum `format: dkf/0.1` and `workspace.id` (a bare lowercase UUIDv7). It MAY contain `workspace.base-uri` (which, if present, SHALL end in `/`) and a `defaults` block with `scope` and `source`. Implementations SHALL ignore unknown keys.

#### Scenario: Minimal workspace file
- **WHEN** `dkf.yaml` contains only `format` and `workspace.id`
- **THEN** the workspace is valid

#### Scenario: Unknown keys
- **WHEN** `dkf.yaml` contains a key not defined by this specification
- **THEN** the implementation ignores it without error

#### Scenario: Base URI without trailing slash
- **WHEN** `workspace.base-uri` does not end in `/`
- **THEN** validation fails

### Requirement: Workspace discovery walks up from the working directory
Implementations SHALL locate the workspace by searching the current directory and each ancestor for `dkf.yaml`, using the first found.

#### Scenario: Invoked from a subdirectory
- **WHEN** a tool runs in `<root>/claims/` and `<root>/dkf.yaml` exists
- **THEN** `<root>` is used as the workspace

### Requirement: Defaults are applied by writers only
Values in `defaults` SHALL be applied when a write operation omits the corresponding value (`scope` when `context.scope` is not supplied; `source` fields when `source` is incomplete). Readers SHALL NOT consult `defaults` when interpreting an object file.

#### Scenario: Asserting a claim without a source
- **WHEN** `claim_assert` is called with no `source` and `defaults.source.author` is `ben`
- **THEN** the written claim file contains `source.author: ben`

#### Scenario: Reading never depends on config
- **WHEN** an object file is read in a workspace whose `dkf.yaml` is absent
- **THEN** its scope and source are taken from the file alone
