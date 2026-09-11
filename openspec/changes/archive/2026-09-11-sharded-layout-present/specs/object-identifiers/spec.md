## MODIFIED Requirements

### Requirement: Object identifiers are prefixed UUIDv7
Every DKF object and record id SHALL be formed as `<prefix>_` followed by a lowercase canonical RFC 9562 UUID version 7, where `<prefix>` is `par` (particular), `clm` (claim), `syn` (synthesis), `mrg` (merge), or `pub` (publish). An id's instant is its position in the workspace's log, not a reading of the writer's clock: minting implementations SHALL ensure ids created within the same millisecond sort in creation order (e.g. via a monotonic counter), and SHALL NOT mint an id earlier than the newest id already in the workspace, advancing the instant to just after that id when the writer's clock is behind it. Assertion time is the object's `timestamp`, and consumers SHALL NOT require the two to agree.

#### Scenario: Minting a new claim id
- **WHEN** an implementation creates a new claim
- **THEN** the id matches `^clm_[0-9a-f]{8}-[0-9a-f]{4}-7[0-9a-f]{3}-[89ab][0-9a-f]{3}-[0-9a-f]{12}$`

#### Scenario: Ids minted in the same millisecond
- **WHEN** two claims are minted within one millisecond by the same implementation
- **THEN** lexical ordering of their ids matches creation order

#### Scenario: Minting a promotion id
- **WHEN** an implementation records a promotion
- **THEN** the id carries the `pub` prefix

#### Scenario: Minting behind the workspace
- **WHEN** the newest id in the workspace was minted at an instant later than the writer's clock
- **THEN** the writer mints at an instant just after that id, and lexical ordering of ids in the workspace still matches creation order

#### Scenario: Minting ahead of the workspace
- **WHEN** the writer's clock is later than every id in the workspace
- **THEN** the writer mints at its own clock
