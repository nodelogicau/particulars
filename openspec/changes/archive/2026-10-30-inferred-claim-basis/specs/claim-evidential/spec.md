## MODIFIED Requirements

### Requirement: Every claim declares what backs it
A claim SHALL carry an `evidential` field with exactly one of three values: `observed`, where someone or something looked; `inferred`, where the claim was derived by reasoning from other claims; or `held`, where the claim is a position and nothing external backs it. There SHALL be no default value, and writers SHALL NOT supply one on the caller's behalf. An `inferred` claim MAY name the claims and syntheses it was derived from in `basis`, as defined in `claim-basis`.

#### Scenario: Reading a fact from a document
- **WHEN** a claim records what a configuration file says, citing that file
- **THEN** it declares `evidential: observed`

#### Scenario: An agent's conclusion asserted as a claim
- **WHEN** an agent asserts a conclusion it reasoned to, without recording it as a synthesis
- **THEN** it declares `evidential: inferred`

#### Scenario: An agent's conclusion names what it reasoned from
- **WHEN** an agent asserts a conclusion it reasoned to from claims in the workspace
- **THEN** it declares `evidential: inferred` and lists those claims in `basis`

#### Scenario: A position
- **WHEN** a claim asserts that an architectural decision was a mistake
- **THEN** it declares `evidential: held`

#### Scenario: Writer omits the value
- **WHEN** `claim_assert` is called without an evidential
- **THEN** the call fails, and the implementation does not choose a value
