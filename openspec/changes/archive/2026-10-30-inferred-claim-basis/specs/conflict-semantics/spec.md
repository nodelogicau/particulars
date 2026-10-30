## MODIFIED Requirements

### Requirement: Structural conflict sets are defined per particular
For a particular (or merge equivalence class) the specification SHALL define: **current** — the most recent non-retracted synthesis with `subject` in the class, ordered by `timestamp` then id; **unsynthesised** — non-retracted claims and syntheses with `subject` in the class that are not in the transitive `inputs` of `current`, where the transitive `inputs` follow synthesis `inputs` only and not `basis`; **stale** — non-retracted claims and syntheses with `subject` in the class that cite, directly or transitively through `inputs` and `basis`, a retracted object. `conflict_detect` SHALL compute and return these sets without requiring an LLM.

#### Scenario: Claim after the latest synthesis
- **WHEN** a synthesis `syn_1` covers `clm_1` and `clm_2`, and `clm_3` is later asserted about the same particular
- **THEN** `current` is `syn_1` and `unsynthesised` is `{clm_3}`

#### Scenario: No synthesis yet
- **WHEN** a particular has claims `clm_1` and `clm_2` and no synthesis
- **THEN** `current` is absent and `unsynthesised` is `{clm_1, clm_2}`

#### Scenario: Retracted input
- **WHEN** `clm_1` is retracted after `syn_1` cited it
- **THEN** `syn_1` is in `stale` and its file is unchanged

#### Scenario: Retracted basis member
- **WHEN** `clm_rule` declares `inferred` with `basis: [clm_a, clm_b]`, and `clm_a` is retracted
- **THEN** `clm_rule` is in `stale` for its particular and its file is unchanged

#### Scenario: Staleness through a rule
- **WHEN** `syn_1` cites `clm_rule` as an input, and a member of `clm_rule`'s basis is retracted
- **THEN** both `clm_rule` and `syn_1` are in `stale` for their particulars

#### Scenario: Leaving the stale set
- **WHEN** a stale inferred claim is retracted with `superseded-by` pointing at a claim with a revised basis
- **THEN** it is no longer in `stale`, and its replacement is `unsynthesised` like any other

## ADDED Requirements

### Requirement: Citing in a basis does not synthesise
An object named in a claim's `basis` SHALL NOT thereby be considered synthesised, for its own particular or any other. A synthesis that cites an inferred claim as an input SHALL be considered to synthesise that claim and SHALL NOT be considered to synthesise its basis.

#### Scenario: Instances of a rule about the same subject
- **WHEN** `clm_rule` about particular P lists `clm_a` and `clm_b`, also about P, in its basis, and P has no synthesis
- **THEN** `unsynthesised` for P is `{clm_rule, clm_a, clm_b}`

#### Scenario: A synthesis over a rule
- **WHEN** the current synthesis for P cites `clm_rule` as an input but not `clm_a` or `clm_b`
- **THEN** `clm_rule` is synthesised for P, and `clm_a` and `clm_b` remain `unsynthesised`
