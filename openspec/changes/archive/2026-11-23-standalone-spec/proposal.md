## Why

DKF, intentions and episodes should each stand in their own right, so people can choose which to implement or use. DKF already does in substance: siblings are named only in *Purpose*, in *Ecosystem* and in one example scenario, and no rule resolves a reference to another format. But the text doesn't say so. There's no Conformance section saying which text is normative. *Purpose* also introduces DKF first as one layer of a family, before saying it's complete on its own. Episodes (its `standalone-spec` change) and intentions (nodelogicau/intentions#44) have each added a Conformance section and a `standalone-conformance` capability. This change does the same here.

## What Changes

- **A Conformance section** after The Approach.
  - **Key words:** capitalised key words are BCP 14. Unlike episodes and intentions, this text states most rules in plain prose ("must", "is refused"), and a Conformance section that bound only capitalised words would quietly unbind them. So the section says prose rules in normative sections bind equally.
  - **Normative sections:** Core Object Types, Object Model, Unbounded History, Bounded Work, and File Layout.
  - **Conditionally normative:** MCP Server Tools, for an implementation that exposes a listed tool name. Public Discovery, for a publisher or consumer of public knowledge. Trust and Provenance, where it defines the reserved `signature` and its payload.
  - **Everything else is informative.**
  - **Completeness:** the specification is complete on its own, with no intentions or episodes code, data or workspace.
- ***Purpose* says DKF stands alone** right after saying what it is. It then describes the family, noting that each format stands alone. The episodes sentence says a log *can be kept* in episodes rather than that it *lives* there.
- **No format version.** No file is read differently and no file stops validating.

## Capabilities

### New Capabilities
- `standalone-conformance`: DKF is implementable from its own text. No field's value must be another format's identifier, no rule constrains another format, and the Conformance section states which text is normative, including that prose rules bind.

### Modified Capabilities
- `format-purpose`: *The specification states its relationship to intentions* now requires *Purpose* to say that DKF is complete on its own before it describes the family.

## Impact

- `README.md`: a new Conformance section, and the second and third paragraphs of *Purpose*.
- `openspec/specs`: one requirement modified, one capability added.
- Implementations: none.
