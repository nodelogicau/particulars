# Workspace Configuration Specification

## Purpose

Defines `dkf.yaml`, the file that marks a DKF workspace root and carries its identity, optional base URI, and writer-side defaults, together with how implementations discover it.

## Requirements

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

### Requirement: Workspace discovery walks up from the working directory
Implementations SHALL locate the workspace by searching the current directory and each ancestor. At each directory, a `dkf.yaml` SHALL make that directory the workspace; otherwise a `.dkf` pointer file, if present, SHALL redirect to the workspace it names. Explicit configuration — a workspace argument, then an environment variable — SHALL take precedence over discovery entirely.

#### Scenario: Invoked from a subdirectory
- **WHEN** a tool runs in `<root>/claims/` and `<root>/dkf.yaml` exists
- **THEN** `<root>` is used as the workspace

#### Scenario: Explicit configuration wins
- **WHEN** a tool is given an explicit workspace path and the working directory is inside a different workspace
- **THEN** the explicit path is used

### Requirement: Defaults are applied by writers only
Values in `defaults` SHALL be applied when a write operation omits the corresponding value (`scope` when `context.scope` is not supplied; `source` fields when `source` is incomplete). Readers SHALL NOT consult `defaults` when interpreting an object file.

#### Scenario: Asserting a claim without a source
- **WHEN** `claim_assert` is called with no `source` and `defaults.source.author` is `ben`
- **THEN** the written claim file contains `source.author: ben`

#### Scenario: Reading never depends on config
- **WHEN** an object file is read in a workspace whose `dkf.yaml` is absent
- **THEN** its scope and source are taken from the file alone

### Requirement: `.dkf` redirects discovery to a workspace elsewhere
A `.dkf` file MAY be placed in a directory that is not itself a workspace. Its first non-blank, non-comment line SHALL be the path of the workspace root, resolved relative to the directory containing the pointer, or absolute. A `dkf.yaml` in the same directory SHALL take precedence over a `.dkf`. Pointers SHALL NOT chain: the named directory MUST contain `dkf.yaml`, and if it does not, implementations SHALL report an error naming both the pointer and its target. A `.dkf` is not a workspace marker: it carries no configuration, and a workspace SHALL remain discoverable from inside it whether or not any pointer exists.

#### Scenario: Tool started at a repository root
- **WHEN** `repo/.dkf` contains `knowledge` and `repo/knowledge/dkf.yaml` exists, and a tool runs in `repo/src/`
- **THEN** `repo/knowledge` is used as the workspace

#### Scenario: Both marker and pointer present
- **WHEN** a directory contains both `dkf.yaml` and `.dkf`
- **THEN** that directory is the workspace and the pointer is ignored

#### Scenario: Pointer to a non-workspace
- **WHEN** a `.dkf` names a directory that has no `dkf.yaml`
- **THEN** discovery fails with an error naming both the pointer file and the target path

#### Scenario: Pointers do not chain
- **WHEN** a `.dkf` names a directory whose only DKF file is another `.dkf`
- **THEN** discovery fails rather than following the second pointer
