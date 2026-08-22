# Object Identifiers Specification

## Purpose

Defines the identifier format for DKF objects and records (`<prefix>_<uuidv7>`), the read-side leniency that keeps older workspaces readable, and the distinction between an id's minting time and an object's assertion `timestamp`.

## Requirements

### Requirement: Object identifiers are prefixed UUIDv7
Every DKF object and record id SHALL be formed as `<prefix>_` followed by a lowercase canonical RFC 9562 UUID version 7, where `<prefix>` is `par` (particular), `clm` (claim), `syn` (synthesis), `mrg` (merge), or `pub` (publish). Minting implementations SHALL ensure ids created within the same millisecond sort in creation order (e.g. via a monotonic counter).

#### Scenario: Minting a new claim id
- **WHEN** an implementation creates a new claim
- **THEN** the id matches `^clm_[0-9a-f]{8}-[0-9a-f]{4}-7[0-9a-f]{3}-[89ab][0-9a-f]{3}-[0-9a-f]{12}$`

#### Scenario: Ids minted in the same millisecond
- **WHEN** two claims are minted within one millisecond by the same implementation
- **THEN** lexical ordering of their ids matches creation order

#### Scenario: Minting a promotion id
- **WHEN** an implementation records a promotion
- **THEN** the id carries the `pub` prefix

### Requirement: Readers accept legacy identifier forms
Consumers and validators SHALL accept any id matching `^(par|clm|syn|mrg|pub)_[A-Za-z0-9-]+$` when reading, so that workspaces written with other schemes (including the draft's truncated ULIDs) remain readable. Validators MAY emit a warning for ids that are not UUIDv7.

#### Scenario: Reading a draft-era workspace
- **WHEN** a consumer loads a claim with id `clm_07m3zp9s2q1r4t8v`
- **THEN** the claim is read successfully and is not rejected as invalid

### Requirement: Minting time and assertion time are distinct
The time embedded in an id SHALL denote the minting instant. The `timestamp` field SHALL denote the assertion time and MAY be earlier than the minting time. Consumers SHALL NOT require the two to agree.

#### Scenario: Recording a dated document
- **WHEN** a claim with `timestamp: 2019-03-01T00:00:00Z` is minted on 2026-08-21
- **THEN** validators accept the claim and ordering by `timestamp` places it before claims asserted in 2026
