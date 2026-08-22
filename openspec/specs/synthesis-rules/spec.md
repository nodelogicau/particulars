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

### Requirement: A synthesis's subject is explicit and never inferred
Every claim and synthesis SHALL carry exactly one `subject` naming a particular. The subject SHALL be supplied explicitly by the caller: `synthesis_create` SHALL take a `particular_id` parameter accepting an id, URI, label, or alias, and implementations SHALL NOT infer a synthesis's subject from its inputs.

#### Scenario: Creating a synthesis
- **WHEN** `synthesis_create(particular_id, content, inputs[], unresolved, source)` is called
- **THEN** the written synthesis carries the resolved particular as its `subject`

#### Scenario: Subject omitted
- **WHEN** `synthesis_create` is called without a `particular_id`
- **THEN** the call fails rather than deriving a subject from the inputs

#### Scenario: Inputs disagree with the subject
- **WHEN** a synthesis about particular X cites only claims about particular Y
- **THEN** its subject remains X, because the subject came from the caller
