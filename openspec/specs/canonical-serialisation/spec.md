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
The specification SHALL define the "canonical object" referenced by the reserved `signature` field as the object in canonical field order with the `retracted` and `signature` fields removed. The specification SHALL state that when signing is specified, emitting the canonical order becomes mandatory for any object that is signed.

#### Scenario: Two implementations sign the same claim
- **WHEN** two conformant implementations serialise the same claim for signing
- **THEN** they produce the same field order, so the same payload is signed
