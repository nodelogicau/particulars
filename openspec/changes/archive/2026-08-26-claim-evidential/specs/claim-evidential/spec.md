## ADDED Requirements

### Requirement: Every claim declares what backs it
A claim SHALL carry an `evidential` field with exactly one of three values: `observed`, where someone or something looked; `inferred`, where the claim was derived by reasoning from other claims; or `held`, where the claim is a position and nothing external backs it. There SHALL be no default value, and writers SHALL NOT supply one on the caller's behalf.

#### Scenario: Reading a fact from a document
- **WHEN** a claim records what a configuration file says, citing that file
- **THEN** it declares `evidential: observed`

#### Scenario: An agent's conclusion asserted as a claim
- **WHEN** an agent asserts a conclusion it reasoned to, without recording it as a synthesis
- **THEN** it declares `evidential: inferred`

#### Scenario: A position
- **WHEN** a claim asserts that an architectural decision was a mistake
- **THEN** it declares `evidential: held`

#### Scenario: Writer omits the value
- **WHEN** `claim_assert` is called without an evidential
- **THEN** the call fails, and the implementation does not choose a value

### Requirement: Readers accept absence and report it as undeclared
Consumers SHALL accept a claim with no `evidential` and SHALL report its warrant as `undeclared`. `undeclared` SHALL NOT be a value a writer may emit, SHALL NOT be treated as equivalent to `observed`, and SHALL NOT be inferred from any other field. It means the claim predates the requirement and its warrant cannot now be established.

#### Scenario: Reading a pre-existing workspace
- **WHEN** a consumer loads a claim written before this requirement existed
- **THEN** the claim is valid, readable, and citable, and its warrant is reported as `undeclared`

#### Scenario: Undeclared is not a fact
- **WHEN** an agent composes an answer from claims including undeclared ones
- **THEN** it does not present them as observations

#### Scenario: Writing undeclared
- **WHEN** a writer attempts to emit `evidential: undeclared`
- **THEN** validation fails

### Requirement: `confidence` is the inverse probability that a claim is mistaken
The specification SHALL define `confidence` as the inverse probability that the claim is mistaken. It SHALL be applicable to `observed` and `inferred` claims, and SHALL have no meaning for `held` claims.

#### Scenario: Confidence on an observation
- **WHEN** a claim declares `observed` with `confidence: 0.9`
- **THEN** the value means the author judges a one-in-ten chance the claim is mistaken

#### Scenario: Confidence carries no other meaning
- **WHEN** a consumer aggregates confidence across claims
- **THEN** it may do so only across claims whose evidential admits confidence

### Requirement: A held claim carries no confidence
A claim declaring `evidential: held` SHALL NOT carry `confidence`. Validators SHALL reject such a claim and SHOULD report the condition as `confidence_on_held`. Implementations SHALL NOT offer a separate field recording strength of conviction.

#### Scenario: Confidence on a position
- **WHEN** a claim declares `held` and carries `confidence: 0.9`
- **THEN** validation fails, reporting `confidence_on_held`

#### Scenario: A position without confidence
- **WHEN** a claim declares `held` and omits `confidence`
- **THEN** it is valid

#### Scenario: Conviction belongs in content
- **WHEN** an author wants to record how firmly a position is held
- **THEN** they express it in the claim's `content`, and no field exists to record it numerically

#### Scenario: Confidence on an undeclared claim
- **WHEN** a pre-existing claim carries confidence and no evidential
- **THEN** validation does not fail, and the confidence is reported as unverified
