## Why

Three items have stood in Status as open "before v0.1 is declared" since 2026-08-25, and nothing else is open anywhere: the signed payload's serialisation basis, the `.well-known` crawling protocol, and registration of the `urn:dkf:` namespace. Each is a decision rather than a discovery — the material to decide with has existed for days — and leaving them open is now the only thing between the draft and a declarable v0.1.

## What Changes

- **The signed payload is defined over the data model, not YAML bytes.** The payload for the reserved `signature` field is the object parsed to its data model, with `retracted` and `signature` removed, canonicalised per RFC 8785 (JSON Canonicalization Scheme). A signature therefore survives reformatting, field reordering, and the later appending of a retraction — none of which change what was asserted. Signature *suites* (algorithms, key formats, DID binding) remain reserved; v0.1 defines only what the bytes would be.
- **The false dependency is corrected. BREAKING** for the spec's own prior claim: canonical field order is *not* a prerequisite for signing and does not become mandatory for signed objects — under a data-model payload, file layout is irrelevant to the signature. Canonical order keeps its real rationale, which was always the stronger one: byte-identical files for identical knowledge, reviewable as git diffs.
- **Public discovery is specified as a publishing contract, and crawler behaviour is explicitly out of scope.** The manifest at `/.well-known/knowledge.yaml` carries `format`, `index`, and `feeds` (required), `topics` and `publisher` (optional), unknown keys ignored; paths resolve against the site root; every published object is fetchable at a feed path plus `<id>.yaml`; only objects whose effective scope is `public` are served, with the promotions feed letting a crawler verify that; the index is the enumeration and may lag. Fetch scheduling, deltas, and politeness are implementation concerns, named as such rather than left dangling.
- **`urn:dkf:` is declared deliberately unregistered at v0.1.** The syntax conforms to RFC 8141 (`dkf` is a valid NID), the workspace UUID embedded in every minted URN makes cross-authority collision practically impossible, and formal registration is post-v0.1 paperwork that would change no identifier. `base-uri` remains the recommended path for anyone publishing.
- **Status is rewritten** to list nothing as open before v0.1. Declaring v0.1 is left as a deliberate act for the maintainer, not a side effect of this change.

## Capabilities

### New Capabilities
- `public-discovery`: the manifest, path resolution, fetchability, the public-only rule, and the explicit descoping of crawler behaviour.

### Modified Capabilities
- `canonical-serialisation`: the signed payload becomes the JCS form of the data model; the order-mandatory-when-signed sentence is removed.
- `particular-uris`: the `urn:dkf:` namespace is stated as deliberately unregistered, with the collision argument and the registration-changes-nothing note.

## Impact

- `README.md` — Trust and Provenance (signing paragraph), Field order (the "prerequisite" sentence), Public Discovery (contract made normative), Minting URIs (registration paragraph), Status (rewritten).
- `openspec/specs/` — one capability added, two modified.
- `particulars-cli` — signing remains unimplemented there, so nothing shipped changes; the JCS choice tells it what a future `sign`/`verify` pair consumes. Its feeds and Graph export already serve only effective-scope-public objects.
- Ordering — this change originates from design review, not reported feedback: **posted for review before applying**, per the standing rule.
