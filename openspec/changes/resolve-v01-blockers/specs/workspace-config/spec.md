## MODIFIED Requirements

### Requirement: Workspace discovery walks up from the working directory
Implementations SHALL locate the workspace by searching the current directory and each ancestor. At each directory, a `dkf.yaml` SHALL make that directory the workspace; otherwise a `.dkf` pointer file, if present, SHALL redirect to the workspace it names. Explicit configuration — a workspace argument, then an environment variable — SHALL take precedence over discovery entirely.

#### Scenario: Invoked from a subdirectory
- **WHEN** a tool runs in `<root>/claims/` and `<root>/dkf.yaml` exists
- **THEN** `<root>` is used as the workspace

#### Scenario: Explicit configuration wins
- **WHEN** a tool is given an explicit workspace path and the working directory is inside a different workspace
- **THEN** the explicit path is used

## ADDED Requirements

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
