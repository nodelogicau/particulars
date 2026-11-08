# Public Discovery Specification

## Purpose

Defines the publishing contract for exposing DKF knowledge on the open internet — the well-known manifest at `/.well-known/dkf.yaml` with its legacy fallback, `describedby` links from a resource to the manifest that describes it, path resolution, fetchability of every published object, the effective-public-only rule with the promotions feed as verification — and deliberately defines no crawl protocol.

## Requirements

### Requirement: A publisher exposes a manifest at a well-known path
A publisher SHALL serve a manifest at `/.well-known/dkf.yaml` carrying `format` (required), `index` (required), and `feeds` (required, a non-empty list); it MAY carry `topics` and `publisher`. Paths in the manifest SHALL resolve against the site root. Consumers SHALL ignore keys they do not understand. A publisher SHALL NOT write a manifest only at `/.well-known/knowledge.yaml`; it MAY serve one there as well during a transition, and where both exist the manifest at `/.well-known/dkf.yaml` SHALL govern.

#### Scenario: Minimal manifest
- **WHEN** a manifest at `/.well-known/dkf.yaml` carries only `format`, `index`, and `feeds`
- **THEN** it is valid and a consumer can enumerate the workspace

#### Scenario: Unknown manifest key
- **WHEN** a manifest carries a key this specification does not define
- **THEN** consumers ignore it

#### Scenario: Both paths served
- **WHEN** a publisher serves manifests at both `/.well-known/dkf.yaml` and `/.well-known/knowledge.yaml` and they differ
- **THEN** a consumer uses the one at `/.well-known/dkf.yaml`

### Requirement: Consumers fall back to the legacy manifest path
A consumer looking for a publisher's manifest SHALL request `/.well-known/dkf.yaml` first. Only when that request returns 404 (Not Found) or 410 (Gone) SHALL it request `/.well-known/knowledge.yaml`. A manifest found only at the legacy path SHALL be used, and SHALL be reported as a legacy compatibility fact, in aggregate across the publishers a consumer has found that way. Any other failure on the new path, such as a 5xx status, a timeout or a TLS error, SHALL NOT trigger the fallback.

#### Scenario: A publisher on the v0.1 path
- **WHEN** `/.well-known/dkf.yaml` returns 404 and `/.well-known/knowledge.yaml` returns a valid manifest
- **THEN** the consumer uses that manifest and reports that the publisher is on the legacy path

#### Scenario: A failing server is not probed twice
- **WHEN** `/.well-known/dkf.yaml` returns 503
- **THEN** the consumer does not request `/.well-known/knowledge.yaml`, and reports the manifest as unreachable rather than absent

### Requirement: The well-known suffix is prepared for registration
The specification SHALL state that `dkf.yaml` is intended for registration in the IANA "Well-Known URIs" registry under RFC 8615, and SHALL carry the registration template: URI suffix `dkf.yaml`; change controller, the specification's maintainers; specification document, this specification's Public Discovery section; status, permanent; related information, the `application/dkf+yaml` media type. Until registration, the suffix is used unregistered, and registration SHALL change no published path.

#### Scenario: An implementer checks the registry
- **WHEN** an implementer looks up `dkf.yaml` in the Well-Known URIs registry before it is registered
- **THEN** the specification says the suffix is not yet registered, that registration is intended, and that it changes no path

### Requirement: A resource can point at the knowledge about it
The resource identified by a published particular's `https` URI, or any other web page, MAY carry a link with relation `describedby` and `type="application/dkf+yaml"` whose target is a DKF manifest. The link SHALL be expressible either as an HTTP `Link` header field (RFC 8288) or as an HTML `<link rel="describedby" type="application/dkf+yaml" href="…">` element, and consumers SHALL treat the two as equivalent. The target SHALL be a manifest, not an object, record or index document, and MAY be on another origin. A relative target SHALL resolve as RFC 8288 or HTML defines for its serialisation. A page MAY carry several such links. A publisher that controls the representation served at a particular's URI SHOULD carry one for each manifest that publishes claims about that particular. Following such links is a consumer's choice: this specification still defines no crawl protocol.

#### Scenario: A link header on a particular's URI
- **WHEN** a consumer fetches `https://example.com/particulars/project-x` and the response carries `Link: <https://example.com/.well-known/dkf.yaml>; rel="describedby"; type="application/dkf+yaml"`
- **THEN** the consumer can fetch that manifest, read its index, and find the particular entry whose `uri` is `https://example.com/particulars/project-x`, along with the published claims whose `subject` is that particular

#### Scenario: An HTML link on a profile page
- **WHEN** a person's particular URI is a profile page whose host cannot set headers, and the page carries `<link rel="describedby" type="application/dkf+yaml" href="https://knowledge.example.org/.well-known/dkf.yaml">`
- **THEN** a consumer treats it exactly as the equivalent `Link` header, and the cross-origin target is valid

#### Scenario: A describedby link of another type
- **WHEN** a page carries `rel="describedby"` with `type="text/turtle"`
- **THEN** a DKF consumer does not treat its target as a manifest

#### Scenario: A link to an object file
- **WHEN** a `describedby` link typed `application/dkf+yaml` targets a claim file rather than a manifest
- **THEN** a consumer does not treat the claim as discovered through the link, because feeds, not links, decide what is published

### Requirement: A link is not an endorsement of claims
The specification SHALL state that a `describedby` link is the linking resource's pointer to knowledge about it. It SHALL NOT be treated as making the linked publisher's claims true, authoritative or verified. Its absence SHALL NOT make claims about that URI, published by any publisher, less admissible. A consumer MAY record which manifests a URI's own resource links to, as a signal alongside the others in Trust and Provenance.

#### Scenario: Claims about a URI that links nowhere
- **WHEN** two publishers publish claims about `https://www.wikidata.org/entity/Q42`, whose resource carries no `describedby` link to either
- **THEN** both publishers' claims are admissible on equal terms, as they were before linking existed

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
