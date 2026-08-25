## MODIFIED Requirements

### Requirement: Retraction is an append-only block on the object file
A retraction SHALL be represented by adding a `retracted` block to the retracted object's own YAML file, with fields `timestamp` (required), `reason` (required), `source` (required, see `source-provenance`), `kind` (optional, see below), and `superseded-by` (optional). Adding this block SHALL be the only permitted modification to an existing object file. The block SHALL never be removed; reinstatement SHALL be expressed as a new claim or synthesis that cites the retracted object.

#### Scenario: Retracting a claim
- **WHEN** `claim_retract(clm_X, reason, source)` is called
- **THEN** `claims/clm_X.yaml` gains a `retracted` block containing `timestamp`, `reason`, and `source`, and no other field of the file changes

#### Scenario: Attempting to un-retract
- **WHEN** an implementation is asked to reverse a retraction
- **THEN** it refuses to remove the `retracted` block and instead requires a new claim or synthesis citing the retracted object

## ADDED Requirements

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
