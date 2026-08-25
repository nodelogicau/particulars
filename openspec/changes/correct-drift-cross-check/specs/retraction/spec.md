## RENAMED Requirements

- FROM: `### Requirement: A declared kind may be cross-checked against source drift`
- TO: `### Requirement: Drift is reported alongside a declared kind, not checked against it`

## MODIFIED Requirements

### Requirement: Drift is reported alongside a declared kind, not checked against it
Implementations SHOULD report the observed drift state of a retracted object's cited document alongside the declared `kind`, as an observation rather than as a judgement of the declaration. They SHALL NOT treat an unchanged document hash as evidence against a declared `supersession`: drift is a signal about the source, whereas supersession asserts that the world moved, and the specification provides no way to distinguish a document that describes current state from one that is dated by design.

Where `defect` is declared against a document that has drifted, implementations SHOULD report the declaration as **unverifiable**, because the text the claim is said to have misread is no longer the text a reviewer can read. No check SHALL reject a retraction.

#### Scenario: Supersession against an unchanged source
- **WHEN** a retraction declares `kind: supersession` and the cited document's hash still matches
- **THEN** no warning is emitted, because a dated document is expected to be unchanged while the world moves

#### Scenario: Defect against a drifted source
- **WHEN** a retraction declares `kind: defect` and the cited document has drifted
- **THEN** the declaration is reported as unverifiable, and the retraction stands

#### Scenario: Defect against an unchanged source
- **WHEN** a retraction declares `kind: defect` and the cited document is unchanged
- **THEN** a reviewer can compare the claim against the quoted text, and nothing is reported

#### Scenario: Unverifiable source
- **WHEN** a retraction declares a kind and its source carries no hash, or cannot be fetched
- **THEN** the kind stands unverified and no warning is emitted
