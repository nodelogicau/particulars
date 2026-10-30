## Context

DKF has three evidentials. `observed` points at its evidence through `source.document`. `held` has no evidence by definition. `inferred` is defined as "derived by reasoning from other claims", but it has no field naming those claims, so its warrant can only be stated in `content`. The only object that cites other objects is `DSYNTHESIS`, through `inputs`. A synthesis also takes part in `current`: the most recent synthesis on a particular is the belief about it.

Issue #42 asks how a rule of thumb, induced from several instances, can cite them. Its review rejected induction as a synthesis `method`, because the induced rule would become `current` for its subject and turn the previous belief `unsynthesised`. This design takes the other option: a claim-level `basis`.

## Goals / Non-Goals

**Goals:**
- An inferred claim can name what it was inferred from, so the chain from a rule back to its instances can be walked mechanically.
- Retracting something a rule rests on surfaces the rule, the way retracting an input surfaces a synthesis.
- Nothing changes about `current`, and a claim never becomes a synthesis by having a basis.
- Existing workspaces stay valid, and nothing has to be backfilled.

**Non-Goals:**
- An episodic format, or citing objects outside DKF. A basis cites DKF claims and syntheses only.
- Roles or weights in a basis. A basis is evidence, not a dialectical relation.
- Recording how many instances a rule rests on. That is derived.
- Judging whether the basis actually supports the claim. As with synthesis inputs, that is the reader's or the harness's judgement.

## Decisions

**A basis is evidence, not inputs.** The field sits beside `evidential` and answers the question `evidential` raises: inferred from what? This keeps the line between claims and syntheses. A synthesis's `inputs` settle a relation among what it cites, and the synthesis competes for `current`. A claim's `basis` only warrants the claim, and nothing about `current` changes. Two alternatives were rejected:
- *Induction as a fourth synthesis `method`.* An induced rule would become `current`, so a single rule of thumb would displace the reconciled belief about its subject, and any instances about the same subject would count as synthesised although nothing was reconciled.
- *Reuse `inputs` on claims.* That would make "has inputs" no longer mean "is a synthesis", and every consumer that tests for `inputs` would have to learn the difference.

**The field is named `basis`, and is a list of ids.** It holds plain id strings, with no `role` or `weight`, because nothing in a basis is a thesis or an antithesis. If present, it is non-empty: an empty list would be indistinguishable in meaning from absence. In canonical order it follows `evidential` and precedes `confidence`, since it qualifies the first and is what the second's "the reasoning may be invalid" refers to.

**Only on `inferred` claims.** An `observed` claim's evidence is a document, and a `held` claim has none by definition. A synthesis has `inputs` already. Writers refuse a basis anywhere else. A file that carries one anyway fails validation as `basis_not_inferred`, but is still read, following the `confidence_on_held` precedent: the file can't be corrected, so a reader that rejected it would strand it.

**A basis cites existing DKF objects.** Each id must be a claim or synthesis in the workspace. A dangling id fails validation, as a dangling `superseded-by` does. A basis may cite retracted objects. Citing one at write time is legal but is immediately stale, which is the honest report. A future episodic format is reached the long way round: an `observed` claim about an episode cites the episode record as its `source.document`, and a rule cites that claim. DKF never resolves another format's ids.

**Citing is not synthesising.** Objects named in a basis keep their place in `unsynthesised`. The transitive `inputs` of `current` follow `inputs` only. If a synthesis cites a rule as an input, it has reconciled the rule, not the instances behind it. This mirrors the existing rule for cross-particular inputs.

**`stale` follows both edges.** The stale set becomes: non-retracted claims and syntheses with subject in the class that cite a retracted object, directly or transitively through `inputs` and `basis`. A synthesis citing a rule whose instance is retracted is stale too, which is what transitivity already means for synthesis chains. A stale inferred claim leaves the set when it is retracted, typically with `superseded-by` pointing at a rule with a revised basis. Claims are immutable, so that is the only way out, and it is the same answer a reader would want.

**`lineage_trace` follows `basis`, labelled.** Lineage already distinguishes `inputs` by role and shows `superseded-by` successors. Basis edges are reported with the relation `basis`, so a reader can tell "argued from" from "inferred from".

**The index carries `basis`.** Conflict sets are computable from the index today because synthesis entries carry `inputs`. Staleness through a basis needs the same, so claim entries with a basis SHALL carry it. Older rebuilders preserve unknown fields on regenerated entries, so a committed `basis` survives them.

**Derived disclosure covers a basis.** An inferred claim's content may restate what its basis says, exactly as a synthesis may restate its inputs. So `scope_wider_than_inputs` applies to an inferred claim whose effective scope is wider than any basis member's, and promotion never cascades to a basis. The condition keeps its name: for this purpose a basis is the claim's inputs, and one name is easier on consumers than two.

**A basis-less inferred claim is reported, not refused.** Every existing inferred claim lacks a basis, and none can be given one. So validators report `inferred_without_basis` as a fact about the corpus, in aggregate. `claim_assert` warns when it writes one, because at write time the condition is still actionable. Refusing would break every harness that reasons without retrieving, and would push authors towards `held`, which is worse.

**Induction needs nothing else.** A rule of thumb is an inferred claim whose basis is its instances. A counterexample is a `qualification` synthesis citing the rule and the counterexample. The number and dates of a rule's instances come from its basis members' timestamps. Recording them as well would duplicate the basis, and could drift from it.

## Risks / Trade-offs

- [Older readers ignore `basis`, so they miss staleness that runs through it] → They still read every file, and their conflict sets are a subset of the new ones, never a contradiction. The README says so.
- [A basis can be padded with loosely related claims] → The same is true of synthesis inputs today. A basis is a claim of support that reviewers can check, which is more than prose offers.
- [Stale inferred claims accumulate in `conflict_detect` priority] → That is the breakdown the change exists to surface. Retracting with `superseded-by` clears each one.
- [`inferred_without_basis` is noisy in workspaces with many inferred claims] → It is aggregated, per *Conditions are findings about objects or facts about the corpus*, so it costs one line.
- [A hand-written file could make basis references form a cycle] → Writers can only cite existing objects, so they can't create one. Traversal for `stale` and `lineage_trace` visits each object once.

## Migration Plan

No migration. Existing files are valid as they are. Implementations add the field, the conditions and the traversal. A workspace gains bases only as new inferred claims are written.

## Open Questions

- Should `recall` mark an entry that is the basis of another entry, as it marks `current`? Left to implementations for now.
- If an episodic format is specified, should a basis be allowed to cite its objects directly? This design says no, and routes through `observed` claims about episodes. Revisit when that format exists.
