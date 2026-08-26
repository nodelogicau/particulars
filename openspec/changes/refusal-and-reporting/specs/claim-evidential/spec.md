## MODIFIED Requirements

### Requirement: A held claim carries no confidence
A claim declaring `evidential: held` SHALL NOT carry `confidence`. Writers SHALL refuse to create such a claim. Validators SHALL fail validation on one, reporting the condition as `confidence_on_held`. Readers SHALL NOT refuse to read the file: it cannot be corrected, so a reader that rejected it would strand it permanently. Implementations SHALL NOT offer a separate field recording strength of conviction.

#### Scenario: Confidence on a position
- **WHEN** a claim declares `held` and carries `confidence: 0.9`
- **THEN** validation fails, reporting `confidence_on_held`

#### Scenario: Refused at write time
- **WHEN** `claim_assert` is called with `evidential: held` and a `confidence`
- **THEN** the call is refused and no file is written

#### Scenario: An existing offending file is still read
- **WHEN** a workspace contains a `held` claim carrying `confidence`, written before writers refused it
- **THEN** the claim is read and citable, and validation reports `confidence_on_held`

#### Scenario: A position without confidence
- **WHEN** a claim declares `held` and omits `confidence`
- **THEN** it is valid

#### Scenario: Conviction belongs in content
- **WHEN** an author wants to record how firmly a position is held
- **THEN** they express it in the claim's `content`, and no field exists to record it numerically

#### Scenario: Confidence on an undeclared claim
- **WHEN** a pre-existing claim carries confidence and no evidential
- **THEN** validation does not fail, and the confidence is reported as unverified
