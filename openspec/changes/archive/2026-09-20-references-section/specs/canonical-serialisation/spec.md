## ADDED Requirements

### Requirement: Timestamps are RFC 3339 instants
Every field this specification defines as a timestamp — an object's `timestamp`, a retraction's `timestamp`, a merge or promotion record's `timestamp`, and an index entry's `timestamp` — SHALL be an RFC 3339 `date-time`. Writers SHALL write the instant in UTC with the `Z` designator at seconds precision, `YYYY-MM-DDTHH:MM:SSZ`. Readers MUST accept any RFC 3339 `date-time` — with a numeric offset, with fractional seconds, with a lowercase `t` or `z` — and MUST NOT reject a file for the form its timestamps take. Timestamps SHALL be compared as instants, never as strings. Wherever this specification derives a calendar month from a timestamp, the month SHALL be that of the instant in UTC. In the data model the signed payload is built from, a timestamp SHALL be its canonical string — the instant in UTC with `Z`, with a fractional second present only when non-zero and without trailing zeros — so that two files carrying the same instant in different forms produce the same payload.

#### Scenario: Writing a claim
- **WHEN** an implementation on a machine set to UTC+2 writes a claim at 11:02 local time on 2026-08-20
- **THEN** the file carries `timestamp: 2026-08-20T09:02:00Z`

#### Scenario: Reading an offset form
- **WHEN** a hand-edited claim carries `timestamp: 2026-08-20T11:02:00+02:00`
- **THEN** the claim is read successfully and its timestamp is the instant 2026-08-20T09:02:00Z

#### Scenario: A retraction at a month boundary
- **WHEN** a retraction carries `timestamp: 2026-09-01T00:30:00+02:00`
- **THEN** it falls in August 2026 for sharding and index purposes, and if August is sealed validation reports it as a retraction dated into a sealed month

#### Scenario: Same instant, one payload
- **WHEN** two otherwise identical claim files carry `timestamp: 2026-08-20T09:02:00Z` and `timestamp: 2026-08-20T11:02:00+02:00`
- **THEN** both produce byte-identical payloads

#### Scenario: Ordering across forms
- **WHEN** two non-retracted syntheses on the same subject carry `timestamp: 2026-08-20T09:02:00Z` and `timestamp: 2026-08-20T10:00:00+02:00`
- **THEN** the first is current, because it is the later instant, although the second is the later string

#### Scenario: A fractional second survives the payload
- **WHEN** a file written by another tool carries `timestamp: 2026-08-20T09:02:00.500Z`
- **THEN** the payload carries `2026-08-20T09:02:00.5Z`, and the same file written `2026-08-20T09:02:00Z` would not produce the same payload
