# Scope Promotion Specification

## Purpose

Defines how an immutable claim is shared more widely: the promotion record written by `knowledge_publish`, the computation of effective scope, the widen-only and no-cascade rules that keep a partial implementation safe, the warning for a synthesis that is wider than its inputs, and the limits of retracting a promotion.

## Requirements

### Requirement: Promotion is recorded, not applied by modification
`knowledge_publish` SHALL record a promotion as a new file `publishes/pub_<uuidv7>.yaml` with `id`, `type: publish`, `claims` (a non-empty list of claim or synthesis ids), `scope` (the target scope), `source`, `timestamp`, and optional `reason`. It SHALL NOT modify any claim, synthesis, particular, or merge record. The signature becomes `knowledge_publish(claim_ids[], scope, source, reason?)`.

#### Scenario: Publishing a personal claim
- **WHEN** `knowledge_publish([clm_X], "public", source)` is called for a claim whose `context.scope` is `personal`
- **THEN** a file `publishes/pub_….yaml` is created naming `clm_X` and no existing object file changes

#### Scenario: Promotion without a source
- **WHEN** a promotion record has a `source` containing neither `author` nor `harness`
- **THEN** validation fails

#### Scenario: Empty promotion
- **WHEN** a promotion record lists no claims
- **THEN** validation fails

### Requirement: Effective scope is asserted scope widened by promotion
A claim's or synthesis's **effective scope** SHALL be the widest scope named by a non-retracted promotion record covering it, or its own `context.scope` when no such record exists, where the ordering is `personal` < `organisation` < `public`. Feed eligibility SHALL be determined from the object file together with the promotion records, and SHALL NOT be determined from workspace configuration.

#### Scenario: A promoted claim in a public feed
- **WHEN** a claim asserted `personal` is covered by a non-retracted promotion to `public`
- **THEN** its effective scope is `public` and it is eligible for a public feed

#### Scenario: Overlapping promotions
- **WHEN** a claim is covered by promotions to `organisation` and to `public`
- **THEN** its effective scope is `public`

#### Scenario: Configuration never widens
- **WHEN** `dkf.yaml` sets `defaults.scope: public` and a claim file says `personal` with no promotion record
- **THEN** the effective scope is `personal`

### Requirement: Promotion may only widen
A promotion record whose `scope` is narrower than the asserted `context.scope` of any claim it names SHALL be invalid. Narrowing SHALL be expressed by retracting the promotion record, or the object itself.

#### Scenario: Attempted narrowing
- **WHEN** a promotion names `scope: personal` for a claim asserted `public`
- **THEN** validation fails

#### Scenario: A naive consumer cannot leak
- **WHEN** a consumer ignores `/publishes/` entirely and honours `context.scope`
- **THEN** it never treats a restricted claim as publishable, and at worst withholds one that was authorised

### Requirement: Promotion does not cascade to inputs
Promoting a synthesis SHALL NOT promote the claims or syntheses it cites. The resulting exposure is covered by the derived-disclosure requirement below, which applies however the synthesis came to be wider.

#### Scenario: Promoting a synthesis over personal inputs
- **WHEN** a synthesis is promoted to `public` and its inputs remain `personal`
- **THEN** only the synthesis becomes eligible for a public feed, and the implementation warns

#### Scenario: Public consumer sees unresolvable inputs
- **WHEN** a public consumer fetches a promoted synthesis whose inputs were not promoted
- **THEN** it receives input ids it cannot resolve, rather than the inputs' contents

### Requirement: Promotion records are retractable and bounded
A promotion record MAY carry a `retracted` block as defined in `retraction`. A retracted promotion SHALL contribute nothing to effective scope. The specification SHALL state that retracting a promotion ends future feed eligibility and cannot recall data an external consumer has already fetched.

#### Scenario: Retracting a promotion
- **WHEN** a promotion to `public` is retracted
- **THEN** the covered claims revert to their asserted scope and are excluded from future feeds, and the promotion file remains on disk with its `retracted` block

#### Scenario: Already-fetched data
- **WHEN** a promotion is retracted after a crawler has fetched the claim
- **THEN** the specification does not claim the fetched copy is withdrawn

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
