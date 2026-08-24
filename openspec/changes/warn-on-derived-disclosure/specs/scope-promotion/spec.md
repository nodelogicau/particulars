## MODIFIED Requirements

### Requirement: Promotion does not cascade to inputs
Promoting a synthesis SHALL NOT promote the claims or syntheses it cites. The resulting exposure is covered by the derived-disclosure requirement below, which applies however the synthesis came to be wider.

#### Scenario: Promoting a synthesis over personal inputs
- **WHEN** a synthesis is promoted to `public` and its inputs remain `personal`
- **THEN** only the synthesis becomes eligible for a public feed, and the implementation warns

#### Scenario: Public consumer sees unresolvable inputs
- **WHEN** a public consumer fetches a promoted synthesis whose inputs were not promoted
- **THEN** it receives input ids it cannot resolve, rather than the inputs' contents

## ADDED Requirements

### Requirement: Derived disclosure is warned, not forbidden
A synthesis's effective scope MAY be wider than the effective scope of its inputs, because reconciling narrowly-scoped evidence into a conclusion that can be shared is a legitimate reason to synthesise. Implementations SHOULD warn when a synthesis's effective scope is wider than the effective scope of any input it cites, and SHALL report that condition as `scope_wider_than_inputs`. Implementations SHALL NOT reject a synthesis on that basis, and SHALL NOT attempt to determine whether its content in fact discloses its inputs.

#### Scenario: Asserted wider than inputs
- **WHEN** a synthesis is asserted `organisation` citing claims asserted `personal`, with no promotion records
- **THEN** the implementation reports `scope_wider_than_inputs` naming the narrower inputs, and writes the synthesis

#### Scenario: Promoted past its inputs
- **WHEN** a synthesis asserted `organisation` over `organisation` inputs is promoted to `public` and its inputs are not
- **THEN** the same condition is reported

#### Scenario: Inputs promoted to match
- **WHEN** a synthesis asserted `public` cites a claim asserted `personal` that a non-retracted promotion widens to `public`
- **THEN** no warning is reported, because the comparison is between effective scopes

#### Scenario: A wider synthesis is still valid
- **WHEN** validation runs over a workspace containing a synthesis wider than its inputs
- **THEN** the condition is a warning and validation does not fail on it

### Requirement: Derived disclosure is evaluated from workspace state
Because a promotion can create or clear the condition without modifying the synthesis or its inputs, `scope_wider_than_inputs` SHALL be computed from current workspace state rather than recorded on the synthesis when it is written. Implementations SHALL evaluate it during validation, when a synthesis is created, and when `knowledge_publish` promotes a synthesis.

#### Scenario: Promotion creates the condition later
- **WHEN** a synthesis that warned on nothing at creation is later promoted past its inputs
- **THEN** `knowledge_publish` reports the condition, and validation reports it thereafter

#### Scenario: Promotion clears the condition later
- **WHEN** the inputs of a warning synthesis are promoted to match its effective scope
- **THEN** validation stops reporting the condition, with no change to the synthesis file
