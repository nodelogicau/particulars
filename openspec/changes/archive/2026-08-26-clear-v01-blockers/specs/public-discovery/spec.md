## ADDED Requirements

### Requirement: A publisher exposes a manifest at a well-known path
A publisher SHALL serve a manifest at `/.well-known/knowledge.yaml` carrying `format` (required), `index` (required), and `feeds` (required, a non-empty list); it MAY carry `topics` and `publisher`. Paths in the manifest SHALL resolve against the site root. Consumers SHALL ignore keys they do not understand.

#### Scenario: Minimal manifest
- **WHEN** a manifest carries only `format`, `index`, and `feeds`
- **THEN** it is valid and a consumer can enumerate the workspace

#### Scenario: Unknown manifest key
- **WHEN** a manifest carries a key this specification does not define
- **THEN** consumers ignore it

### Requirement: Every published object is fetchable at a predictable path
Every object served in a feed SHALL be fetchable at a feed path plus `<id>.yaml`. The index named by the manifest SHALL enumerate every published object, and remote consumers SHALL treat it as potentially lagging the files.

#### Scenario: Fetching an enumerated claim
- **WHEN** the index lists a claim and the manifest lists `/knowledge/claims/`
- **THEN** the claim is fetchable at `/knowledge/claims/<id>.yaml`

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
