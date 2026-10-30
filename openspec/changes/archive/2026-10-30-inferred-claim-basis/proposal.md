## Why

An `inferred` claim is "derived by reasoning from other claims", but nothing on the claim names those claims (#42). Its warrant is prose, so no reader or validator can walk from a rule of thumb back to the instances it was drawn from. And when an instance is retracted, nothing surfaces the rule that rested on it. [Forgetting §9](https://forgetting.fyi/#episode-to-habit) names this as the point where the way back from a habit to what happened breaks inside particulars. It is also where agent memory most often writes fluent unsourced claims: reflections and lessons learned that cite nothing.

The review on #42 rejected a fourth synthesis `method` for induction. A synthesis becomes `current` for its subject, and a rule of thumb is one belief about a subject, not the reconciled whole. This change takes option 2 instead: an inferred claim names its basis, as its evidence.

## What Changes

- New optional claim field `basis`: a non-empty list of ids of existing claims or syntheses that the claim was inferred from. An `inferred` claim's basis is its evidence, in the way an `observed` claim's evidence is its `source.document`.
- `basis` is allowed only on `evidential: inferred` claims. Writers refuse it on any other claim, and on a synthesis, which has `inputs`. Validators fail on it as `basis_not_inferred`, and readers still read the file.
- A dangling basis id fails validation, as a dangling `superseded-by` does.
- **Citing is not synthesising.** Claims named in a basis stay `unsynthesised`. The transitive `inputs` of `current` follow `inputs` only, not `basis`.
- **`stale` extends to claims.** A non-retracted claim or synthesis is stale when anything it cites, directly or transitively through `inputs` and `basis`, is retracted. A rule of thumb whose instance is retracted surfaces in `conflict_detect`.
- `lineage_trace` follows `basis` and labels those edges apart from synthesis inputs.
- Index entries for claims with a basis carry `basis`, so conflict sets can still be computed from the index.
- The `scope_wider_than_inputs` warning applies to an inferred claim wider than its basis, and promotion does not cascade to a basis.
- An `inferred` claim without a basis stays valid. Validators report it as `inferred_without_basis`, a fact about the corpus reported in aggregate, and `claim_assert` warns when it writes one.
- Induction gets no method of its own: a rule of thumb is an inferred claim whose basis is its instances. A later counterexample is a `qualification` synthesis, as now. How many instances a rule rests on, and when they happened, is derived from the basis rather than recorded.
- README: the claim example and *What backs a claim*, *Conflict semantics*, the `claim_assert` and `lineage_trace` rows, validation conditions, and derived disclosure.

## Capabilities

### New Capabilities

- `claim-basis`: the `basis` field, what it may cite, write-time and validation behaviour, `lineage_trace` traversal, reporting a basis-less inferred claim, and induction as an inferred claim with a basis.

### Modified Capabilities

- `claim-evidential`: *Every claim declares what backs it* says that an inferred claim names what it was inferred from in `basis`.
- `conflict-semantics`:
  - *Structural conflict sets are defined per particular*: `stale` covers claims, and follows `basis` as well as `inputs`; transitive inputs of `current` follow `inputs` only.
  - New requirement: *Citing in a basis does not synthesise*.
- `scope-promotion`: new requirement *A basis is treated as inputs for disclosure*. No cascade, the `scope_wider_than_inputs` warning, and when it is evaluated all apply to an inferred claim and its basis.
- `index-manifest`: *Index entries carry a baseline and may be extended*: claims with a basis carry `basis`.

## Impact

- README.md: the sections listed above.
- `openspec/specs/`: one new spec and four modified ones.
- particulars-cli: `claim assert --basis`, the MCP `claim_assert` parameter, conflict sets, lineage, index entries, the validation conditions, and the skill text. To be raised as an issue there.
- particulars-knowledge: existing `inferred` claims have no basis. They are reported in aggregate, and none can be backfilled, since claims are immutable.
- Not breaking. Old readers ignore the unknown field, so they miss staleness that runs through a basis but read every file. Old index rebuilds keep the unknown `basis` field on entries.
