## MODIFIED Requirements

### Requirement: Merge records are a defined record type
A merge SHALL be stored as `merges/mrg_<uuidv7>.yaml` with `id`, `type: merge`, `uris` (exactly two URIs), optional `reason`, `source` (see `source-provenance`), and `timestamp`, written in that order (see `canonical-serialisation`). The file SHALL be listed in `index.yaml` with `id`, `type`, and `uris`. Merge records SHALL NOT rewrite, move, or modify any claim, synthesis, or particular.

#### Scenario: Declaring a merge
- **WHEN** `particular_merge(uri_a, uri_b, source)` is called
- **THEN** a file `merges/mrg_….yaml` is created with `uris: [uri_a, uri_b]`, `source`, and `timestamp`, and no existing file other than `index.yaml` changes

#### Scenario: Malformed merge
- **WHEN** a merge record lists one URI or three URIs
- **THEN** validation fails

#### Scenario: Field order matches the specification example
- **WHEN** an implementation writes a merge record carrying a `reason`
- **THEN** `reason` appears between `uris` and `source`

### Requirement: The core is three knowledge objects plus records
The specification SHALL state that particular, claim, and synthesis are the complete set of knowledge objects, and that the format additionally defines records — retraction, merge, and publish — which are events about objects rather than knowledge.

#### Scenario: Naive consumer
- **WHEN** a consumer implements only the three knowledge objects and ignores `/merges/`
- **THEN** it still reads every claim and synthesis correctly, merely without cross-particular unification

#### Scenario: Naive consumer and promotion
- **WHEN** a consumer ignores `/publishes/` as well
- **THEN** it still reads every claim correctly and treats each object's asserted scope as its effective scope
