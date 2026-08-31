## MODIFIED Requirements

### Requirement: Conditions are findings about objects or facts about the corpus
The specification SHALL distinguish two kinds of reportable condition. A **finding about an object** is one a person might act on at that object — drift on a claim's source, a synthesis wider than its inputs, an unverifiable defect, a dangling reference — and SHALL be reported per object. A **fact about the corpus** is one that carries no per-object action — an undeclared evidential, a legacy compatibility marker, a document that cannot be verified, an author name that resolves to no particular or to several — and SHOULD be reported in aggregate, because its discovery value is spent on first sight while its cost recurs on every run, and it cannot be cleared at any object: either because clearing it would mean rewriting an immutable file, or because the action that clears it is at the workspace and clears every occurrence at once.

#### Scenario: An actionable finding lists per object
- **WHEN** validation finds `quote_drift` on two claims in a workspace of ninety
- **THEN** each is reported against its claim, because the claim is the unit of action

#### Scenario: A corpus fact aggregates
- **WHEN** every claim in a workspace predates the evidential requirement
- **THEN** `undeclared` is reported once with a count, not once per claim

#### Scenario: A workspace-level action clears a corpus fact
- **WHEN** one hundred claims carry `author: ben` matching no particular, and a particular with alias `ben` is then defined
- **THEN** the `author_unresolved` line disappears from the next report with no object having changed

#### Scenario: Aggregation does not hide the signal
- **WHEN** corpus facts are reported in aggregate
- **THEN** each condition still appears, with its count, and a consumer can expand it to the object list
