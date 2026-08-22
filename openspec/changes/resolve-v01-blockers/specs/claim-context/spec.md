## MODIFIED Requirements

### Requirement: `context.scope` is present on disk
Every claim and synthesis file SHALL contain a `context` block with a `scope` of `personal`, `organisation`, or `public`. `context.topics` is optional and defaults to empty. Writers SHALL apply the workspace default (or `personal`) when a caller omits scope; readers SHALL NOT infer a scope for a file that lacks one. The value in the file is the object's **asserted** scope; its effective scope is that value widened by any promotion record covering it (see `scope-promotion`), and is never taken from workspace configuration.

#### Scenario: Asserting without scope
- **WHEN** `claim_assert` is called without `scope` in a workspace with no `defaults.scope`
- **THEN** the written file contains `context.scope: personal`

#### Scenario: File missing context
- **WHEN** a claim file has no `context` block
- **THEN** validation fails and the claim is not eligible for any feed

#### Scenario: Publishing decision from the file alone
- **WHEN** a public feed generator evaluates a claim file with no promotion record covering it
- **THEN** it determines eligibility from `context.scope` in that file without consulting `dkf.yaml`

#### Scenario: Asserted scope is never rewritten
- **WHEN** a claim asserted `personal` is promoted to `public`
- **THEN** its file still reads `context.scope: personal` and the promotion lives in its own record
