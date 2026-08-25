## ADDED Requirements

### Requirement: A synthesis is inferred by construction
A synthesis SHALL NOT declare an `evidential`. Its warrant is argument from its inputs, which is what a synthesis is, and consumers SHALL treat every synthesis as `inferred`.

#### Scenario: Synthesis omits the field
- **WHEN** a synthesis is written with no `evidential`
- **THEN** it is valid, and consumers treat its warrant as inferred

#### Scenario: Synthesis declares one
- **WHEN** a synthesis carries an `evidential` field
- **THEN** validation fails, because the value is implied and cannot vary

### Requirement: `method` names the kind of resolution performed
A synthesis SHALL carry `method` with one of three values: `reconciliation`, where the inputs disagreed about a fact and the synthesis settles it; `qualification`, where the inputs are each true in different contexts; or `positions`, where no evidence settles the disagreement and the synthesis names the positions and what would move either.

#### Scenario: Settling a factual disagreement
- **WHEN** two claims give different ports for the same service and a synthesis determines which holds
- **THEN** it records `method: reconciliation`

#### Scenario: Both true in context
- **WHEN** two claims conflict only because they describe different environments
- **THEN** the synthesis records `method: qualification`

#### Scenario: A disagreement evidence cannot settle
- **WHEN** a synthesis reconciles two `held` claims that no evidence would decide between
- **THEN** it records `method: positions`, and its `unresolved` may state that the question is not one evidence closes

#### Scenario: A held claim is not exempt from synthesis
- **WHEN** two conflicting `held` claims are unsynthesised for a particular
- **THEN** `conflict_detect` reports them, and marking them `held` does not remove the need for a synthesis
