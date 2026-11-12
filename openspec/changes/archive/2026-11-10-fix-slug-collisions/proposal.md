## Why

`particular_define` without a `uri` mints one from a slug of the label. The spec then makes define idempotent on that minted URI: *Same label across sessions* requires any two labels that **slug** identically to resolve to one particular. The rule exists to stop an agent creating a duplicate every session. But the slug discards everything outside `[a-z0-9]`, so labels for different things share one: `C`, `C#` and `C++` all slug to `c`. Once `C` exists, `particular_define(label: "C#")` reports success with `created: false`. From then on, every claim about either language is about one particular, and nothing tells the caller. The reference CLI also relabels on that path, so `C` becomes `C#`. An agent defining things by label is the likely victim. Raised as #62, found in nodelogicau/particulars-cli#32.

## What Changes

- **The no-duplicate rule keys on the label, not the slug.** When `uri` is omitted and the minted URI already names a particular, define resolves to it only if the supplied label equals that particular's `label` or one of its `aliases` under Unicode case folding. `Project X` and `project x` are still one particular.
- **A minted collision that doesn't match is refused.** Nothing is created or changed. The refusal names the existing particular (`id`, `uri`, `label`) and says what to do: pass an explicit `uri` for a different thing, or refer to the same thing by its URI or id.
- **A minted-URI define never relabels.** When it resolves to an existing particular, the label stays as it is. Supplied aliases are added and none are removed. Renaming requires the explicit `uri`.
- **An explicit `uri` is unaffected.** It names the particular, so define stays idempotent on it and may change the label, as now.
- **No format version.** No file is read differently and no file stops validating. The change is to what `particular_define` does when it is called. Writes that used to merge two things silently are now refused.

## Capabilities

### New Capabilities

_None._

### Modified Capabilities
- `particular-uris`: *URI minting convention* replaces the *Same label across sessions* scenario with label-keyed scenarios, and a new requirement, *A minted URI resolves only to the particular it was minted for*, covers the label match, the refusal, no relabelling, and the explicit-`uri` exception.

## Impact

- `README.md`:
  - *Particulars*: "idempotent on URI, may rewrite its `label` and `aliases`".
  - *Minting URIs*: the paragraph saying two labels that slug identically resolve to one particular.
  - *MCP Server Tools*: the `particular_define` row.
  - Status.
- `openspec/specs/particular-uris`: one requirement modified, one added.
- `particulars-cli`: define currently resolves on the minted URI alone and relabels. nodelogicau/particulars-cli#32 tracks the fix: match on label or alias, refuse with the existing particular named, and don't relabel without an explicit `uri`.
- Existing workspaces: particulars already conflated this way stay conflated. The format can't tell them apart from a deliberate alias, so this change does not try to detect them (see design).
