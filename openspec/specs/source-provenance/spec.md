# Source Provenance Specification

## Purpose

Defines the shared `source` block carried by claims, syntheses, retractions, and merge records, its minimum content, and the requirement that syntheses carry `source` with a `harness` in place of the earlier `produced-by` field.

## Requirements

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

### Requirement: Syntheses carry `source` with a mandatory `harness`
A synthesis SHALL carry `source` in the same shape as a claim, and its `source.harness` SHALL be present. The `produced-by` field SHALL NOT be used; `synthesis_create` SHALL accept this block as a parameter named `source`. Readers MAY treat a legacy `produced-by` block as `source` during v0.1.

#### Scenario: Consumer treating a synthesis as a claim
- **WHEN** a consumer that ignores synthesis-specific fields reads a synthesis
- **THEN** it finds a complete `source` block without special-casing

#### Scenario: Synthesis without harness
- **WHEN** a synthesis has `source: {author: ben}` and no `harness`
- **THEN** validation fails

#### Scenario: Legacy file
- **WHEN** a synthesis file written by the v0.1.0 reference implementation carries `produced-by` and no `source`
- **THEN** a reader MAY interpret `produced-by` as `source` and SHOULD warn

### Requirement: Retraction and merge sources follow the same rule
The `source` inside a `retracted` block and on a merge record SHALL satisfy the same minimum as a claim's `source`.

#### Scenario: Retraction by an agent
- **WHEN** a `retracted` block has `source: {harness: claude}`
- **THEN** the retraction is valid
