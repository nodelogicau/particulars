## Context

The three blockers differ in kind. The signing basis is a genuine design fork with consequences either way. The crawling protocol is a scoping decision — what does interop actually require. The URN registration is a decision about whether paperwork gates a release. All three have been waiting on a decision, not on information.

## Goals / Non-Goals

**Goals:** nothing left in Status; each closure honest about what it defers.
**Non-Goals:** signature suites, key management, or DID resolution; crawler scheduling or delta protocols; actually submitting an IANA registration; declaring v0.1 (the maintainer's act, not this change's side effect).

## Decisions

### D1. The signed payload is the JCS form of the data model

Sign the object as parsed — mappings, arrays, strings, numbers — with `retracted` and `signature` removed, canonicalised per RFC 8785. Not the file bytes.

Byte-signing fails three ways. It requires pinning a complete YAML emission style — quoting, indentation, wrapping, block-scalar forms — which is a specification several times larger than this one's whole serialisation section, for a format whose readers MUST already accept any field order. It makes verification of a retracted object depend on byte-exact reconstruction of the pre-retraction file, which is fragile in exactly the place provenance must not be. And it breaks on cosmetic reformatting, converting an editor's whitespace pass into signature invalidation.

The data-model payload has the dual properties: a signature survives reformatting, reordering, and retraction-appending, because none of them change what was asserted; and two writers producing the same knowledge produce the same payload regardless of style, because JCS's key ordering and ES6 number serialisation are deterministic (`0.90` and `0.9` parse to the same number and sign identically — the same reasoning as CRLF/LF in the document hash: normalise what is an artefact, sign what is asserted).

Mapping rules the spec must state: keys are strings; values are strings, numbers, booleans, arrays, mappings; every field the specification defines as textual — timestamps, ids, URIs — is a string in the data model even where a YAML parser would type it otherwise; `confidence` is a number. YAML anchors, aliases, and non-string keys have no canonical form and MUST NOT appear in objects.

*Cost accepted:* verification requires a JCS implementation rather than `sha256sum` over a filtered file. JCS is a small RFC with implementations in every mainstream language, and the CRLF precedent already conceded that raw bytes are the wrong thing to fix on.

### D2. The prerequisite claim was wrong, and this change says so

The #11 round justified canonical field order partly as "a prerequisite for signing", and `canonical-serialisation` requires that order become mandatory for signed objects. Under D1 both are false: the payload is derived from the data model, so file order never touches it. The sentences are removed rather than reinterpreted, and the correction is recorded here: canonical order's surviving rationale — byte-identical files for identical knowledge, reviewable as diffs — was always the stronger half, and #11's determinism argument was really about the *hash* (which does cover bytes), not the signature. Conflating the two artefacts of determinism was the error.

### D3. Discovery is a publishing contract; crawling is not a protocol this format owns

What a consumer needs to interoperate: where the manifest is, what it must contain, how paths resolve, that every published object is fetchable at a predictable path, that only effective-scope-`public` is served, and that the index enumerates but may lag. That is the whole contract, and it is normative here.

What is deliberately not specified: how often to fetch, how to detect changes cheaply, how to be polite. Those are properties of crawlers, not of the format — the format's own analogues (`.ics`, RSS) succeeded by specifying the artefact and leaving the fetching to HTTP. Index `timestamp` fields already give an implementation everything incremental fetching needs without a protocol. Named as out of scope so the omission reads as considered.

### D4. Unregistered, deliberately, and said aloud

`urn:dkf:` stays unregistered at v0.1. Three facts make this safe to say rather than embarrassing to admit: the NID syntax already conforms to RFC 8141, so nothing would change shape under registration; every minted URN embeds the workspace UUID, so collision with any other use of a `dkf` NID requires a UUID collision; and the spec already steers publishers to `base-uri`, with merge records existing precisely to join a URN to a later public URI. Registration becomes post-v0.1 paperwork with zero migration. The alternative — gating v0.1 on an IANA expert-review cycle — spends the project's momentum on a queue it does not control.

## Risks / Trade-offs

- [JCS ties the payload to JSON's data model] → DKF objects are already JSON-representable by construction; the mapping rules close the YAML-typing gap.
- [Removing the order-mandatory rule weakens pressure to emit canonical order] → The diff-review rationale stands, the hash still covers bytes, and a SHOULD that was doing its work through a false justification was borrowed strength anyway.
- [A publishing contract without a crawl protocol may fragment crawlers] → Accepted; fragmented fetching strategies over one artefact contract is how every syndication format works.
- [Someone else registers `dkf`] → Their URNs cannot collide with minted ones (UUID), and the spec's claim sentence documents priority of use.

## Open Questions

- None left deliberately. This change exists to end the list.
