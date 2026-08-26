# Condition Reporting Specification

## Purpose

Distinguishes the two kinds of reportable condition — findings about an object, reported per object because the object is the unit of action, and facts about the corpus, reported in aggregate because they carry no per-object action and can never be cleared — and the rule that an aggregate line carries a message only when it is uniform.

## Requirements

### Requirement: Conditions are findings about objects or facts about the corpus
The specification SHALL distinguish two kinds of reportable condition. A **finding about an object** is one a person might act on at that object — drift on a claim's source, a synthesis wider than its inputs, an unverifiable defect, a dangling reference — and SHALL be reported per object. A **fact about the corpus** is one that carries no per-object action — an undeclared evidential, a legacy compatibility marker, a document that cannot be verified — and SHOULD be reported in aggregate, because its discovery value is spent on first sight while its cost recurs on every run, and it cannot be cleared without rewriting an immutable file.

#### Scenario: An actionable finding lists per object
- **WHEN** validation finds `quote_drift` on two claims in a workspace of ninety
- **THEN** each is reported against its claim, because the claim is the unit of action

#### Scenario: A corpus fact aggregates
- **WHEN** every claim in a workspace predates the evidential requirement
- **THEN** `undeclared` is reported once with a count, not once per claim

#### Scenario: Aggregation does not hide the signal
- **WHEN** corpus facts are reported in aggregate
- **THEN** each condition still appears, with its count, and a consumer can expand it to the object list

### Requirement: An aggregate line carries a message only when it is uniform
Where a corpus fact is reported in aggregate, the condition's message SHALL appear on the aggregate line only when it is identical across the group. Where messages vary by object, the line SHALL carry the condition and count alone.

#### Scenario: Uniform message
- **WHEN** six objects carry the same legacy-provenance message
- **THEN** the aggregate line includes that message, and reads as a sentence

#### Scenario: Varying messages
- **WHEN** ninety-five objects are unverified for differing reasons
- **THEN** the aggregate line carries the condition and the count, and no single object's reason
