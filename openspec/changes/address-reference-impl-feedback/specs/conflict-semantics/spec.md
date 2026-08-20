## ADDED Requirements

### Requirement: Structural conflict sets are defined per particular
For a particular (or merge equivalence class) the specification SHALL define: **current** — the most recent non-retracted synthesis with `subject` in the class, ordered by `timestamp` then id; **unsynthesised** — non-retracted claims and syntheses with `subject` in the class that are not in the transitive `inputs` of `current`; **stale** — non-retracted syntheses with `subject` in the class that cite, directly or transitively, a retracted input. `conflict_detect` SHALL compute and return these sets without requiring an LLM.

#### Scenario: Claim after the latest synthesis
- **WHEN** a synthesis `syn_1` covers `clm_1` and `clm_2`, and `clm_3` is later asserted about the same particular
- **THEN** `current` is `syn_1` and `unsynthesised` is `{clm_3}`

#### Scenario: No synthesis yet
- **WHEN** a particular has claims `clm_1` and `clm_2` and no synthesis
- **THEN** `current` is absent and `unsynthesised` is `{clm_1, clm_2}`

#### Scenario: Retracted input
- **WHEN** `clm_1` is retracted after `syn_1` cited it
- **THEN** `syn_1` is in `stale` and its file is unchanged

### Requirement: Reporting rule and priority
`conflict_detect` SHALL report a particular when `current` exists and `unsynthesised` is non-empty, or when `current` is absent and `unsynthesised` has two or more members, or when `stale` is non-empty. The suggested synthesis priority SHALL be `|unsynthesised| + |stale|`. Judging whether members actually contradict SHALL be left to the reasoning harness.

#### Scenario: Single unsynthesised claim, no current
- **WHEN** a particular has exactly one claim and no synthesis
- **THEN** it is not reported

#### Scenario: Priority ordering
- **WHEN** particular P has 3 unsynthesised and 1 stale and particular Q has 2 unsynthesised and 0 stale
- **THEN** P is returned with priority 4 ahead of Q with priority 2

### Requirement: Current belief is the `current` synthesis
The statement "the current belief about any particular is the most recent synthesis" SHALL be defined as `current`, even when claims post-date it; such claims SHALL be surfaced as `unsynthesised` rather than silently becoming the belief.

#### Scenario: Recall in lineage order
- **WHEN** `knowledge_recall` is called for a particular with a `current` synthesis and later claims
- **THEN** the response identifies `current` as the belief and lists the later claims as unsynthesised

### Requirement: Retraction does not cascade by mutation
Retracting an input SHALL NOT modify any synthesis that cites it. Affected syntheses SHALL be reported as `stale` until a newer synthesis supersedes them. A `superseded-by` pointer SHALL NOT count as synthesis; the replacement object is `unsynthesised` like any other.

#### Scenario: Supersession is not synthesis
- **WHEN** `clm_1` is retracted with `superseded-by: clm_9`
- **THEN** `clm_9` appears in `unsynthesised` for its particular

### Requirement: Cross-particular inputs do not synthesise the other particular
A claim about particular Y cited as an input by a synthesis about particular X SHALL NOT thereby be considered synthesised for Y.

#### Scenario: Library claim informing a project synthesis
- **WHEN** `clm_lib` (subject Y) is an input to `syn_proj` (subject X)
- **THEN** `clm_lib` remains in Y's `unsynthesised` set
