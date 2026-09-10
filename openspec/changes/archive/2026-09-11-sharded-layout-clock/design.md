## Context

`sharded-layout-corrections` (2026-09-11) keyed tombstones by the month a retraction happened and defined the current month as the later of two clocks: the newest id's month and the newest `retracted.timestamp`'s month. The minting guard, written a day earlier, was left bounded by the newest id's month alone. #27 shows the gap between the two: when a retraction is dated into a month with no mints yet, a mint into any month between the newest id and the current month is legal and unindexable. The change even has a scenario for the state that opens the gap. The review also notes that a retraction timestamp is bounded below and not above, so a typo can seal a year, and that the README's filtering bound is stated on the wrong quantity.

No implementation has shipped `dkf/0.2`. The reference implementation stamps retractions from its own clock and cannot produce the bad state alone; the exposure is another implementation, a hand edit, or two machines that disagree.

## Goals / Non-Goals

**Goals:**
- Both guards bound against the same quantity, so a mint that passes its guard always has an unsealed home.
- No write refused because another machine's clock disagreed.
- A typo'd future timestamp degrades to something visible and self-correcting, not to a sealed year.
- The README's filtering bound stated on the quantity it actually depends on.

**Non-Goals:**
- Clock synchronisation across writers. The format cannot see clocks; it can only arrange that disagreement costs nothing permanent.
- Bounding *object* timestamps below. Assertion time may legitimately precede minting, and this change does not touch that rule.
- Reopening the tombstone shape. Per-month tombstones in the retraction month's segment stay; only what the root holds while ahead changes.

## Decisions

### D1. The current month is the newest id's month, and nothing else

#27 offers bounding mints by the current month. That closes the hole by refusal: a machine with a correct clock is told no because a machine with a wrong one wrote a retraction first, and if the wrong one was a year out, every write is refused for a year. Refusal is the right answer when the writer is at fault and the wrong one when it is not.

Removing the second clock closes the hole by construction. Sealing follows mints alone; a retraction's month decides only which document it will eventually seal into. While the newest id is in October and a retraction is dated December, the retraction sits in the root, which holds October's entries and every retraction dated October or later. A November mint seals October — its entries and its October retractions — and the December retraction stays in the root. A December mint seals November, an empty-entries segment if November had retractions and no segment otherwise, and the December retraction seals when January mints. Every scenario `sharded-layout-corrections` wrote still holds; *A month of retractions only* holds by the same mechanism it always did, one step later.

A rebuild is still a pure function of the files: the newest id is in the files, and the partition of retractions between root and segments follows from it.

### D2. Both guards, one bound

With one clock the guards read the same: a writer SHALL NOT mint an id whose month is earlier than the newest id's month, and SHALL NOT write a retraction whose `timestamp` month is earlier than the newest id's month. The second is weaker than before — a retraction may now be dated into a month that has no mints, which is exactly the state that was dangerous under two clocks and is harmless under one — and it is the weakest rule that keeps a retraction out of a sealed segment.

### D3. A retraction is not dated later than the writer's clock

A retraction timestamp is when the retraction was recorded, and no honest recording is in the future. The upper bound costs nothing and removes the one plausible way to put a retraction far ahead: a typo. Under D1 a far-ahead retraction is harmless to the layout, but it is still wrong — it would sit in the root for a year and a reader filtering by time would misplace it — and a writer that can refuse it should.

The bound is against the writer's own clock, the only clock it has. That leaves clock skew, which the format cannot detect at write time and which D1 makes harmless.

### D4. A validator warns on time it cannot have seen

Writer rules bind writers. A hand-edited file, a copied file, or an implementation that predates the rule can still carry a future id or timestamp. A validator has a clock too, so it SHOULD warn on an id minted, or an object or retraction timestamp dated, later than now, naming the object. A warning rather than an error, because the validator's clock might be the wrong one, and because nothing structural is broken: under D1 the file has a home and the index is consistent. Reported per object, since the action — check the clock, or accept the timestamp — is at that object.

### D5. The filtering bound is elapsed months, and the README says so

An object minted in month M can be retracted in any month from M to now, so checking whether it is retracted reads the tombstone list of every month from M to now: proportional to elapsed calendar months, about twelve a year, and independent of how many objects the workspace holds. That is a real bound and a good one; "bounded by the period filtered" was a better-sounding one that the design does not deliver. The sentence is corrected rather than the design changed, because the alternative — tombstones keyed by the object's minting month — makes sealed documents mutable, which `sharded-layout-corrections` rejected for reasons that still stand.

## Risks / Trade-offs

- [A retraction dated far ahead sits in the root until the calendar reaches it] → Visible in the hot document on every read, harmless to the layout, refused by any writer implementing D3, and warned on by any validator implementing D4.
- [Two clocks disagreeing at a month boundary still put a retraction and a mint in an order neither machine intended] → The layout no longer cares about the order; each object has one derived home and the index is a function of the files.
- [The validator's clock is the skewed one] → A warning, not an error; and a validator that is a month out has larger problems than this.
- [The `sharded-layout-corrections` claim in the dogfood workspace describes the two-clock rule] → Qualified by a claim recording this change; it was true at its timestamp.
