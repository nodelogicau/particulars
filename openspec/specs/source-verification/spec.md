# Source Verification Specification

## Purpose

Defines the structured document reference a claim may carry, the verbatim quote that locates what was read, the drift states derived from comparing a quote and a document hash against the source today, and the best-effort rule that keeps unfetchable sources first-class.

## Requirements

### Requirement: A document reference may be structured
`source.document` MAY be either a string or a mapping with `ref` (required), `author` (optional), `hash` (optional), and `quote` (optional), written in that order. `ref` SHALL identify the source: a URI, a path resolved against the workspace root, or an identifier for a source that cannot be fetched at all, such as a conversation. Implementations MAY attempt to resolve a `ref` as a URI or as a workspace path, and where it resolves as neither the reference SHALL be treated as unverifiable rather than invalid — an unfetchable source may still carry a `quote`, which is provenance a reviewer can weigh. Readers SHALL accept `uri` as a legacy alias for `ref` and SHOULD warn, because a file carrying it can never be rewritten.

`author` SHALL identify who produced what was read, as a particular reference in the forms defined in `source-attribution`. It is distinct from `source.author`, which identifies who read it. An unresolvable `document.author` SHALL be reported as unresolved rather than invalid.

`hash` SHALL be an algorithm-prefixed digest taken over the document with CRLF sequences normalised to LF and nothing else altered: not trailing whitespace, not Unicode form, not a final newline. Writers SHOULD write `sha256`; readers SHALL accept any `<algorithm>:<digest>` and SHALL report an unrecognised algorithm as unverified rather than invalid.

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

#### Scenario: The stored quote keeps the shape it was given
- **WHEN** a writer supplies a quote containing a line break and two spaces of indentation
- **THEN** the claim file carries the quote with that line break and indentation, and the reader compares it under the whitespace rule without altering the file

#### Scenario: A writer is given an empty quote
- **WHEN** a writer is asked to record a `quote` that is empty or consists only of whitespace
- **THEN** the writer refuses it, as it would a `confidence` outside [0, 1]

#### Scenario: A reader meets an empty quote
- **WHEN** a claim file carries a `document` mapping whose `quote` folds to nothing
- **THEN** the reader verifies the reference as though the mapping carried no `quote`, warns, and does not report quote drift or reject the claim
### Requirement: The locator is a verbatim quote, not an offset
Where a claim records which part of a document it was drawn from, it SHALL do so as verbatim text in `quote`. The specification SHALL NOT define line, byte, or character offsets as a locator, because insertion elsewhere in a document moves an offset without changing what it points at.

#### Scenario: Text inserted above the quote
- **WHEN** a paragraph is added to the top of a cited document and the quoted text is unchanged
- **THEN** the quote is still found and no drift is reported for the quote

#### Scenario: Human audit without tooling
- **WHEN** a reviewer reads a claim and its `quote` in a pull request
- **THEN** they can compare the claim against the quoted text without fetching anything

### Requirement: Drift is determined from the quote and the document hash together
An implementation checking a structured reference SHALL evaluate whether the `quote` still appears in the fetched document and whether the `hash` still matches it, and SHALL report: no drift when both hold; **context drift** when the quote is present but the hash differs; and **quote drift** when the quote is absent, whether or not the hash differs. When the quote is absent and the hash still matches, the report SHOULD say that the quote has never matched the unchanged document, since a quote that is not in a document nobody has edited was miscopied or taken from another revision. When the mapping carries a `quote` but no `hash`, the quote is the whole signal: present SHALL be reported as no drift with the hash unverified, and absent as quote drift without the never-matched inference, because nothing says whether the document changed. Drift SHALL be reported as a condition for a reader to resolve, not as a validation error.

A quote **appears** in a document when, after folding both, the folded quote is a substring of the folded document. Folding SHALL replace every maximal run of characters having the Unicode `White_Space` property with a single U+0020 and SHALL strip leading and trailing whitespace; it SHALL alter nothing else. Case, punctuation, and Unicode normalisation form SHALL be compared verbatim: for everything other than whitespace, the quote SHALL agree with the hash about what constitutes an edit. Folding is a property of the comparison; the stored `quote` is never altered by it. The specification SHALL state that the rule is format-blind — it removes no blockquote marker, comment prefix, or other syntax from a continuation line — so a quote spanning such a line must be taken from within one line.

#### Scenario: Context changed around an unchanged quote
- **WHEN** a cited document is edited elsewhere and the quoted text is untouched
- **THEN** context drift is reported, because the surrounding text may have changed what the quote means

#### Scenario: The quoted text is gone
- **WHEN** the quoted text no longer appears in the cited document and the hash differs
- **THEN** quote drift is reported

#### Scenario: The quote never matched
- **WHEN** the quoted text does not appear in the cited document and the hash still matches
- **THEN** quote drift is reported, and the report says the quote has never matched the unchanged document

#### Scenario: Quote only, still present
- **WHEN** a `document` mapping carries a `quote` and no `hash`, and the quote appears in the document
- **THEN** no drift is reported, and the hash is reported as unverified

#### Scenario: Quote only, absent
- **WHEN** a `document` mapping carries a `quote` and no `hash`, and the quote does not appear in the document
- **THEN** quote drift is reported, without any claim about whether the document changed

#### Scenario: A quote spans a hard line wrap
- **WHEN** a document reads `the billing service listens\non 443` and a claim quotes `the billing service listens on 443`
- **THEN** the quote appears, and still appears after the document is re-wrapped at another column or checked out with CRLF line endings

#### Scenario: A quote spans a paragraph break
- **WHEN** a document holds two sentences separated by a blank line and a claim quotes both, separated by one space
- **THEN** the quote appears

#### Scenario: A non-breaking space folds
- **WHEN** a document reads `listens on 443` with a U+00A0 between `on` and `443`, and a claim quotes `listens on 443` with U+0020
- **THEN** the quote appears

#### Scenario: A quote written as a block scalar
- **WHEN** a `quote` is written as a YAML block scalar and so carries a trailing newline, and its text appears in the document
- **THEN** the quote appears

#### Scenario: A whitespace-only edit is context drift
- **WHEN** a claim quotes a tab-indented code block and the document is later re-indented with spaces and otherwise unchanged
- **THEN** the quote appears and context drift is reported, because the hash differs

#### Scenario: Words must still match
- **WHEN** a document reads `listens on 443` and a claim quotes `listens on 8443`
- **THEN** the quote is absent

#### Scenario: Case and punctuation are verbatim
- **WHEN** a document reads `The service listens on 443.` and a claim quotes `the service listens on 443`
- **THEN** the quote is absent, because the two differ in case, and the quote and the hash agree that this is an edit

#### Scenario: A wrapped blockquote does not fold
- **WHEN** a document reads `> the billing service listens\n> on 443` and a claim quotes `the billing service listens on 443`
- **THEN** the quote is absent, because folding removes whitespace and not the `>` on the continuation line

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
