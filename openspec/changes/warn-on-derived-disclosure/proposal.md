## Why

[Issue #15](https://github.com/nodelogicau/particulars/issues/15) reports that scope protects assertions individually but not by derivation: an `organisation` synthesis can quote `personal` claims and carry their substance past the per-claim scope check. It was observed in a real workspace, where a Graph export emitted a belief with `claimCount: 0` above prose that argued in detail from the three withheld claims.

The spec already half-covers this. The no-cascade rule under Promotion records says implementations SHOULD warn when a *promoted* synthesis has narrower inputs — but that warning is conditioned on promotion, and the case actually hit involved no promotion record at all. A synthesis asserted `organisation` over claims asserted `personal` is reachable the moment a workspace's `defaults.scope` is wider than the scope of what is already in it, which needs no deliberate act by the author and is therefore the more common path.

## What Changes

- **The derived-disclosure warning is generalised** from promotion to effective scope on both sides: implementations SHOULD warn when a synthesis's effective scope is wider than the effective scope of any input it cites. This subsumes the promoted-synthesis case verbatim, covers the asserted case, and stays correct once inputs are promoted to match — where a warning conditioned on assertion would fire falsely.
- **The condition is named** `scope_wider_than_inputs`, so the same situation reports identically across implementations and a workspace moving between tools gets the same warnings.
- **The condition is a property of workspace state, not of a synthesis.** Promotion can create or clear it later without either file changing, so the spec states that it is evaluated across the workspace rather than only at write time, and that `knowledge_publish` evaluates it too.
- **Derived disclosure is warned, not forbidden.** The spec says explicitly that a synthesis MAY be wider than its inputs, and why: reconciling private evidence into a shareable conclusion is a normal reason to synthesise, and no tool can judge whether prose discloses its sources. The judgement belongs to the human approving the change.
- The no-cascade rule itself is unchanged; only its warning clause moves out and broadens.

## Capabilities

### New Capabilities
<!-- none -->

### Modified Capabilities
- `scope-promotion`: the promotion-conditioned warning is replaced by a general derived-disclosure requirement covering both the asserted and the promoted path.

## Impact

- `README.md` — the closing sentence of the no-cascade paragraph under Promotion records.
- `openspec/specs/scope-promotion/spec.md` — one requirement modified, one added.
- Issue #15 — resolved; close with a pointer to the resolving text.
- `particulars-cli` — already warns on the asserted case as `scope_wider_than_inputs` ([5a50421](https://github.com/nodelogicau/particulars-cli/commit/5a50421)) and has said it will move to effective scope when promotion records land, which is tracked in particulars-cli#2. Nothing here contradicts what it shipped; the spec adopts its name and generalises its comparison.
- No code in this repository; no dependencies.
