## MODIFIED Requirements

### Requirement: Retraction is an append-only block on the object file
A retraction SHALL be represented by adding a `retracted` block to the retracted object's own YAML file, with fields `timestamp` (required), `reason` (required), `source` (required, see `source-provenance`), `kind` (optional, see below), and `superseded-by` (optional). For a claim, synthesis, merge record or promotion record, adding this block SHALL be one of exactly two permitted modifications to an existing file; the other is redaction, as defined in `redaction`, which applies to claims and syntheses only. A particular cannot be retracted; its file MAY instead be updated in its `label` and `aliases` by `particular_define`, and never in its `id`, `type` or `uri`. `workspace-layout` lists every permitted modification in one place. The block SHALL never be removed; reinstatement SHALL be expressed as a new claim or synthesis that cites the retracted object. A redaction MAY remove the block's `reason`, and only its `reason`: the block itself, with its `timestamp`, `source`, `kind` and `superseded-by`, SHALL remain, and its `reason` SHALL then be valid when absent.

#### Scenario: Retracting a claim
- **WHEN** `claim_retract(clm_X, reason, source)` is called
- **THEN** `claims/clm_X.yaml` gains a `retracted` block containing `timestamp`, `reason`, and `source`, and no other field of the file changes

#### Scenario: Attempting to un-retract
- **WHEN** an implementation is asked to reverse a retraction
- **THEN** it refuses to remove the `retracted` block and instead requires a new claim or synthesis citing the retracted object

#### Scenario: A redacted retraction reason
- **WHEN** a retracted claim's `retracted.reason` is redacted
- **THEN** the `retracted` block remains without `reason`, the object is still retracted, and its `kind` still counts as declared

#### Scenario: A particular is not retracted but may be updated
- **WHEN** an implementation is asked to retract a particular, and separately to add an alias to it
- **THEN** it refuses the retraction, and the alias update rewrites only the particular's `aliases`
