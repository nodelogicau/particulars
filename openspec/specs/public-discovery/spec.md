# Public Discovery Specification

## Purpose

Defines the publishing contract for exposing DKF knowledge on the open internet — the well-known manifest, path resolution, fetchability of every published object, the effective-public-only rule with the promotions feed as verification — and deliberately defines no crawl protocol.

## Requirements

### Requirement: A publisher exposes a manifest at a well-known path
A publisher SHALL serve a manifest at `/.well-known/knowledge.yaml` carrying `format` (required), `index` (required), and `feeds` (required, a non-empty list); it MAY carry `topics` and `publisher`. Paths in the manifest SHALL resolve against the site root. Consumers SHALL ignore keys they do not understand.

#### Scenario: Minimal manifest
- **WHEN** a manifest carries only `format`, `index`, and `feeds`
- **THEN** it is valid and a consumer can enumerate the workspace

#### Scenario: Unknown manifest key
- **WHEN** a manifest carries a key this specification does not define
- **THEN** consumers ignore it

### Requirement: Every published object is fetchable at a predictable path
Every object served in a feed SHALL be fetchable at a predictable path derived from its id and the workspace's declared format: for a `dkf/0.1` publisher, the feed path plus `<id>.yaml`; for a `dkf/0.2` publisher, the feed path plus `<YYYY-MM>/<id>.yaml`, where the month is derived from the id as `workspace-layout` defines. A consumer SHALL take the format from the index named by the manifest. The index named by the manifest SHALL enumerate every published object, and in a `dkf/0.2` workspace SHALL be the root index, whose `segments` paths resolve relative to the index's own URL. Remote consumers SHALL treat the index as potentially lagging the files.

#### Scenario: Fetching an enumerated claim
- **WHEN** a `dkf/0.1` index lists a claim and the manifest lists `/knowledge/claims/`
- **THEN** the claim is fetchable at `/knowledge/claims/<id>.yaml`

#### Scenario: Fetching a sharded claim
- **WHEN** a `dkf/0.2` index lists a claim whose id was minted in September 2026 and the manifest lists `/knowledge/claims/`
- **THEN** the claim is fetchable at `/knowledge/claims/2026-09/<id>.yaml`, with no lookup beyond the id

#### Scenario: Fetching a sealed segment
- **WHEN** the manifest names `/knowledge/index.yaml` and that root lists `index/2026-08.yaml` under `segments`
- **THEN** the segment is fetchable at `/knowledge/index/2026-08.yaml`

#### Scenario: Lagging index
- **WHEN** an object file is published before the index is regenerated
- **THEN** a consumer that misses it is not wrong, merely behind
### Requirement: Only public effective scope is served
A feed SHALL serve only objects whose effective scope is `public`. Serving the promotions feed lets a consumer verify effective scope for itself; a publisher that omits it asks to be trusted on the filtering.

#### Scenario: A promoted claim is served
- **WHEN** a claim asserted `personal` is covered by a non-retracted promotion to `public`
- **THEN** it appears in the feed

#### Scenario: A private export is not a feed
- **WHEN** an implementation serves organisation-scope knowledge to an authenticated surface, such as a tenant search index
- **THEN** that surface is not bound by this contract, which governs publishing to the open internet

#### Scenario: A narrow claim is not
- **WHEN** an object's effective scope is `organisation`
- **THEN** it appears in no feed, whatever the index says

### Requirement: Crawler behaviour is out of scope
The specification SHALL state that fetch scheduling, change detection, and politeness are properties of consumers, not of the format, and defines no crawl protocol. Index `timestamp` fields MAY be used for incremental fetching.

#### Scenario: A considered omission
- **WHEN** an implementer looks for a crawl protocol
- **THEN** the specification says the publishing contract is the whole contract, and the omission is deliberate
