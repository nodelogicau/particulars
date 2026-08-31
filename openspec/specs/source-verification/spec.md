# Source Verification Specification

## Purpose

Defines the structured document reference a claim may carry, the verbatim quote that locates what was read, the drift states derived from comparing a quote and a document hash against the source today, and the best-effort rule that keeps unfetchable sources first-class.

## Requirements

### Requirement: A document reference may be structured
`source.document` MAY be either a string or a mapping with `ref` (required), `author` (optional), `hash` (optional), and `quote` (optional), written in that order. `ref` SHALL identify the source: a URI, a path resolved against the workspace root, or an identifier for a source that cannot be fetched at all, such as a conversation. Implementations MAY attempt to resolve a `ref` as a URI or as a workspace path, and where it resolves as neither the reference SHALL be treated as unverifiable rather than invalid — an unfetchable source may still carry a `quote`, which is provenance a reviewer can weigh. Readers SHALL accept `uri` as a legacy alias for `ref` and SHOULD warn, because a file carrying it can never be rewritten.

`author` SHALL identify who produced what was read, as a particular reference in the forms defined in `source-attribution`. It is distinct from `source.author`, which identifies who read it. An unresolvable `document.author` SHALL be reported as unresolved rather than invalid.

`hash` SHALL be an algorithm-prefixed digest taken over the document with CRLF sequences normalised to LF and nothing else altered: not trailing whitespace, not Unicode form, not a final newline. Writers SHOULD write `sha256`; readers SHALL accept any `<algorithm>:<digest>` and SHALL report an unrecognised algorithm as unverified rather than invalid.

`quote` SHALL be verbatim text drawn from that document. Consumers SHALL accept the string form of `document` and SHALL NOT treat it as inferior provenance.

#### Scenario: Bare string reference
- **WHEN** a claim has `source: {author: ben, document: https://example.com/a.md}`
- **THEN** the claim is valid and no verification is attempted

#### Scenario: Structured reference
- **WHEN** a claim has a `document` mapping with `ref`, `hash`, and `quote`
- **THEN** the claim is valid and the reference is eligible for drift checking

#### Scenario: Reported testimony
- **WHEN** a claim has a `document` mapping with `ref: conversation with Jane, 2026-08-30`, `author: urn:dkf:01a0…:jane`, and a `quote`
- **THEN** the claim is valid, unverifiable, reported from Jane, and the quote stands as provenance

#### Scenario: Field order in the mapping
- **WHEN** an implementation writes a `document` mapping carrying all four fields
- **THEN** they appear in the order `ref`, `author`, `hash`, `quote`

#### Scenario: Workspace-relative reference
- **WHEN** a `document` mapping has `ref: docs/architecture.md`
- **THEN** it resolves against the workspace root, and hashing requires no network

#### Scenario: An unfetchable source with a quote
- **WHEN** a `document` mapping has `ref: chat session 2026-08-22` and a `quote`, with no `hash`
- **THEN** the claim is valid, the reference is unverifiable, and the quote stands as provenance

#### Scenario: Legacy `uri`
- **WHEN** a `document` mapping carries `uri` rather than `ref`
- **THEN** readers accept it as the reference and warn, because the file cannot be rewritten to use the new name

#### Scenario: Unrecognised hash algorithm
- **WHEN** a `hash` names an algorithm the consumer does not implement
- **THEN** the reference is reported as unverified, and the claim is not rejected

#### Scenario: Mapping without a reference
- **WHEN** a `document` mapping carries `author`, `hash` and `quote` but no `ref`
- **THEN** validation fails

#### Scenario: Line endings do not constitute drift
- **WHEN** the same document is hashed from a CRLF checkout and from an LF checkout
- **THEN** the two hashes agree, and no drift is reported

#### Scenario: Trailing whitespace does constitute drift
- **WHEN** a document is edited only by adding trailing whitespace to a line
- **THEN** the hash differs, because the change is an edit rather than an artefact of transport

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
