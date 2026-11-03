## Context

The sealed-month rule was written when retraction was believed to be the only way an existing file changes. Two other ways already exist:

- **Particular update.** `particular_define` is "Create or update… Idempotent on URI" (README tool table). It rewrites `label` and `aliases`, never `uri` or `id`. This has been true since v0.1.
- **Redaction.** It arrived with `add-redaction` (`dkf/0.3`, on `main` and not yet declared). It removes listed fields and adds or extends a `redacted` block.

Neither changes anything the index mirrors. A particular's index entry is `id`, `type` and `uri`, and redaction's redactable set was chosen to exclude every mirrored field. So no segment is rewritten, no count changes, and the drift check and validation stay clean. The only statements that are false are the enumeration and the git benefit derived from it. The semantic cache's "keyed by object id, never needs recomputing" premise fails for particulars in the same way.

## Goals / Non-Goals

**Goals:**
- One authoritative list of the modifications a sealed-month file may undergo, so implementers and the git-benefit sentence agree.
- A semantic cache that cannot serve a vector of a label or alias the particular no longer carries.
- Correct the worked example of path derivation.

**Non-Goals:**
- Changing what `particular_define` may update. `uri` stays immutable, and `id` is never rewritten.
- Changing the index or the drift check. Neither needs to see these modifications.
- Forbidding particular updates in sealed months (#51 option b) or exempting particulars from sharding (option c).

## Decisions

### D1. Enumerate, don't generalise

The requirement lists the three permitted modifications by name: append `retracted`, add or extend `redacted`, and update a particular's `label` and `aliases`. A general rule such as "any change that does not alter an index entry" was rejected. It would permit edits the format forbids, such as rewriting a claim's `content`, which the index does not mirror either. Immutability of claims is a format rule, not a consequence of indexing.

### D2. The particular update is a v0.2 erratum, not a format change

v0.2 already permitted the update through `particular_define`, and the reference CLI already does it in sealed months. The spec contradicted itself; it did not forbid something implementations relied on being forbidden. So `format` is not bumped, and the README Status records the correction against v0.2. The redaction exception needs no erratum, because redaction exists only in `dkf/0.3`, which is not declared.

### D3. The retraction rule is scoped, not widened

"Adding a `retracted` block is one of exactly two permitted modifications to an existing object file" becomes a statement about files that can be retracted: claims, syntheses, merge records and promotion records. Particulars cannot be retracted. Folding the particular update into retraction's list would make it a third "modification" of claims, which it is not. The retraction requirement instead names particulars as governed by `particular_define`, and `workspace-layout` holds the complete list.

### D4. The cache detects particular changes itself

The index does not mirror `label` or `aliases`, so the incremental update ("ids in the index that the cache lacks") cannot see a particular update. The cache SHALL record, per particular vector, the text it embedded or a hash of it. It SHALL NOT consult a vector whose recorded text differs from the particular's current label or alias, and SHALL recompute or delete it no later than its next update. Rereading particulars on each update is cheap: they are few relative to claims, and a rebuild already reads them. Recording the text puts nothing new at risk, because the cache already lives outside the workspace and is never served. A hash is allowed for implementations that prefer not to keep the text.

A removed alias is the case that matters. Its stale vector could resolve a query to a particular through a name it no longer answers to. That is wrong, though not unsafe, which is why "never consulted" is the rule rather than only "eventually recomputed".

### D5. The git benefit is stated with all three exceptions

"An old month's tree object is rewritten only by a late merge, a retraction, a redaction, or an update to a particular's label or aliases — never by an ordinary append." The benefit that matters, that appending never touches old trees, still holds. Listing the exceptions keeps the sentence true.

## Risks / Trade-offs

- **[A spec that lists exceptions invites more]** → Each future modification has to be added to this one list. That is the point: it makes such a change a deliberate spec edit, not an implementation drift.
- **[Erratum against a tagged release]** → `v0.2` is a lightweight tag, and re-tagging would move a published reference. The README Status records the erratum instead, and the GitHub release notes can link to it.
- **[Cache text retention]** → Storing embedded text duplicates labels and aliases outside the workspace. These are already in the workspace, and the cache is never served. Implementations may store a hash instead.

## Migration Plan

None. No file, index document or `format` value changes. Implementations with a semantic cache add the per-vector text or hash on their next rebuild.

## Open Questions

- Should the GitHub v0.2 release notes gain an "Errata" line linking to the README Status? Draft answer: yes, as part of this change's tasks, once it merges.
