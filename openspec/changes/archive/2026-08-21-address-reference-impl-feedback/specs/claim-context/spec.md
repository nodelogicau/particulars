## ADDED Requirements

### Requirement: `context.scope` is present on disk
Every claim and synthesis file SHALL contain a `context` block with a `scope` of `personal`, `organisation`, or `public`. `context.topics` is optional and defaults to empty. Writers SHALL apply the workspace default (or `personal`) when a caller omits scope; readers SHALL NOT infer a scope for a file that lacks one.

#### Scenario: Asserting without scope
- **WHEN** `claim_assert` is called without `scope` in a workspace with no `defaults.scope`
- **THEN** the written file contains `context.scope: personal`

#### Scenario: File missing context
- **WHEN** a claim file has no `context` block
- **THEN** validation fails and the claim is not eligible for any feed

#### Scenario: Publishing decision from the file alone
- **WHEN** a public feed generator evaluates a claim file
- **THEN** it determines eligibility from `context.scope` in that file without consulting `dkf.yaml`
