## MODIFIED Requirements

### Requirement: Object identifiers are prefixed UUIDv7
Every DKF object and record id SHALL be formed as `<prefix>_` followed by a lowercase canonical RFC 9562 UUID version 7, where `<prefix>` is `par` (particular), `clm` (claim), `syn` (synthesis), `mrg` (merge), or `pub` (publish). Minting implementations SHALL ensure ids created within the same millisecond sort in creation order (e.g. via a monotonic counter). An id's instant is a reading of the minting implementation's clock; assertion time is the object's `timestamp`, and consumers SHALL NOT require the two to agree.

#### Scenario: Minting a new claim id
- **WHEN** an implementation creates a new claim
- **THEN** the id matches `^clm_[0-9a-f]{8}-[0-9a-f]{4}-7[0-9a-f]{3}-[89ab][0-9a-f]{3}-[0-9a-f]{12}$`

#### Scenario: Ids minted in the same millisecond
- **WHEN** two claims are minted within one millisecond by the same implementation
- **THEN** lexical ordering of their ids matches creation order

#### Scenario: Minting a promotion id
- **WHEN** an implementation records a promotion
- **THEN** the id carries the `pub` prefix

#### Scenario: Two writers with different clocks
- **WHEN** two implementations on different machines mint ids in the same hour with clocks a minute apart
- **THEN** each id carries its own machine's instant, and the workspace's layout tolerates the disagreement through the sealing grace period defined in `workspace-layout`
