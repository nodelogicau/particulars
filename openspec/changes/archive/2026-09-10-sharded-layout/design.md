## Context

Every DKF operation today touches history in proportion to its size. `index.yaml` is one YAML document that every index-reading verb parses whole: 105,000 synthetic entries parse in 1.3 s at 700 MB resident, against 80 ms and 24 MB for the 220-entry dogfood workspace, so the parsed tree costs about 6.7 KB per entry and a million-entry workspace needs ~7 GB. `claims/` is one flat directory, so git rewrites its entire tree object on every commit that adds a claim, and hosted listings truncate it at a thousand files — which the dogfood workspace reaches in about two months at fourteen objects a day. The filesystem is not the limit: APFS and NTFS are effectively unbounded, ext4 handles millions per directory. The limits are the format's own shapes.

Three facts already in the spec make the fix cheap. Ids are UUIDv7, so every id carries its minting instant (object-identifiers); the index is a derived cache reconstructible from files (index-manifest); and signatures are over the canonical data model, not file bytes (canonical-serialisation), so a file can move without anything it asserts changing. One fact makes it the first non-additive change: the leniency rules that let older readers survive new fields and new entry types say nothing about a new *shape*, and an older reader meeting one would not fail — it would see a partial workspace and report it as whole.

## Goals / Non-Goals

**Goals:**
- Every operation's cost bounded by the working set it concerns, stated as a requirement so a future shape is judged against it.
- A file's path derivable from its id alone, with no lookup, no configuration, and no field of the file.
- Sealed history byte-immutable, so git never rewrites it and an HTTP consumer can cache it forever.
- An older reader that meets the new shape refuses, naming the version, rather than misreading.
- Migration that changes nothing any signature covers.

**Non-Goals:**
- Compacting knowledge. No object is removed, merged, or summarised; a retraction still appends and a synthesis still keeps its inputs. This change moves files and cuts the index; it forgets nothing.
- Packing objects into multi-object files. It breaks the id-to-path derivation that public discovery relies on, for a gain (fewer HTTP requests) that a segment-aware consumer gets anyway.
- Choosing shard granularity per workspace. Month is fixed; see D6.
- A frontier or current-beliefs view. Useful, additive, and a separate change.
- Streaming the index as a YAML document stream. It fixes memory but not git trees or listings, and has the same old-reader hazard; segments fix all three.

## Decisions

### D1. The principle is a requirement, not a remark

"History unbounded, working set bounded" could sit in the README as design philosophy. It is written as a requirement because the next shape proposal — a frontier view, a day-granularity shard, a pack format — needs something to be judged against, and because the failure it forbids is invisible until it hurts: nothing in a 220-entry workspace signals that the index is parsed whole. The requirement names four operations the format defines (read the working set, append an object, check drift, enumerate what changed since a point) and says each SHALL be possible in cost proportional to what it touches. It does not name an algorithm.

### D2. Shard by the id's minting month, in UTC

The shard key is the calendar month of the UUIDv7 timestamp in the id's first 48 bits: `claims/2026-09/clm_01a0f3c1-….yaml`. Three choices inside that.

*The id, not `timestamp`.* object-identifiers says assertion time may precede minting time and consumers must not require them to agree. A claim recorded in 2026 about a 2019 document has `timestamp: 2019-…` and an id minted in 2026; it belongs in the 2026 shard, where it was written, and only the id says so without opening the file.

*Calendar month, not hex prefix.* Four hex characters of the timestamp give 49.7-day buckets with no date arithmetic, which is how git fans out its object store. Rejected because a human reads these paths in diffs and pull requests, and `2026-09/` says what `01a0/` does not. The arithmetic is one integer division.

*Every type directory, not just claims.* `particulars/` holds nine files and will hold dozens; sharding it looks fussy. It is sharded anyway so that path derivation is one rule for every prefix, with no per-type exception a consumer must know.

*Alternatives:* shard by subject particular — groups what is recalled together, but a subject is a field of the file, not of the id, and a claim's subject can be merged; shard by scope — mutable in effect through promotion.

### D3. The index is a hot tail, sealed segments, and a tombstone list

```
index.yaml                          index/2026-08.yaml  (sealed)
  format: dkf/0.2                     format: dkf/0.2
  segments:                           entries:
    - index/2026-08.yaml                - id: clm_01a021ab-…
    - index/2026-09.yaml                  …
  entries:            (current month)
    - id: clm_01a0f3c1-…
  retracted:          (every retracted id, sorted)
    - clm_01a022f1-…
```

*The current month is the month of the newest id in the workspace.* Not the clock: a rebuild is then a pure function of the files, two implementations rebuilding on different days produce the same layout, and the drift check compares like with like. On the first rebuild after a new month's first object is minted, the previous month's entries move from `entries` into a new segment file. That is one large diff a month, which is the expected shape of a log rotating.

*Retractions are a list in the root, and entries carry no flag.* `retracted: true` on an entry is the one mutable index field, and it is what would force a sealed segment to change. Moving it to a list in the tail makes every segment byte-immutable once sealed, which is what lets git leave its tree alone and lets a remote consumer cache a segment indefinitely and poll only the root. The list is complete — it holds every retracted id, including ones whose entry is in the tail — so there is one place to look, and `knowledge_recall --include-retracted false` still filters without opening a file. The alternative, regenerating the affected segment, keeps segments logically sealed but not physically, and a consumer cannot tell a retraction from any other reason to refetch.

*Each segment is itself a valid index document.* `format` plus `entries`, nothing else. A tool that understands the entry shape understands a segment, and a segment can be validated alone.

*The drift check is per document.* Tail against regenerated tail, each segment against its regenerated self, the tombstone list against the regenerated list. The MAY-field tolerances of index-manifest carry over unchanged; the `retracted` entry rule is replaced by list comparison: an id in one list and not the other is reported.

### D4. `dkf/0.2`, and a reader refuses a version it does not implement

The additive path — a `layout: sharded` key in `dkf.yaml` that older readers ignore — is exactly the failure to avoid. workspace-config requires readers to ignore unknown keys, so a `dkf/0.1` reader would open the workspace, glob `claims/*.yaml`, find nothing, and report an empty workspace with no error. The same reader unmarshalling the new `index.yaml` as one document would see the tail and believe it the whole. Partial-and-silent is worse than refused, and the only thing every reader is guaranteed to read before anything else is `format`.

So the version string changes, and workspace-config gains the rule `dkf/0.1` never stated: a reader SHALL refuse a workspace whose `format` names a version it does not implement, and SHALL name the version. Honesty about what this binds: a `dkf/0.1` reader written before this rule may accept `dkf/0.2` and misread. There is one such reader, the reference implementation, and it is updated with this change. Every reader from now on is bound.

A `dkf/0.2` reader SHALL read `dkf/0.1` workspaces as well, choosing the layout by the declared version. Nothing obliges a workspace to migrate; a flat `dkf/0.1` workspace remains valid indefinitely, and the ceilings it faces are documented rather than forbidden.

### D5. Migration moves files and changes nothing they assert

`dkf/0.1` to `dkf/0.2` is: move each object file to its derived path; regenerate the index in the new shape; rewrite `format` in `dkf.yaml`. Ids, contents, `source`, `retracted` blocks, and canonical payloads are untouched, so every signature verifies before and after, and git detects the moves as renames with full history. A reader that cannot prove the rewrite changed no payload has not implemented the migration correctly; the spec says so as a scenario.

### D6. Month is the only granularity, for now

At the dogfood rate a month is ~420 objects; at five hundred a day it is fifteen thousand, past the hosted-listing limit though well within git and the filesystem. A per-workspace `layout.shard: day` key would fix that and reintroduce configuration into path derivation, which D2 exists to avoid — a remote consumer would need the manifest to know the path shape. Fixed month now; if a workspace reaches that rate the choice is between a `dkf/0.3` with day shards and a manifest-declared granularity, and there will be evidence to choose on.

### D7. What "sealed" means, precisely

A sealed month's *directory* gains no files: every id minted in that month already exists. A *file* within it may still change in the one way the format has always permitted, by appending a `retracted` block. A sealed *index segment* never changes at all, because retraction shows in the tombstone list. So git may rewrite one object file in an old month when it is retracted, and never rewrites an old segment or an old directory's tree for any addition.

The one way a sealed segment could need to change is an id minted into a past month — a machine with a badly skewed clock. object-identifiers already requires monotonic minting within an implementation; skew across machines of a month is implausible, and if it happens the drift check reports the segment, which is the right outcome.

## Risks / Trade-offs

- [A `dkf/0.1` reader that predates the refuse rule misreads a `dkf/0.2` workspace as small and empty] → One such reader exists and is updated alongside. The rule binds all readers from now on; the risk is confined to a binary nobody should be running against a workspace it did not write.
- [Two workspaces of the same knowledge, one flat and one sharded, have different paths for the same id] → The path is derived from the id and the declared version; nothing else keys on paths. Cross-workspace references are by id and URI, never by path.
- [Month rollover produces one large index diff] → Once a month, moving the tail into a segment; expected and reviewable. An implementation may seal eagerly on the first write of a new month rather than on the next rebuild; the result is the same.
- [Clock skew mints an id into a sealed month] → Drift check reports it. Implausible at month scale; see D7.
- [A remote consumer caches a segment forever and misses a skew-induced change] → Same case; the root index's tombstone list and tail are polled, and an implementation that reseals a segment SHOULD change its name or note it in the root. Not specified further until it happens.
- [`particulars/2026-08/` for nine files looks like ceremony] → One derivation rule for every prefix is worth nine files in a subdirectory.
- [The reference implementation carries two layouts indefinitely] → Reading `dkf/0.1` is a glob and a single-document parse; the cost is one code path that exists today.
