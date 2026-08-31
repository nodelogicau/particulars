## MODIFIED Requirements

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
