# Synthesis Rules Specification

## Purpose

Defines rules on synthesis content beyond its shape: inputs may concern other particulars, and `unresolved` is always present with `None identified` as the conventional empty value.

## Requirements

### Requirement: Synthesis inputs may concern other particulars
A synthesis's `inputs` MAY reference claims or syntheses whose `subject` differs from the synthesis's `subject`. Validators SHALL NOT reject a synthesis on that basis.

#### Scenario: Library claim informing a project synthesis
- **WHEN** a synthesis with `subject: par_project` lists an input with `subject: par_library`
- **THEN** the synthesis is valid

### Requirement: `unresolved` is required and has a conventional empty value
`unresolved` SHALL be present on every synthesis. The exact string `None identified` SHALL be the conventional value meaning that the producer considered the question and found nothing outstanding. Validators SHALL accept it and SHALL reject a synthesis whose `unresolved` is absent, null, or empty.

#### Scenario: Fully reconciled synthesis
- **WHEN** a synthesis has `unresolved: None identified`
- **THEN** it is valid and tooling can distinguish it from a synthesis that omitted the field

#### Scenario: Missing unresolved
- **WHEN** a synthesis has no `unresolved` field
- **THEN** validation fails

#### Scenario: Null unresolved
- **WHEN** a synthesis has `unresolved: ~`
- **THEN** validation fails

### Requirement: A synthesis's subject is explicit and never derived
Every claim and synthesis SHALL carry exactly one `subject` naming a particular. The subject SHALL be supplied explicitly by the caller: `synthesis_create` SHALL take a `particular_id` parameter accepting an id, URI, label, or alias, and implementations SHALL NOT derive a synthesis's subject from its inputs. The wording avoids "infer", which names an evidential value in `claim-evidential` and means something unrelated there.

#### Scenario: Creating a synthesis
- **WHEN** `synthesis_create(particular_id, content, inputs[], unresolved, source)` is called
- **THEN** the written synthesis carries the resolved particular as its `subject`

#### Scenario: Subject omitted
- **WHEN** `synthesis_create` is called without a `particular_id`
- **THEN** the call fails rather than deriving a subject from the inputs

#### Scenario: Inputs disagree with the subject
- **WHEN** a synthesis about particular X cites only claims about particular Y
- **THEN** its subject remains X, because the subject came from the caller

### Requirement: A synthesis is inferred by construction
A synthesis SHALL NOT declare an `evidential`. Its warrant is argument from its inputs, which is what a synthesis is, and consumers SHALL treat every synthesis as `inferred`.

#### Scenario: Synthesis omits the field
- **WHEN** a synthesis is written with no `evidential`
- **THEN** it is valid, and consumers treat its warrant as inferred

#### Scenario: Synthesis declares one
- **WHEN** a synthesis carries an `evidential` field
- **THEN** validation fails, because the value is implied and cannot vary

### Requirement: `method` names the kind of resolution performed
A synthesis SHALL carry `method` with one of three values: `reconciliation`, where the inputs disagreed about a fact and the synthesis settles it; `qualification`, where the inputs are each true in different contexts; or `positions`, where no evidence settles the disagreement. A `positions` synthesis MAY reach an evaluative conclusion, and SHALL say what would move it. An evaluative conclusion SHALL NOT be recorded as `reconciliation`, which asserts that a factual disagreement was settled.

#### Scenario: Settling a factual disagreement
- **WHEN** two claims give different ports for the same service and a synthesis determines which holds
- **THEN** it records `method: reconciliation`

#### Scenario: Both true in context
- **WHEN** two claims conflict only because they describe different environments
- **THEN** the synthesis records `method: qualification`

#### Scenario: A disagreement evidence cannot settle
- **WHEN** a synthesis reconciles two `held` claims that no evidence would decide between
- **THEN** it records `method: positions`, and its `unresolved` may state that the question is not one evidence closes

#### Scenario: An evaluative conclusion
- **WHEN** a synthesis weighs two `held` claims and concludes that one path is better
- **THEN** it records `method: positions`, states what would change the conclusion, and is still `inferred` because it was reached by argument

#### Scenario: An evaluative conclusion dressed as a settlement
- **WHEN** a synthesis reaches an evaluative conclusion and records `method: reconciliation`
- **THEN** validation fails, because no factual disagreement was settled

#### Scenario: A held claim is not exempt from synthesis
- **WHEN** two conflicting `held` claims are unsynthesised for a particular
- **THEN** `conflict_detect` reports them, and marking them `held` does not remove the need for a synthesis
