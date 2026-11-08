## Why

A particular's `https://` URI must be resolvable once published, but the specification never says what a consumer finds when it resolves one. Nothing leads from a particular's page to the knowledge published about it, and the one fixed entry point — `/.well-known/knowledge.yaml` — is a generic name that RFC 8615 expects to be registered and nobody has. Three existing standards close this. They need no new file format, and the rename is cheapest now, while no publisher, consumer or tool in the ecosystem serves or reads the old path.

## What Changes

- **The manifest moves to `/.well-known/dkf.yaml`. BREAKING** for the discovery contract only: no workspace file, index document, or `format` value changes. Consumers SHALL fall back to `/.well-known/knowledge.yaml` when the new path is absent, and report that they did, so that a publisher following the earlier text is still found. The specification states its intention to register the suffix under RFC 8615 and carries the registration template. As with `urn:dkf:`, submitting the registration is left to the maintainer.
- **A media type, `application/dkf+yaml`, is defined** under the `+yaml` structured suffix of RFC 9512. It covers every DKF document: objects, records, index documents and the manifest. It has no parameters: a document's `format` is still read from the document or its index, never from a header. Publishers SHOULD serve it where they control headers. Consumers SHALL NOT reject a document because a static host labelled it `application/yaml`, `text/yaml`, `text/plain` or `application/octet-stream`. The specification carries the RFC 6838 registration template.
- **Particular URIs and publisher pages advertise DKF knowledge with Web Linking (RFC 8288).** The resource at a published particular's URI, or any page, MAY carry `rel="describedby"` with `type="application/dkf+yaml"` pointing at a manifest, either as an HTTP `Link` header or as an HTML `<link>`. The two are equivalent and consumers accept either. The manifest may be on another origin, which is the case the link exists for. This uses an IANA-registered relation and defines no new one. Following links is a consumer's choice, and crawling stays out of scope.
- **References and Status** gain RFC 8288, RFC 8615, RFC 9512 and RFC 6838, and an entry for this change.

## Capabilities

### New Capabilities
- `media-type`: the `application/dkf+yaml` media type — what it covers, the absence of parameters, encoding, consumer tolerance of generic YAML labels, and the registration template.

### Modified Capabilities
- `public-discovery`: the manifest path becomes `/.well-known/dkf.yaml`, with a legacy fallback and an RFC 8615 registration template. New requirements cover the `describedby` link from particular URIs and pages to a manifest, and the content types a consumer accepts.

## Impact

- `README.md`: Public Discovery (new path, linking, media type), References (four RFCs), Status (an additive-except-the-path entry).
- `openspec/specs/`: `public-discovery` modified, `media-type` added.
- `particulars-cli`, `particulars-feeds`, `particulars-website`: none of them serves or reads the old manifest path today, so nothing shipped breaks. A future publish or feed step writes `/.well-known/dkf.yaml` and, where its host allows, sets the media type and `Link` headers.
- IANA: two registrations (well-known suffix, media type) are prepared, not submitted, by this change.
- Ordering: this change comes from design review, not reported feedback, so it is **posted for review before applying**.
