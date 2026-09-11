## Context

`sharded-layout-grace` gave the drift check a short-circuit: compare a sealed month's file count against the recorded count, and parse the segment only on a mismatch. It was written to detect a late mint without reading sealed history, and it does. It was also, by oversight, made the only place a sealed segment's `retracted` list is ever compared, and a retraction changes no file count. The requirement therefore fails one of its own scenarios, and the late-merge check has a retraction-shaped hole.

Separately, the validator requirement gives one reason for warning on a future-dated id and then fails on a far-future one as though the reason did not apply. It does apply; a different reason is needed.

## Goals / Non-Goals

**Goals:**
- Every scenario in the two requirements reachable by an implementation that follows them.
- The drift check stays bounded, and the spec says exactly what its count guarantees.
- A retraction dated into a sealed month is caught somewhere, and the spec says where.
- The far-future failure rests on a reason that survives its own premise.

**Non-Goals:**
- Changing the grace period, the count, or any write rule.
- Making the drift check catch sealed-month retractions. That costs a whole-history parse.

## Decisions

### D1. The drift check and validation guarantee different things

The drift check exists to catch the index lagging the workspace, cheaply, on every commit. It reads listings for sealed months and parses only the open documents. What a matching count proves is that no file arrived in that month since the segment was written: no late mint. It proves nothing about retractions, and the requirement now says so rather than leaving a reader to infer a stronger promise.

Validation exists to check the workspace, and it already reads every object file — it cannot check references, sources, or evidential fields otherwise. Having read them, it knows every retraction's month at no extra cost. So validation regenerates each sealed month's `retracted` list from the files and compares it with the committed segment, and a retraction dated into a sealed month — a guard violation on one machine, or a branch that retracted across two boundaries and merged late — is reported there, naming the object and the segment.

*Alternative, from #30:* parse a sealed segment in the drift check when the regenerated index places a retraction in that month. Right in effect, but "the regenerated index" would then have to be regenerated from every file, since a retraction dated into August may sit on any object minted at or before August. That is the whole-history parse the count check was added to avoid, moved one sentence to the left. The split keeps the lag check bounded and puts the full comparison where the full parse already is.

### D2. The scenario moves, and the promise to consumers is restated on validation

*A retraction dated into a sealed month* moves under the new validation requirement, where an implementation that follows the text reaches its outcome. The cache-forever scenario already says "and the workspace validates"; that phrase now carries both halves — no late mint by the count, no late retraction by validation — and the README says so in one sentence.

### D3. The far-future failure is justified by consequence, not confidence

A validator cannot tell an id two months ahead from its own clock two months behind; the uncertainty is symmetric and the warning's rationale says as much. The failure is still right, because the two errors are not symmetric in cost. A validator that is two months slow fails a healthy workspace once, loudly, on a machine that is itself broken. A validator that accepts a genuinely far-future id lets it seal the month every correct writer is minting into, and that cannot be undone. The rule stays and the sentence under it changes.

## Risks / Trade-offs

- [Validation grows one comparison per sealed month] → Against files it has already parsed; the cost is the comparison, not a read.
- [A reader takes "the workspace validates" to mean the drift check passed] → The README now names both operations and what each guarantees.
- [Six changes to one shape in four days] → Each was a paragraph, none an implementation, and the shape is simpler now than on day one. The dogfood claim records the pattern as the loop working.
