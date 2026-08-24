## Context

Issue #15 was filed after an export made the exposure visible, and its author then corrected the issue's own premise: the spec does address derived disclosure, under the no-cascade rule, and the reasoning there is the better-argued half of what the issue asked for. What survives is narrow — the existing SHOULD-warn is conditioned on promotion, and the observed case had no promotion in it.

This is the first spec question here where the reference implementation shipped behaviour before the spec ruled: `particulars-cli` already emits `scope_wider_than_inputs` for the asserted case. The choice is therefore partly about whether to ratify or unwind working code.

## Goals / Non-Goals

**Goals:**
- Close the gap between the two paths by which a synthesis can end up wider than its inputs.
- Give the condition one name, specified rather than left to implementations.
- Keep the judgement with the human reviewing the change.

**Non-Goals:**
- Constraining a synthesis's scope by its inputs. Considered and rejected below.
- Any change to promotion records, effective scope, or the no-cascade rule itself.
- Detecting whether a synthesis's prose actually discloses its inputs, which is not computable.

## Decisions

### D1. Warn, do not require

A synthesis's effective scope MAY exceed its inputs'. The alternative — requiring `scope ≤ narrowest input` — is sound and would close the hole completely, but it forbids the format's most useful move: reconciling private evidence into a conclusion that can be shared. An author who writes that conclusion carefully discloses nothing, and no tool can tell the difference between that and a careless one. Requiring would push authors toward re-asserting conclusions as standalone claims with no inputs at all, which destroys the lineage the format exists to keep.

The third option in the issue — say nothing, and call derived disclosure the author's responsibility — is rejected because silence on `scope` reads as "not considered", and every implementer would rediscover the exposure the way this one did.

*"For now" is meant literally:* warning is the weakest closure that names the problem. If review proves insufficient in practice, requiring remains available and this decision is what would be revisited.

### D2. Compare effective scope on both sides

The condition is: a synthesis's **effective** scope is wider than the **effective** scope of any input it cites. Not asserted scope, which goes wrong in both directions once promotion records exist — it warns when an input is `personal` but promoted to match, and stays silent when the synthesis itself is promoted past inputs that were never widened.

This is the generalisation the issue's author arrived at, and it subsumes the promoted-synthesis case the no-cascade rule already covered, so that rule's warning clause is removed rather than duplicated.

### D3. The condition belongs to the workspace, not the file

Because promotion can create the condition later — and clear it later — without modifying either the synthesis or its inputs, it cannot be settled at write time. The spec therefore says it is evaluated over workspace state: by a validation pass, by `synthesis_create`, and by `knowledge_publish`, which is the second way to enter it.

The practical consequence for implementations is that `scope_wider_than_inputs` is not a property to be stamped on a file when written; it is recomputed from current state, and a warning that fires today may correctly stop firing tomorrow.

### D4. It lives in `scope-promotion`

The rule is not about promotion, but `scope-promotion` is where effective scope is defined and where the rules that keep a partial implementation safe already live. Splitting it into `synthesis-rules` would separate the condition from the definition it depends on. The capability's Purpose is widened to say it covers derived disclosure as well.

## Risks / Trade-offs

- [A warning is only as good as the review that reads it] → Accepted, and the reason the condition is named and specified rather than left to implementations: a consistent name is what makes it recognisable across tools and reviewable in a diff. The alternative closure remains open if this proves too weak.
- [Recomputing from workspace state costs more than a write-time check] → It is a scan of promotion records, which the index already carries. The correctness argument in D3 outweighs it.
- [Ratifying `5a50421` before it compares effective scope] → The spec adopts the name and the intent; the comparison change is already tracked in particulars-cli#2. Nothing shipped becomes wrong, only incomplete.

## Open Questions

- Whether the format should record that an author considered derived disclosure — an acknowledgement that suppresses the warning deliberately rather than silently. That would restore some of the ceremony asymmetry noted on #15, where promotion is explicit, sourced and retractable while asserting a wider synthesis is a field value and nothing else. Deferred as more machinery than "for now" warrants.
