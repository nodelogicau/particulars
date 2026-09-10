## MODIFIED Requirements

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
