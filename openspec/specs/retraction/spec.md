# Retraction Specification

## Purpose

Defines how a claim, synthesis, or merge record is retracted: an append-only `retracted` block on the object's own file, the optional `superseded-by` pointer, and the consequences for the index and for signatures.

## Requirements

### Requirement: Retraction is an append-only block on the object file
A retraction SHALL be represented by adding a `retracted` block to the retracted object's own YAML file, with fields `timestamp` (required), `reason` (required), `source` (required, see `source-provenance`), `kind` (optional, see below), and `superseded-by` (optional). Adding this block SHALL be the only permitted modification to an existing object file. The block SHALL never be removed; reinstatement SHALL be expressed as a new claim or synthesis that cites the retracted object.

#### Scenario: Retracting a claim
- **WHEN** `claim_retract(clm_X, reason, source)` is called
- **THEN** `claims/clm_X.yaml` gains a `retracted` block containing `timestamp`, `reason`, and `source`, and no other field of the file changes

#### Scenario: Attempting to un-retract
- **WHEN** an implementation is asked to reverse a retraction
- **THEN** it refuses to remove the `retracted` block and instead requires a new claim or synthesis citing the retracted object

### Requirement: Syntheses and merge records are retractable
The `retracted` block SHALL be valid on claims, syntheses, and merge records alike.

#### Scenario: Retracting a synthesis
- **WHEN** a synthesis file carries a `retracted` block
- **THEN** consumers treat it as retracted for recall and conflict purposes, and it is no longer eligible to be `current`

### Requirement: The index mirrors retraction
When an object is retracted, its `index.yaml` entry SHALL carry `retracted: true`.

#### Scenario: Filtering without opening files
- **WHEN** `knowledge_recall` is called with `include_retracted: false`
- **THEN** retracted objects are excluded using the index entry alone

### Requirement: `superseded-by` points at an existing claim or synthesis
A `retracted.superseded-by` value, when present, SHALL be the id of an existing claim or synthesis. Validators SHALL reject a dangling target. The pointer is informational for readers and `lineage_trace`; it SHALL NOT make the target an input of anything and SHALL NOT count as synthesis for conflict detection.

#### Scenario: Typo-grade correction
- **WHEN** a claim stating port 443 is retracted with `superseded-by: clm_Y` and `clm_Y` exists
- **THEN** the retraction is valid and `lineage_trace(clm_X)` shows `clm_Y` as its successor

#### Scenario: Dangling supersession
- **WHEN** a `retracted` block names a `superseded-by` id that does not exist in the workspace
- **THEN** validation fails

### Requirement: Signatures exclude the retraction block
The payload covered by the reserved `signature` field SHALL be the canonical object minus the `retracted` and `signature` fields.

#### Scenario: Retracting a signed claim
- **WHEN** a signed claim is later retracted
- **THEN** the original signature still verifies against the object with `retracted` and `signature` removed

### Requirement: A retraction may declare why the claim died
A `retracted` block MAY carry `kind` with one of three values: `defect`, where the claim misread its source; `supersession`, where the source was correct when read and the world has since moved; or `provenance-failure`, where the source itself was wrong. Implementations SHALL NOT infer `kind` from the presence or absence of `superseded-by`, which records whether a replacement exists and not why the object was withdrawn.

#### Scenario: Defect with a replacement
- **WHEN** a misread claim is corrected by asserting the right value and retracting the original with `superseded-by`
- **THEN** `kind: defect` is valid alongside `superseded-by`

#### Scenario: Supersession with no replacement
- **WHEN** a claim is retracted because its subject no longer exists and nothing replaces the fact
- **THEN** `kind: supersession` is valid with no `superseded-by`

#### Scenario: Kind omitted
- **WHEN** a `retracted` block carries no `kind`
- **THEN** the retraction is valid and its cause is reported as undeclared

### Requirement: A declared kind may be cross-checked against source drift
Where a retracted object cites a structured document reference that can be fetched, implementations SHOULD compare the declared `kind` against the observed drift and warn on disagreement — in particular where `supersession` is declared but the document hash is unchanged, since nothing moved to supersede the claim. The check SHALL be a warning and SHALL NOT reject the retraction.

#### Scenario: Supersession against an unchanged source
- **WHEN** a retraction declares `kind: supersession` and the cited document's hash still matches
- **THEN** the implementation warns that nothing in the source moved

#### Scenario: Unverifiable source
- **WHEN** a retraction declares a kind and its source carries no hash, or cannot be fetched
- **THEN** the kind stands unverified and no warning is emitted

### Requirement: Retraction kind is the basis of harness attribution
The specification SHALL state that `kind` is the observation from which the reliability of a `source.harness` or `source.model` may be assessed: a `defect` is evidence about the process that produced the claim, a `supersession` is not, and a `provenance-failure` is evidence about the cited document and everything else citing it.

#### Scenario: Assessing a harness
- **WHEN** a consumer evaluates the reliability of claims produced by a given harness
- **THEN** it counts `defect` retractions against that harness and does not count `supersession` retractions

#### Scenario: A discredited document
- **WHEN** a claim is retracted with `kind: provenance-failure`
- **THEN** other non-retracted claims citing the same document are identifiable as candidates for review
