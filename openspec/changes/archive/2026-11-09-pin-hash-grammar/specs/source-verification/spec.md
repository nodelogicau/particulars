## MODIFIED Requirements

### Requirement: A document reference may be structured
`source.document` MAY be either a string or a mapping with `ref` (required), `author` (optional), `hash` (optional), and `quote` (optional), written in that order. `ref` SHALL identify the source: a URI, a path resolved against the workspace root, or an identifier for a source that cannot be fetched at all, such as a conversation. Implementations MAY attempt to resolve a `ref` as a URI or as a workspace path, and where it resolves as neither the reference SHALL be treated as unverifiable rather than invalid — an unfetchable source may still carry a `quote`, which is provenance a reviewer can weigh. Readers SHALL accept `uri` as a legacy alias for `ref` and SHOULD warn, because a file carrying it can never be rewritten.

`author` SHALL identify who produced what was read, as a particular reference in the forms defined in `source-attribution`. It is distinct from `source.author`, which identifies who read it. An unresolvable `document.author` SHALL be reported as unresolved rather than invalid.

`hash` SHALL be an algorithm-prefixed digest, in the grammar and canonical form of *A hash has one grammar and a canonical form*, taken over the document with CRLF sequences normalised to LF and nothing else altered: not trailing whitespace, not Unicode form, not a final newline. Writers SHALL write `sha256`. Readers SHALL report an algorithm they do not implement as unverified rather than invalid, and SHALL read a malformed hash as described in *A malformed hash is read as no hash*.

`quote` SHALL be verbatim text drawn from that document, written as given: an implementation SHALL NOT fold, trim, or otherwise normalise the stored quote. A writer SHALL NOT write a quote that folds to nothing under the whitespace rule of *Drift is determined from the quote and the document hash together*; a reader that meets one SHALL treat the mapping as carrying no quote and SHOULD warn. Consumers SHALL accept the string form of `document` and SHALL NOT treat it as inferior provenance.

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
- **WHEN** a `hash` matches the grammar and names an algorithm the consumer does not implement, such as `blake3:…`
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

#### Scenario: The stored quote keeps the shape it was given
- **WHEN** a writer supplies a quote containing a line break and two spaces of indentation
- **THEN** the claim file carries the quote with that line break and indentation, and the reader compares it under the whitespace rule without altering the file

#### Scenario: A writer is given an empty quote
- **WHEN** a writer is asked to record a `quote` that is empty or consists only of whitespace
- **THEN** the writer refuses it, as it would a `confidence` outside [0, 1]

#### Scenario: A reader meets an empty quote
- **WHEN** a claim file carries a `document` mapping whose `quote` folds to nothing
- **THEN** the reader verifies the reference as though the mapping carried no `quote`, warns, and does not report quote drift or reject the claim

## ADDED Requirements

### Requirement: A hash has one grammar and a canonical form
A `hash` SHALL match the OCI image-spec digest grammar: `algorithm ":" encoded`, where `algorithm` is one or more components `[a-z0-9]+` joined by single separators from `+`, `.`, `_`, `-`, and `encoded` is `[a-zA-Z0-9=_-]+`. Two algorithms are registered: `sha256`, whose encoded part SHALL be 64 hexadecimal digits, and `sha512`, whose encoded part SHALL be 128. Readers SHALL implement `sha256` and MAY implement `sha512`. The encoded part of any other algorithm is opaque and SHALL NOT be interpreted.

A hash is in **canonical form** when it names a registered algorithm in lowercase with lowercase hexadecimal digits of the registered length, or names an unregistered algorithm and matches the grammar. Writers SHALL write canonical form and SHALL refuse a hash that is not in it, naming the canonical form, rather than normalising what they were given.

For the registered algorithms, readers SHALL also accept hexadecimal digits in either case, an algorithm name in any case, and the spellings `sha-256` and `sha-512` in any case, as `sha256` and `sha512`. No other alias is recognised. Readers SHALL compare such a hash with a computed one by algorithm and digest value, case-insensitively in the hexadecimal digits. A reader that accepts a hash not in canonical form SHALL report `hash_noncanonical` as a fact about the corpus, in aggregate.

#### Scenario: A canonical hash
- **WHEN** a `document` mapping carries `hash: sha256:` followed by 64 lowercase hexadecimal digits
- **THEN** the hash is in canonical form and is compared with the document's computed digest

#### Scenario: Uppercase hexadecimal from another writer
- **WHEN** a claim file carries a `sha256` hash whose 64 hexadecimal digits are uppercase, and the document's digest has the same value
- **THEN** the reader reports no drift from the hash, and reports `hash_noncanonical` in aggregate rather than against the claim

#### Scenario: The IANA spelling
- **WHEN** a claim file carries `hash: SHA-256:` followed by a 64-digit digest
- **THEN** the reader treats it as `sha256`, compares it by value, and reports `hash_noncanonical`

#### Scenario: An unrecognised alias
- **WHEN** a claim file carries `hash: sha2-256:` followed by a 64-digit digest
- **THEN** the reader treats `sha2-256` as an unregistered algorithm and reports the reference as unverified, not as `sha256`

#### Scenario: A writer is given a non-canonical hash
- **WHEN** a writer is asked to record `sha256:` with 64 uppercase hexadecimal digits
- **THEN** the writer refuses it and names the canonical form, lowercase hexadecimal, rather than lowercasing it silently

### Requirement: A malformed hash is read as no hash
A `hash` SHALL be **malformed** when it does not match the grammar, or when it names a registered algorithm (after accepting the aliases and case of *A hash has one grammar and a canonical form*) and its encoded part is not hexadecimal or not the registered length. Writers SHALL refuse a malformed hash. A reader that meets one SHALL verify the reference as though the mapping carried no `hash`: by the `quote` alone where there is one, as the drift rules define for a quote with no hash, and otherwise as unverified. It SHALL report `hash_malformed` as a finding about the object. A malformed hash SHALL NOT be reported as drift and SHALL NOT fail validation, because the file cannot be rewritten. Redacting `source.document.hash` in a `dkf/0.3` workspace clears the finding.

#### Scenario: A truncated digest
- **WHEN** a claim file carries `hash: sha256:9f2a` and a `quote` that appears in the document
- **THEN** the reader reports no drift, reports the hash as unverified, and reports `hash_malformed` against the claim; it reports no context drift

#### Scenario: Base64 under a hexadecimal algorithm
- **WHEN** a claim file carries `sha256:` followed by a base64 digest
- **THEN** the hash is malformed, and the reference is verified by its quote alone, or is unverified if it has none

#### Scenario: No algorithm prefix
- **WHEN** a claim file carries `hash: 9f2a…` with no `:`
- **THEN** the hash is malformed and the claim is valid

#### Scenario: Validation does not fail
- **WHEN** a workspace validates and one claim carries a malformed hash
- **THEN** validation reports `hash_malformed` against that claim and does not fail

#### Scenario: Redaction clears it
- **WHEN** `source.document.hash` is redacted from a claim whose hash was malformed, in a `dkf/0.3` workspace
- **THEN** `hash_malformed` is no longer reported, and no drift is reported for the redacted hash
