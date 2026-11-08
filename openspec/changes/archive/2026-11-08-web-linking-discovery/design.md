## Context

Public Discovery was made normative for v0.1 as a publishing contract: a manifest at a fixed path, predictable object paths, public-only feeds, and no crawl protocol. It answers "given a publisher, what do I fetch?" and not "given a thing, who publishes about it?". The second question is the one federation by shared URI depends on: two publishers pointing at the same URI are talking about the same thing only if a consumer can find both. It also leaves the manifest under an unregistered generic name and every DKF document without a media type, so there is nothing to put in a `type` attribute or a `Content-Type` header.

Nothing in the ecosystem serves a manifest yet. `particulars-cli`, `particulars-feeds` and `particulars-website` contain no reference to `/.well-known/knowledge.yaml`.

## Goals / Non-Goals

**Goals:** a registrable, DKF-specific manifest path; a media type that names DKF documents; a standard way for a URI's resource to point at the knowledge about it; all of it additive for workspace files.

**Non-Goals:** a crawl protocol, or any obligation to follow links. A new link relation. Media-type parameters. Content negotiation on a particular's URI. HTTP caching rules (`immutable`, ETags), which are a separate candidate change. Submitting either IANA registration. Any change to object files, the index, or `format`.

## Decisions

### D1. The manifest moves to `/.well-known/dkf.yaml`

RFC 8615 asks that well-known suffixes be registered, and a registry entry for `knowledge` would claim a word far wider than this format. `dkf.yaml` is DKF-specific, as `dkf.yaml` and `dkf.md` are at a workspace root, and it would be a reasonable thing to register.

Why `dkf.yaml` and not a bare `dkf`: static hosts derive the content type from the file extension and cannot be configured otherwise. GitHub Pages, which serves `particulars.fyi`, would serve an extensionless `dkf` as `application/octet-stream`. With the extension, every static host serves YAML, a host that can set headers serves `application/dkf+yaml`, and the path says what it is when someone reads it. `security.txt` (RFC 9116) is a registered suffix that carries an extension for the same reason.

*Alternatives:* keep `knowledge.yaml` and register it. That claims a generic word, and the rename is free only now. Use bare `dkf` with the media type carrying the format. That breaks on the commonest hosting for small publishers.

### D2. Consumers fall back to the old path, and report it

The rename is breaking in principle, because a publisher who followed the v0.1 text would no longer be found. A consumer therefore tries `/.well-known/dkf.yaml` and, only when that returns 404 or 410, `/.well-known/knowledge.yaml`. Finding the manifest at the old path is reported as a legacy compatibility fact, as the `uri` alias for `document.ref` is. Publishers write the new path only. Serving both is permitted, and the new one wins.

The fallback covers "not there" responses only, not every error: a 5xx or a timeout on the new path means the publisher's server is unwell, and probing a second path would hide that.

### D3. One media type, `application/dkf+yaml`, with no parameters

It covers object and record files, index documents (root, segments, legacy), and the manifest. All of them are YAML documents defined by this specification, and a consumer already tells them apart by where it fetched them and by `type`. Separate subtypes would multiply registrations to say what the path already says.

No `format` or `version` parameter. The layout is read from the index's `format`, and the spec's rule that a reader never infers the layout from what it finds would be weakened by a second source that can disagree with the first. A header set by a host is less trustworthy than the document it labels.

Consumers accept `application/yaml`, `text/yaml`, `application/x-yaml`, `text/plain` and `application/octet-stream` for a document fetched from a path the manifest or index names, because the path is what makes it a DKF document. A consumer rejects nothing on Content-Type alone. A `text/html` response is not rejected for its header; it is reported as not parsing as a DKF document, which is what it is.

The registration template follows RFC 6838 §5.6. Its security considerations are the ones the specification already imposes: no YAML anchors or aliases (alias expansion is a resource-exhaustion vector), no tags beyond the YAML 1.2 core schema, and no active content. Fragment identifiers are those of the `+yaml` suffix, with nothing added; object files carry no anchors, so in practice none resolve.

### D4. `describedby`, typed, pointing at a manifest

`describedby` is IANA-registered (from POWDER) and means exactly "the target describes the context". Paired with `type="application/dkf+yaml"`, it identifies a DKF manifest among any other descriptions a page links to, such as RDF or JSON-LD. This is why the media type and the link come in one change: without the type, the relation cannot be told apart.

The target is the **manifest**, not a particular file or a claim:
- Particular files are never served in a feed, and the specification depends on that.
- The manifest is the one stable entry point.
- From the manifest, a consumer reaches the index, the index's particular entries carry `uri`, and claims carry `subject`. Finding the claims about a URI is a lookup the consumer already knows how to do.

Linking to a claim would bypass the effective-scope filter that the feed contract exists to enforce.

Both serialisations are valid, and consumers treat them alike:
- **HTTP `Link` header:** works for any representation, including a non-HTML resource.
- **HTML `<link>`:** the only option on a host that cannot set headers.

The target may be on another origin. A person's particular URI is often a profile page on a site they don't control while their knowledge is published elsewhere, and that is the case where `/.well-known` on the same origin cannot help.

*Alternatives:* register a `dkf` relation, which needs a registration for something an existing relation already says. Use `alternate`, which claims the target is the same resource in another format, and a manifest is not that.

### D5. A link is the URI owner's pointer, not an endorsement of claims

A `describedby` link from a URI's resource is made by whoever controls that resource. It says "knowledge about me is here", and it is the one signal in this format that comes from the subject's side. It does not make the linked publisher's claims true, authoritative, or signed. Nor does its absence make another publisher's claims about the same URI any less admissible: Wikidata will never link to anyone's manifest. The specification says so, so that no consumer turns the link into a trust rule. Reasoning about it belongs with the other signals in Trust and Provenance.

## Risks / Trade-offs

- [A publisher on the v0.1 path is found only by consumers that implement the fallback] → No such publisher is known. The fallback is a SHALL, and finding the old path is reported, so it is visible rather than silent.
- [Jekyll-based GitHub Pages skips dot-directories, so `/.well-known/` is not published by default] → This was already true of the old path. The README notes the `include:` or `.nojekyll` fix where it describes hosting.
- [Media-type tolerance means the header carries no information for a consumer] → Intended. The header helps generic tooling and the `type` attribute on links, while DKF consumers rely on the path and the document. The rule "the document outranks the header" is the same as "the files outrank the index".
- [IANA could ask for changes, or decline, during expert review] → The registration changes no identifier that a document carries. A requested rename of the suffix would need a further change, and the fallback mechanism already exists for that.
- [Links multiply crawl surface] → Following them stays optional, and politeness stays a property of consumers.

## Migration Plan

Nothing to migrate in any workspace. A publisher serving the old path moves the file, or serves both during a transition. Rollback is reverting the README text: no file written under this change is read differently by an older consumer. The only effect is that an older consumer does not find a manifest at the new path.

## Open Questions

- Should the change also register a `profile` URI, so that `application/yaml; profile=…` works on hosts that can't set a custom type? Deferred: the tolerance rule already covers those hosts.
