## Why

`particular_define` without a `uri` mints `<base-uri><slug>` or `urn:dkf:<workspace-id>:<slug>`, where the slug keeps only `[a-z0-9]` after folding. A label with none of those characters — `#`, `東京`, `Ωμέγα` — slugs to nothing, and the spec doesn't say what happens next. Read literally, the minted URI is the bare `base-uri`, which is the workspace's own namespace rather than a thing in it, or `urn:dkf:<workspace-id>:` with an empty last segment. Every such label mints that same URI. Under *A minted URI resolves only to the particular it was minted for* (#62), the first one succeeds and owns the URI, and every later label in the same script is refused as a collision with it. Raised as #63.

## What Changes

- **An empty slug is refused.** When `uri` is omitted and the label's slug is empty, `particular_define` refuses without creating or changing anything. The refusal says the label yields no slug and that an explicit `uri` is required.
- **Nothing else changes.** No label that mints a URI today mints a different one. A label with at least one `[a-z0-9]` character after folding (`C 東京` → `c`) mints as before and is subject to the #62 collision rule.
- **No format version.** No file is read differently and no file stops validating. A particular already written with an empty-slug URI stays valid; it was only ever reachable as one per workspace.

## Capabilities

### New Capabilities

_None._

### Modified Capabilities
- `particular-uris`: *URI minting convention* gains the empty-slug refusal and scenarios for it.

## Impact

- `README.md`: *Minting URIs* (the refusal and why the alternatives were rejected), the `particular_define` row in *MCP Server Tools*, and Status.
- `openspec/specs/particular-uris`: one requirement modified.
- `particulars-cli`: `define` and MCP `particular_define` must refuse an empty slug, alongside the #62 work tracked in nodelogicau/particulars-cli#32.
- Existing workspaces: a particular already minted with an empty slug is left as it is. A later define of the same label without a `uri` is refused, and the particular is still reachable by its URI or id.
