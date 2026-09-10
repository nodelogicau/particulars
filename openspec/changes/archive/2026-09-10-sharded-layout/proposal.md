## Why

A DKF workspace is append-only by design — a retraction appends, a synthesis keeps its inputs — so it grows without bound, and that is the product, not a defect. What is a defect is that three costs currently scale with the whole history rather than with what changed: every verb that reads `index.yaml` parses all of it (measured: 105,000 entries parse in 1.3 s and peak at 700 MB resident, so a million-entry workspace needs ~7 GB); every commit that adds a claim rewrites the git tree object for the entire `claims/` directory; and every hosted directory listing truncates at a thousand files. The filesystem is not the ceiling — APFS and NTFS are effectively unbounded and ext4 copes with millions per directory — but the whole-file index and the single flat directory are, and at agent-team rates of a few hundred objects a day they arrive within a year. The dogfood workspace's `claims/` passes a thousand files in about two months.

The fix is a principle and its first consequence. The principle: history may be unbounded, but the cost of any operation SHALL be bounded by the working set. The consequence: objects live in directories sharded by the minting month their own UUIDv7 id encodes, and the index is a small hot tail plus sealed, byte-immutable segments per month, with retractions carried as a tombstone list in the tail so a sealed segment never changes. Paths stay derivable from an id with no lookup. A change of *shape*, unlike every change of *fields* before it, cannot be made additively: an older reader that globs `claims/*.yaml` or unmarshals the index as one document would see a partial workspace and believe it complete, which is worse than refusing. So this is the first change that bumps the format version, and it is proposed now, while the only workspaces that exist are small enough to re-lay out in a second.

## What Changes

- **A principle, stated normatively.** No operation defined by the specification SHALL require reading an amount of data proportional to the workspace's history when the operation concerns only a bounded part of it: reading the working set, appending an object, checking the index for drift, and enumerating what changed since a point SHALL each be possible in cost proportional to what they touch.
- **Object files are sharded by minting month.** An object whose id was minted in month `YYYY-MM` (UTC, taken from the id's UUIDv7 timestamp) SHALL live at `<type-dir>/YYYY-MM/<id>.yaml`. The month is derived from the id alone; no lookup, no configuration, no `timestamp` field, which the spec already says may predate minting. A sealed month's directory never changes again except by the one modification the format already permits, a `retracted` block appended to a file within it.
- **The index becomes a hot tail plus sealed segments.** `index.yaml` carries `format`, a `segments` list naming one file per sealed month, `entries` for the current month only, and `retracted`, a complete list of the ids of retracted objects. Each segment at `index/YYYY-MM.yaml` carries `format` and `entries` for its month and, once sealed, SHALL never change. The current month is the month of the newest id in the workspace, so a rebuild is a pure function of the files. Index entries no longer carry `retracted: true`; the tombstone list is the single place a retraction shows, and it is what a remote consumer polls.
- **Fetch paths follow the shard.** A published object SHALL be fetchable at the feed path plus `YYYY-MM/<id>.yaml`. Segment paths in the index resolve relative to the index's own location. The `.well-known` manifest is unchanged.
- **BREAKING: the format version becomes `dkf/0.2`.** A `dkf/0.2` workspace declares itself in `dkf.yaml` and in every index file. A reader SHALL read both layouts, choosing by the declared version, and SHALL refuse a workspace whose `format` it does not implement, naming the version — a rule that `dkf/0.1` never stated and that binds every reader from now on. Existing `dkf/0.1` workspaces remain valid and readable indefinitely; nothing obliges migration.
- **Migration is a pure relayout.** Moving a `dkf/0.1` workspace to `dkf/0.2` moves each file to its derived path, regenerates the index, and rewrites `format`. No id, content, `source`, or canonical payload changes, so every signature still verifies, and git records the moves as renames.

## Capabilities

### New Capabilities

- `workspace-layout`: the bounded-working-set principle; the sharded directory layout and the derivation of a file's path from its id; the format version gate that makes a shape change safe; migration from the flat layout.

### Modified Capabilities

- `index-manifest`: the index is a root document with `segments`, `entries` for the current month, and `retracted` tombstones; sealed segments are immutable; the rebuild is deterministic from the files; the drift check is per segment plus the tail; `retracted: true` is no longer an entry field.
- `public-discovery`: the predictable fetch path gains the shard; segment paths resolve against the index.
- `workspace-config`: `format` may be `dkf/0.2`; readers refuse a version they do not implement.
- `retraction`: the index consequence of a retraction is a tombstone in the root index, not a flag on the entry.

## Impact

- `README.md` — File Layout: the sharded tree replaces the flat one, with `dkf/0.1` shown as the legacy shape; `index.yaml`: the root/segment/tombstone shape and the deterministic current-month rule; Public Discovery: the fetch path; a new short section stating the principle and the numbers behind it; `format: dkf/0.2` in every example.
- **Not** touched: object file contents, ids, `source`, canonical serialisation, signatures, scope, promotion, conflict semantics. The change is entirely in where files sit and how the index is cut.
- `particulars-cli` — read both layouts; write `dkf/0.2` on `init`; a `migrate` (or `layout`) verb; `index` and `index --check` per segment; `serve` and `validate` unchanged in behaviour; the drift check drops `retracted` from entry comparison and compares the tombstone list. To be filed once the spec settles.
- Dogfood: particulars-knowledge (220 entries, 163 claim files) migrates in one commit; its CI pins a CLI version and moves to one that reads `dkf/0.2`. The knowledge workspace records the change; the 2026-08-26 belief that the index is "a derived cache" is qualified, not reversed.
- Open, deliberately: shard granularity is month only. A workspace minting more than a few thousand objects a month would want days; that is a `dkf/0.3` question, or a `layout.shard` key, and is not decided here.
