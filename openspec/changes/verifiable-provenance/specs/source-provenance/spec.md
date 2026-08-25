## MODIFIED Requirements

### Requirement: `source` has one shape and a minimum content
Claims, syntheses, retraction blocks, and merge records SHALL carry a `source` block with optional fields `author`, `harness`, `model`, and `document`. `document` MAY be a URI string or a structured reference as defined in `source-verification`. A `source` SHALL contain at least one of `author` or `harness`. Validators SHALL reject a `source` containing neither.

#### Scenario: Agent-only claim
- **WHEN** a claim has `source: {harness: claude, model: claude-sonnet-4-6}` and no `author`
- **THEN** the claim is valid

#### Scenario: Human-only claim
- **WHEN** a claim has `source: {author: ben}`
- **THEN** the claim is valid

#### Scenario: Empty source
- **WHEN** a claim has `source: {document: https://…}` only
- **THEN** validation fails

#### Scenario: Structured document does not satisfy the minimum
- **WHEN** a claim carries a structured `document` with `uri`, `hash` and `quote` but neither `author` nor `harness`
- **THEN** validation fails, because a document is what was read and not who read it
