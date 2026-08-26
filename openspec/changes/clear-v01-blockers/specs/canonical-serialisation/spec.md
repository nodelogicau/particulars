## MODIFIED Requirements

### Requirement: The signed payload is defined over the canonical form
The payload covered by the reserved `signature` field SHALL be the object parsed to its data model — mappings with string keys; values that are strings, numbers, booleans, arrays, or mappings — with the `retracted` and `signature` fields removed, canonicalised per RFC 8785 (JSON Canonicalization Scheme). Every field this specification defines as textual, including timestamps, ids, and references, SHALL be a string in the data model regardless of how a YAML parser would type it; `confidence` SHALL be a number. YAML anchors, aliases, and non-string keys SHALL NOT appear in objects. File-level layout — field order, quoting, indentation — SHALL NOT affect the payload.

#### Scenario: Reformatting does not invalidate
- **WHEN** a signed claim's file is rewritten in a different field order and quoting style with identical content
- **THEN** the payload, and therefore the signature, is unchanged

#### Scenario: Retraction does not invalidate
- **WHEN** a `retracted` block is appended to a signed claim
- **THEN** the payload is computed with `retracted` removed and the original signature still verifies

#### Scenario: Two writers, one payload
- **WHEN** two implementations serialise the same claim with `confidence: 0.9` and `confidence: 0.90`
- **THEN** both parse to the same number and produce byte-identical payloads

#### Scenario: Signature suites remain reserved
- **WHEN** an implementation asks what algorithm signs the payload
- **THEN** the specification defines only the payload in v0.1; suites are reserved
