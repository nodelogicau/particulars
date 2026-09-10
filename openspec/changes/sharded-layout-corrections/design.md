## Context

`sharded-layout` landed on 2026-09-10 as `dkf/0.2` and has no implementation yet. Its review from the implementation side (particulars-cli#11, and #25 and #26 raised from it) found that the shape contradicts itself in two places: the layout cannot place an id the read rules require it to accept, and the root index carries a list that grows with history in the change whose principle forbids exactly that. It also found the README wrong about the one existing reader and loose about what its headline number measured. All four are addressed here, before the version number acquires an implementation.

The constraints are the same as before: a file's path derived from its id alone; a rebuild that is a pure function of the files; sealed history byte-immutable; every operation's cost bounded by what it touches.

## Goals / Non-Goals

**Goals:**
- Every id the format accepts has exactly one derived path and one index home.
- Neither appending nor retracting rewrites anything that grows with history.
- "What changed since" — objects and retractions both — is the root plus the segments a consumer has not seen.
- The README says only what was measured, and describes the reference implementation as it is.

**Non-Goals:**
- Reopening any decision of `sharded-layout` that the review did not contest: month granularity, calendar over hex, every type directory sharded, the format bump.
- A general clock discipline for `retracted.timestamp`. One guard is added; what a retraction's timestamp means otherwise is unchanged.
- Changing how a `dkf/0.1` index records retraction.

## Decisions

### D1. A `legacy` shard, triggered by "no month derives"

The trigger is stated as a property of the derivation, not of the id's syntax: an id from which no month derives goes to `<type-dir>/legacy/`. That covers the draft's truncated ULIDs, a UUID of version 4, and anything else the read-side regex admits, in one sentence, and it means the rule needs no list of legacy forms to maintain. A UUIDv7 with an implausible timestamp still derives a month and goes there; the shard is for ids with no clock at all.

Its index entries live in `index/legacy.yaml`, listed first under `segments` so a consumer enumerating in order meets it before any month. It is not sealed — nothing minted it, so nothing can seal it — and it is exempt from *A sealed month gains no files*. In practice it never changes: a conformant writer mints only UUIDv7, so a legacy id can only arrive by copy, merge, or a non-conformant writer, and a rebuild that finds one reports the difference as ordinary drift.

*Alternatives, from #25:* refuse to migrate a workspace containing one — honest, but strands it on `dkf/0.1` and says nothing about a legacy id arriving later; exempt the type-directory root for legacy ids — makes the stray-file rule conditional on parsing the id, which is a lookup the layout was written to avoid. The reserved shard keeps both rules absolute. `legacy` over `unknown` because the directory name should say why the files are there.

### D2. Tombstones are keyed by retraction month and live in the segment for that month

The root's `retracted` list grew with history because it was keyed by nothing: every retraction ever, in one place. Two other keys were on offer. The object's minting month (#26 option 1) puts each tombstone beside its entry, but then a retraction rewrites a sealed month's document — or a sibling file, which is the same thing for a consumer that must now poll one file per month to learn what was retracted. The month the retraction *happened* (#26 option 2) makes tombstones an append-only log exactly like entries, and the observation that makes it cheap is that it needs no new file: a segment already exists per month, so it carries that month's retractions beside that month's entries.

```
index.yaml                          index/2026-09.yaml   (sealed)
  format: dkf/0.2                     format: dkf/0.2
  segments:                           entries:      minted in September
    - index/legacy.yaml                 - id: clm_01a0f3c1-…
    - index/2026-08.yaml              retracted:    retracted in September
    - index/2026-09.yaml                - clm_01a022f1-…   (minted in August)
  entries:     minted this month
  retracted:   retracted this month
```

What follows, each of which the earlier shape lacked:

- **Append and retract touch the root only**, and the root holds one month's worth of each. Nothing rewritten grows with history.
- **Sealed segments are byte-immutable without exception.** A retraction in October of an object minted in August goes in October's document, and August's is untouched.
- **"What changed since" is one read.** A consumer that last visited in August fetches the root and every segment newer than August, and has every object minted and every object retracted since. The earlier shape gave it the objects but made it re-fetch a root that grew forever for the retractions.
- **Filtering is bounded by the period filtered.** An object minted in month M cannot be retracted before M, so its tombstone, if any, is in a segment from M onward or in the root. Filtering this month's objects reads the root; filtering everything reads everything, which is what "everything" costs.

The current month becomes the later of the month of the newest id and the month of the newest `retracted.timestamp`. Both are in the files, so a rebuild is still a pure function of them. A month in which objects were retracted but none minted produces a segment with an empty `entries`, which is correct and slightly odd, and a month with neither produces no segment.

### D3. A retraction is not written into a sealed month

Keying by `retracted.timestamp` means a retraction dated into an earlier month would land in a sealed segment. The minting guard has the same shape and the same answer: implementations SHALL NOT write a retraction whose timestamp falls in a month earlier than the current one. A retraction that is "really" about last month is written with a timestamp of now and a reason that says so; the `reason` field is where that belongs. The guard binds writers; a reader that meets a violation reports drift on the segment, as with a skewed mint.

### D4. Legacy objects are filtered like any other, at the cost their nature implies

A legacy id has no minting month, so the "segments from M onward" rule has no M for it: checking whether a legacy object is retracted means reading every segment's `retracted`. That is proportional to history, and it is accepted rather than designed around, because it applies only to objects no conformant writer creates and whose number is fixed at migration. Putting legacy retractions into `index/legacy.yaml` instead would make that document change on retraction, trading a bounded-but-total read for a mutable segment; the read is the better trade.

### D5. The README says what was measured and what the reader does

The refusal caveat is withdrawn, not softened: the reference implementation has refused an unknown `format` on every verb since its first commit, so the sentence describing a reader that "may accept and misread" described no reader that exists. The rule stays, stated as the behaviour the reference implementation already has and every reader must share.

The cost paragraph keeps the index-parse measurement (1.3 s, 700 MB, ~6.7 KB per entry at 105,000 entries) and says that is what it is; adds the full-check measurement from the implementation side (~29 KB per entry marginal across real object files, so tens of gigabytes at a million); and draws the one conclusion both support, that the cost is linear in history. The larger number strengthens the case, which is exactly why the smaller one should not be left standing as the whole story.

## Risks / Trade-offs

- [A retraction that belongs to last month cannot be dated there] → Its `reason` can say so; the format has never promised that `retracted.timestamp` is anything but when the retraction was recorded. See D3.
- [A month with only retractions yields a segment with empty `entries`] → Correct and harmless; the segment is still a valid document.
- [Filtering a legacy object reads every segment] → Bounded by the number of segments, and only for objects that no conformant writer creates. See D4.
- [`index/legacy.yaml` is a segment that can change] → Only when a legacy id arrives, which only a copy, a merge, or a non-conformant writer can cause; a rebuild reports it as drift, which is what should happen.
- [The `sharded-layout` claim in the dogfood workspace now describes a superseded tombstone shape] → Qualified by a claim recording this change; the earlier claim was true of the spec at its timestamp and stays.
