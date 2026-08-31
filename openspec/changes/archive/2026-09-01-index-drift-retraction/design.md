## Context

A correction to a correction. #21 opened a real gap — the first implementation to write a new MAY field would have failed CI on every workspace — and D5 of `attribution-review-round` closed it with a rule about *absence*. The follow-up review (#22) showed that absence is the wrong axis: for one field, absence is a value. The fix is to say what the tolerance is *for*, because the purpose picks the right axis on its own.

The three standing constraints apply. Files are the truth and the index is a cache, so the check may be lenient about the cache but never about the files. Claims are immutable, so the only property of an object that can change after the index was written is whether it has been retracted. And readers are lenient — a consumer never depends on a MAY field being present — so a presence difference costs a reader nothing.

## Goals / Non-Goals

**Goals:**
- A drift check that never passes over a retraction the committed index does not know about.
- A tolerance that survives every future MAY field without a per-field decision.
- The older-tool direction handled the same way #16 handled entry types.

**Non-Goals:**
- A per-index declaration of known fields. It would work, and it is machinery the index has never needed; the immutability criterion makes it unnecessary.
- Changing what entries carry, or making any MAY field required.
- Reopening the byte-for-byte comparison the reference implementation uses. The masking form keeps it.

## Decisions

### D1. The criterion is immutability of the mirrored property, not absence

Why the check exists: to catch the index lagging *changes to the workspace*. So the question for any presence difference is whether it can reflect a change. For a field mirroring an immutable property the answer is never — the object could not have changed, so the only explanation is that one side's writer predated the field. For a field mirroring a mutable property the answer is yes, and there is exactly one such property:

```
  field             mirrors                   can it change after
                                              the index was written?
  ────────────────────────────────────────────────────────────────
  scope             context.scope             no   → presence tolerated
  topics            context.topics            no
  timestamp         timestamp                 no
  author            source.author             no
  document-author   source.document.author    no
  retracted         the retracted block       YES  → compared as present;
                                                     absent means false
```

#22 offered a second formulation — "a field whose absence carries a value is never tolerated as unknown" — which agrees on every field that exists. The two can diverge: a future boolean mirror of an immutable property (a `signed: true`, if signatures prove write-once) has an absence that carries a value yet cannot reflect a change, and the purpose-based rule would tolerate it correctly where the value-based rule would fail every old index again. The rule is therefore stated on immutability, and "absent means false" is how `retracted` falls out of it rather than a rule of its own.

### D2. The tolerance is symmetric

#21 tolerated absence from the *committed* side only, because that was the failing case in hand. Immutability does not care which side is older: a committed index carrying `author`, checked by an older tool whose rebuild lacks it, is the same non-change. Stating it symmetrically also removes the need for a check to know which writer is newer, which it cannot.

### D3. A rebuild preserves fields it does not recognise

Symmetry has a consequence. If an older tool's rebuild strips `author` from every entry, the newer tool's next check tolerates the absence — correctly, by D2 — and the cache has silently lost a field that recall by author uses to avoid opening files. This is the field-level twin of the case #16 closed for entry types, and the argument is the same: a rebuild is of the *workspace*, not of one tool's view of it. The stakes are lower — a stale index must never produce a wrong result, so the loss is speed, not truth — which is why this rides along rather than being its own change.

### D4. Masking is the implementation form, not the rule

The reference implementation compares bytes. The form that keeps that: before encoding the rebuilt entries, mask each to the committed entry's *presence* of the immutable MAY fields — and, by D3, carry across any field the tool does not recognise — then compare as before. An old index passes; formatting drift, a changed `scope`, and a new `retracted: true` all still fail. This is recorded as an implementation note because the spec's rule is about meaning, and a future implementation that compares parsed entries needs no masking at all.

## Risks / Trade-offs

- [Stating the rule on immutability requires the reader to know which properties are immutable] → The format has exactly one mutable property and says so in *Retraction*; the README lists the MAY fields with their classification once, and the next field classifies itself.
- [Symmetric tolerance means an older tool's check passes an index it cannot fully read] → That is the #16 behaviour for entry types, already accepted; and D3 stops the older tool degrading the index it passes.
- [A workspace with no retractions has `retracted` absent everywhere, which is the case the obvious patch got wrong] → Not a case under this rule: `retracted` is never tolerated as unknown, so its first appearance is drift regardless of how many entries lack it.

## Migration Plan

Text only here. Implementations: the masking step, and unknown-field preservation on rebuild. No index changes shape; an index that passed under #21 passes here unless it is hiding a retraction, in which case it should not have passed.

## Open Questions

- None. #22's extensions — symmetry and field preservation — are taken here rather than left.
