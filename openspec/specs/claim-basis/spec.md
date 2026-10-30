# Claim Basis Specification

## Purpose

Defines the optional `basis` on an inferred claim — the claims and syntheses it was inferred from, as its evidence — the rule that only inferred claims carry one, what a basis may cite, how lineage traverses it, the reporting of an inferred claim without a basis as `inferred_without_basis`, and the treatment of induction as an inferred claim with a basis rather than a synthesis method.

## Requirements

### Requirement: An inferred claim may name its basis
A claim MAY carry `basis`, a non-empty list of ids, each the id of a claim or synthesis. The basis SHALL be the objects the claim was inferred from, and SHALL be its evidence in the sense that `source.document` is the evidence of an `observed` claim. A basis SHALL carry ids only, with no `role` or `weight`. In canonical field order `basis` SHALL follow `evidential` and precede `confidence`.

#### Scenario: A rule of thumb cites its instances
- **WHEN** a claim states that renewals go wrong when the TTL is long, declares `evidential: inferred`, and is inferred from three claims about renewals that went wrong
- **THEN** it carries `basis` listing those three claim ids

#### Scenario: Inferred from a synthesis
- **WHEN** a claim is inferred from the current belief about another particular
- **THEN** its `basis` may list that synthesis's id

#### Scenario: Empty basis
- **WHEN** a claim carries `basis: []`
- **THEN** validation fails, because an empty basis means nothing that absence does not

### Requirement: Only an inferred claim carries a basis
`basis` SHALL appear only on a claim declaring `evidential: inferred`. Writers SHALL refuse to write `basis` on a claim declaring any other evidential, on a claim with no evidential, or on a synthesis. Validators SHALL fail validation on such a file, reporting the condition as `basis_not_inferred`. Readers SHALL NOT refuse to read the file.

#### Scenario: Basis on an observation
- **WHEN** `claim_assert` is called with `evidential: observed` and a `basis`
- **THEN** the call is refused and no file is written

#### Scenario: Basis on a synthesis
- **WHEN** a synthesis file carries `basis`
- **THEN** validation fails, reporting `basis_not_inferred`, and the synthesis is still read and citable

#### Scenario: Basis on a position
- **WHEN** a file declares `evidential: held` and carries a `basis`
- **THEN** validation fails, reporting `basis_not_inferred`, and the claim is still read

### Requirement: A basis cites existing DKF objects
Each id in a basis SHALL be the id of a claim or synthesis present in the workspace. Validators SHALL reject a dangling basis id, reporting it as a dangling reference. A basis MAY cite a retracted object. A basis SHALL NOT cite the claim that carries it, nor any object of another format; an object outside DKF is reached through a DKF claim about it, whose `source.document` cites it.

#### Scenario: Dangling basis id
- **WHEN** a claim's basis lists an id that matches no file in the workspace
- **THEN** validation fails, reporting the dangling reference against that claim

#### Scenario: An episode outside DKF
- **WHEN** a rule of thumb rests on an episode recorded by another format
- **THEN** its basis cites an `observed` DKF claim about the episode, and that claim's `source.document` cites the episode record

### Requirement: Lineage follows a basis
`lineage_trace` SHALL traverse `basis` as well as `inputs` and `superseded-by`, and SHALL label each basis edge with the relation `basis`, distinct from synthesis input roles. Traversal SHALL visit each object at most once.

#### Scenario: Walking from a rule to its instances
- **WHEN** `lineage_trace` is called on a claim whose basis lists three claims
- **THEN** the tree contains the three claims as children labelled `basis`

#### Scenario: Through a synthesis to a rule's instances
- **WHEN** a synthesis cites an inferred claim as an input, and `lineage_trace` is called on the synthesis with enough depth
- **THEN** the tree reaches the inferred claim through its input role and the instances through `basis`

### Requirement: An inferred claim without a basis is reported, not refused
An `inferred` claim without `basis` SHALL be valid. Validators SHALL report it as `inferred_without_basis`, a fact about the corpus as defined in `condition-reporting`, and SHOULD report it in aggregate. `claim_assert` SHALL write such a claim, and SHOULD warn when it does.

#### Scenario: An existing workspace
- **WHEN** validation runs over a workspace in which forty inferred claims predate `basis`
- **THEN** validation passes, and `inferred_without_basis` is reported once with a count of forty

#### Scenario: Writing without a basis
- **WHEN** `claim_assert` is called with `evidential: inferred` and no `basis`
- **THEN** the claim is written, and the response carries a warning naming `inferred_without_basis`

### Requirement: Induction is an inferred claim with a basis
The specification SHALL NOT define a synthesis method for induction. A generalisation from instances SHALL be recorded as an `inferred` claim whose basis lists the instances. A later counterexample SHALL be reconciled as any other disagreement is, typically as a `qualification` synthesis citing the rule and the counterexample. The number of instances a rule rests on, and when they occurred, SHALL be derived from its basis and SHALL NOT be recorded in a separate field.

#### Scenario: A counterexample arrives
- **WHEN** a rule of thumb with a basis of three instances is followed by a claim reporting a renewal with a long TTL that went well
- **THEN** the rule and the counterexample are reconciled by a `qualification` synthesis, and the rule's file is unchanged

#### Scenario: How much a rule rests on
- **WHEN** a reader asks how many instances a rule rests on and how recent they are
- **THEN** the answer is computed from the basis members and their timestamps
