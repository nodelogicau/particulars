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
