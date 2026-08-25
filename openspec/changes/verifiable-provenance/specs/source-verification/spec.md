## ADDED Requirements

### Requirement: A document reference may be structured
`source.document` MAY be either a URI string or a mapping with `uri` (required), `hash` (optional), and `quote` (optional). `hash` SHALL be an algorithm-prefixed digest of the document as fetched, for example `sha256:9f2a…`. `quote` SHALL be verbatim text drawn from that document. Consumers SHALL accept the string form and SHALL NOT treat it as inferior provenance.

#### Scenario: Bare string reference
- **WHEN** a claim has `source: {author: ben, document: https://example.com/a.md}`
- **THEN** the claim is valid and no verification is attempted

#### Scenario: Structured reference
- **WHEN** a claim has a `document` mapping with `uri`, `hash`, and `quote`
- **THEN** the claim is valid and the reference is eligible for drift checking

#### Scenario: Mapping without a URI
- **WHEN** a `document` mapping carries `hash` and `quote` but no `uri`
- **THEN** validation fails

### Requirement: The locator is a verbatim quote, not an offset
Where a claim records which part of a document it was drawn from, it SHALL do so as verbatim text in `quote`. The specification SHALL NOT define line, byte, or character offsets as a locator, because insertion elsewhere in a document moves an offset without changing what it points at.

#### Scenario: Text inserted above the quote
- **WHEN** a paragraph is added to the top of a cited document and the quoted text is unchanged
- **THEN** the quote is still found and no drift is reported for the quote

#### Scenario: Human audit without tooling
- **WHEN** a reviewer reads a claim and its `quote` in a pull request
- **THEN** they can compare the claim against the quoted text without fetching anything

### Requirement: Drift is determined from the quote and the document hash together
An implementation checking a structured reference SHALL evaluate whether the `quote` still appears in the fetched document and whether the `hash` still matches it, and SHALL report: no drift when both hold; **context drift** when the quote is present but the hash differs; and **quote drift** when the quote is absent. Drift SHALL be reported as a condition for a reader to resolve, not as a validation error.

#### Scenario: Context changed around an unchanged quote
- **WHEN** a cited document is edited elsewhere and the quoted text is untouched
- **THEN** context drift is reported, because the surrounding text may have changed what the quote means

#### Scenario: The quoted text is gone
- **WHEN** the quoted text no longer appears in the cited document
- **THEN** quote drift is reported

#### Scenario: Drift does not invalidate
- **WHEN** a workspace contains claims whose sources have drifted
- **THEN** validation does not fail on that basis and the claims remain readable and citable

### Requirement: Verification is best-effort
No requirement SHALL oblige a consumer to fetch a document. Where a source cannot be fetched, hashed, or quoted — a conversation, a recollection, an access-controlled page — the claim SHALL remain fully valid and its provenance SHALL be reported as unverified rather than absent or invalid.

#### Scenario: Claim from a conversation
- **WHEN** a claim records `source: {author: ben}` with no document at all
- **THEN** it is valid, and any provenance report describes it as unverified

#### Scenario: Validator without network access
- **WHEN** validation runs offline over claims carrying hashes
- **THEN** it reports those references as not checked, and does not fail

### Requirement: A quote carries source text and is subject to disclosure review
Because a `quote` reproduces source text verbatim inside the claim file, an object's effective scope governs the exposure of that text. Implementations SHOULD warn when a claim's effective scope is wider than the scope of the material it quotes where that is known, and the specification SHALL state that a verbatim quote discloses its source completely rather than in summary.

#### Scenario: Public claim quoting private material
- **WHEN** a claim scoped `public` carries a quote drawn from a document the author treats as private
- **THEN** the implementation warns, and does not reject the claim

#### Scenario: Quote exposure is total
- **WHEN** a reader evaluates what a published claim reveals about its source
- **THEN** the specification tells them a quote reproduces the source exactly, unlike a synthesis which summarises
