# Canonical Serialisation Specification

## Purpose

Defines the canonical field order for each object and record type, the asymmetry between writers and readers, where implementation-specific fields belong, and the relationship between canonical order and the payload covered by the reserved `signature` field.

## Requirements

### Requirement: Each object type has a canonical field order
The field order shown for each object and record type in the specification SHALL be its canonical order. Writers SHOULD emit fields in that order. Readers MUST accept the fields in any order and MUST NOT reject a file because its fields are ordered differently.

#### Scenario: Writing a merge record
- **WHEN** an implementation writes a merge record
- **THEN** the fields appear in the order `id`, `type`, `uris`, `reason`, `source`, `timestamp`

#### Scenario: Reading a differently ordered file
- **WHEN** a consumer loads a claim whose `timestamp` precedes its `content`
- **THEN** the claim is read successfully

### Requirement: Extension fields follow specified fields
Fields an implementation adds beyond those the specification defines SHALL be written after all specified fields, preserving their relative order among themselves.

#### Scenario: An implementation-specific field
- **WHEN** an implementation adds a field of its own to a claim
- **THEN** the field is written after `confidence` and consumers that do not understand it ignore it

### Requirement: The signed payload is defined over the canonical form
The payload covered by the reserved `signature` field SHALL be the object parsed to its data model — mappings with string keys; values that are strings, numbers, booleans, arrays, or mappings — with the `retracted` and `signature` fields removed, canonicalised per RFC 8785 (JSON Canonicalization Scheme). Every field this specification defines as textual, including timestamps, ids, and references, SHALL be a string in the data model regardless of how a YAML parser would type it; `confidence` SHALL be a number. The payload SHALL be built from the parsed, typed data model, not from a generic YAML-to-JSON conversion, which types these fields differently — a YAML 1.2 parser returns an unquoted timestamp as a native time value, and only the typed model formats it back to the string this specification requires. YAML aliases are resolved before the data model exists and therefore never affect the payload; their prohibition in object files is a file-format safety rule (see below), not a signing rule. Non-string keys SHALL NOT appear in objects. File-level layout — field order, quoting, indentation — SHALL NOT affect the payload.

Object files SHALL NOT use YAML anchors and aliases: alias expansion is a resource-exhaustion vector, and validators SHOULD reject files containing them.

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
