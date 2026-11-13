## Context

`knowledge_recall(particular_id)` returns a particular's whole lineage, in lineage order, with `current` identified. The spec gives it no size bound. Recall by query returns, for each resolved particular, exactly what recall by particular would. Its `limit` truncates particulars, not entries.

On the dogfood workspace (8 particulars, about 230 entries, two particulars holding most of them), the query `is` returns about 230 entries, and with `limit: 1` the first particular alone is still 140. The reference implementation's `limit` on recall by particular takes the last N in lineage order (`internal/query/recall.go:166`), so a long tail of later claims pushes `current` out. That is the one entry recall exists to surface.

The #38 thread considered three fixes. Returning only matched entries, (1a), barely shrinks the response while substring OR marks nearly everything. It also drops unsynthesised entries, which are where the format keeps contradictions. Declaring the response unbounded, (1c), records the problem without fixing it. Only a per-particular cap, (1b), bounds the response whatever the query.

## Goals / Non-Goals

**Goals:**
- A caller can bound the number of entries any particular contributes to a recall, in both modes.
- What a cap keeps is fixed by the spec, so two implementations given the same workspace and call return the same entries.
- A capped response always keeps the belief (`current`) and, as far as the cap allows, what disputes it (unsynthesised entries).
- The caller can tell a response was capped, and by how much.
- A call without the cap behaves exactly as today.

**Non-Goals:**
- Changing how a query resolves, which entries are marked matched, or the order of particulars (#38 point 2: whole-word matching and a document-frequency tiebreak).
- A total cap across all particulars in a response. `limit` × `entry_limit` already bounds it.
- Pagination or cursors. `omitted` plus a follow-up recall by particular is the continuation.
- Author-only recall (`author` with neither `particular_id` nor `query`), whose response isn't grouped by particular.

## Decisions

### D1. A new parameter, `entry_limit`, in both modes

`limit` already means particulars in recall by query. Giving it a second meaning, entries, in recall by particular would make one name mean two things on one tool, and the query stage couldn't pass it through. `entry_limit` means the same in both modes, and stage two passes it through unchanged. That keeps stage two "exactly what recall by particular would return" for the same parameters.

*Alternative:* define `limit` as entries for recall by particular and add `entry_limit` to query only. It matches the CLI's current flag, but stage two would then translate one parameter into another, and the tool row would need a mode-dependent definition. The CLI can keep `limit` on recall by particular as a deprecated synonym, since the spec never defined it.

### D2. Selection order: `current`, unsynthesised, matched, the rest

When a particular's response has more entries than `entry_limit`, the kept entries are the first `entry_limit` of:

1. the entry identified as `current`, if it is in the response;
2. entries in the `unsynthesised` set, most recent first;
3. in recall by query only, entries marked as matched, most recent first;
4. every other entry, most recent first.

Each entry is taken once, at its first tier. "Most recent first" means descending `timestamp`, ties broken by descending id. It mirrors how `current` is chosen, so no new ordering is introduced.

- `current` first, because recall answers "what is believed about this", and the belief is what a cap must not cut.
- Unsynthesised before matched, because unsynthesised entries are where disagreement lives (*Conflict semantics*: later claims are not silently the belief). An agent that sees `current` without what disputes it is worse off than one that sees nothing. While substring OR marks almost everything, matched-first would not even be selective.
- Matched before the rest, in query mode, because the query is the only evidence of what the caller wants among entries already synthesised.
- Recency within each tier, because a cap of N mostly matters to long-lived particulars, and recent entries are more likely to be what changed.

*Alternatives:* the last N in lineage order (the CLI today) can drop `current`. `current` plus the inputs it cites, the (1a) shape, makes the response size depend on how broad a synthesis is, so it isn't a bound.

`stale` entries get no tier of their own. A stale entry that is also unsynthesised is kept at tier 2. A stale synthesis that is `current` is kept at tier 1. That leaves only stale entries already absorbed by a newer synthesis, which the belief no longer rests on.

### D3. Kept entries come back in lineage order

Selection decides membership, not order. The kept entries are returned in lineage order with `current` identified, exactly as an uncapped recall orders them. A caller that reads the lineage sees a shorter one, not a reshuffled one. *Recall by query* already forbids resolution from reordering a particular's entries, and the cap follows the same rule.

### D4. `omitted` counts only what the cap removed

Each particular in a response where `entry_limit` was supplied carries `omitted`, a non-negative integer: the number of entries in its uncapped response that the cap left out. Entries removed by `scope`, `author` or `include_retracted` are not counted. Those filters already decide what the caller can see, and counting them would leak, for example, how many `personal` claims a `public` caller can't see. This is the same principle as the existing scenario *What the caller cannot see does not rank*.

`omitted` appears, as `0`, whenever `entry_limit` was supplied, so a caller can tell "nothing was cut" from "this implementation doesn't report it".

### D5. Ranking counts against the uncapped response

*Each result says how it was resolved* counts distinct matched terms against "the objects in its response". With a cap, that would let `entry_limit` change which particulars `limit` keeps, because a term in a dropped entry would stop counting. The ranking counts against the uncapped response instead, so `entry_limit` changes only what each particular shows, never which particulars appear or in what order. The order is computed under the same filters as before, so nothing hidden ranks either.

### D6. Omitted means uncapped, with no implementation default

If implementations could pick a default cap, the same call would return different entries on different implementations. The cross-implementation determinism #36 established would be gone. Without `entry_limit`, a recall is what it is today. Agents are told to pass a cap when they don't need the lineage (see Open Questions).

### D7. A non-positive cap is refused

`entry_limit` is a positive integer. `0`, a negative number or a non-integer is an error, not an empty response. A cap of 1 keeps `current` when there is one. The smallest cap is therefore still a useful answer, and there's no reason to allow a smaller one.

## Risks / Trade-offs

- [A cap below the number of unsynthesised entries hides some disagreement] → `omitted` says so, and the kept unsynthesised entries are the most recent. `conflict_detect` still reports the full set.
- [Agents won't pass `entry_limit`, so the common case stays unbounded] → Document it in the tool row and in agent guidance. A default stays a possible later change once bench numbers exist, and adding one is easier than removing it.
- [Ranking against the uncapped response costs reading entries that aren't returned] → The uncapped response is what recall reads today, so the cost is unchanged. The cap saves output, not reading.
- [`entry_limit` × `limit` is still large for broad queries] → It is bounded and caller-chosen. Making it small is #38's second change.

## Migration Plan

No format version and no file change. Spec and README land first. particulars-cli then implements `entry_limit`, the selection order and `omitted`, and keeps its existing recall-by-particular `limit` as a deprecated synonym for `entry_limit`. Callers that don't pass the parameter see no difference. Rollback is removing the parameter, with no data to migrate.

## Open Questions

- Should `agent-guidance` (the delivered `dkf.md` conventions) recommend a cap, for example `entry_limit: 10` for recall by query? It is left out here to keep this change to tool behaviour, and fits with the bench work.
- Should a later version set a default cap once particulars-bench can measure one? Deferred under D6.
