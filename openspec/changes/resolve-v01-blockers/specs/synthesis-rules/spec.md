## ADDED Requirements

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
