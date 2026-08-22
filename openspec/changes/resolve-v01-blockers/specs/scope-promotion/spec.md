## ADDED Requirements

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
Promoting a synthesis SHALL NOT promote the claims or syntheses it cites. Implementations SHOULD warn when a promoted synthesis has inputs whose effective scope is narrower than its own.

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
