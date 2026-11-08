## 1. Review

- [x] 1.1 Post the proposal for review before applying (design-review origin, per the standing rule); fold in feedback — reviewed by the maintainer, who asked to apply

## 2. README — Public Discovery

- [x] 2.1 Change the manifest example and prose to `/.well-known/dkf.yaml`; state that publishers write the new path only and that, where both exist, the new one governs
- [x] 2.2 Add the consumer fallback: try `dkf.yaml`, then `knowledge.yaml` only on 404/410; never on 5xx or a timeout; report finding the legacy path in aggregate
- [x] 2.3 Add a "Linking to knowledge" subsection: `rel="describedby"` + `type="application/dkf+yaml"`, as a `Link` header and as an HTML `<link>`, the target being a manifest that may be on another origin, with an example of each
- [x] 2.4 State that a link is the resource owner's pointer, not an endorsement, and that its absence makes no claims less admissible (the Wikidata case)
- [x] 2.5 Add the RFC 8615 registration template for `dkf.yaml`, and say it is unregistered for now and that registration changes no path
- [x] 2.6 Note the GitHub Pages / Jekyll dot-directory caveat (`include: [".well-known"]` or `.nojekyll`)

## 3. README — Media type

- [x] 3.1 Add a "Media type" subsection defining `application/dkf+yaml` for objects, records, index documents and the manifest, with no parameters, UTF-8, and `format` read from documents, never from headers
- [x] 3.2 State consumer tolerance of `application/yaml`, `text/yaml`, `application/x-yaml`, `text/plain`, `application/octet-stream` and a missing type, and that the path makes the document DKF
- [x] 3.3 Add the RFC 6838 registration template, with security considerations cross-referencing the existing anchors/aliases rule in Trust and Provenance

## 4. README — References and Status

- [x] 4.1 Add RFC 8288 (Web Linking), RFC 8615 (Well-Known URIs), RFC 9512 (YAML media type and `+yaml` suffix) and RFC 6838 (media type registration) under "Standards borrowed as grammars"
- [x] 4.2 Add a Status entry: the manifest path rename (breaking for discovery only, with a fallback, and no file or `format` affected), plus linking and the media type as additive

## 5. Verify

- [x] 5.1 Check that no other README section or `openspec/specs/*` text still names `/.well-known/knowledge.yaml` except as the legacy path
- [x] 5.2 Run `openspec validate web-linking-discovery --strict` and fix any findings
- [x] 5.3 Open follow-up issues on `particulars-cli` / `particulars-feeds` for writing the new path, setting the media type and `Link` headers when publishing (link them from the PR) — nodelogicau/particulars-cli#30; `particulars-feeds` is a local workspace with no repository, so it needs none
