## MODIFIED Requirements

### Requirement: `source` has one shape and a minimum content
Claims, syntheses, retraction blocks, and merge records SHALL carry a `source` block with optional fields `author`, `harness`, `model`, and `document`. `author` SHALL be a particular reference — a particular id, a particular URI, or a bare name — as defined in `source-attribution`; `harness` and `model` are strings. `document` MAY be a URI string or a structured reference as defined in `source-verification`. A `source` SHALL contain at least one of `author` or `harness`, and an `author` in any of its three forms satisfies that minimum whether or not it resolves. Validators SHALL reject a `source` containing neither.

#### Scenario: Agent-only claim
- **WHEN** a claim has `source: {harness: claude, model: claude-sonnet-4-6}` and no `author`
- **THEN** the claim is valid

#### Scenario: Human-only claim
- **WHEN** a claim has `source: {author: ben}`
- **THEN** the claim is valid

#### Scenario: Author as a URI
- **WHEN** a claim has `source: {author: https://orcid.org/0000-0002-1825-0097}` and no `harness`
- **THEN** the claim is valid, whether or not a particular with that URI exists

#### Scenario: Empty source
- **WHEN** a claim has `source: {document: https://…}` only
- **THEN** validation fails

#### Scenario: Structured document does not satisfy the minimum
- **WHEN** a claim carries a structured `document` with `ref`, `author`, `hash` and `quote` but the `source` has neither `author` nor `harness`
- **THEN** validation fails, because a document's author is who was read and not who read them
