## Why

[Issue #16](https://github.com/nodelogicau/particulars/issues/16): the index's compatibility rule covers unknown **fields** but not unknown **entry types**. When a workspace gained `type: publish` entries, an older conforming build read every object file correctly — the format degraded exactly as promised — and then failed `index --check`, because a rebuild from the files it knows produces a set missing those entries, and nothing tells it not to report them as drift.

This is structural, not promotion-specific: every future record type breaks every existing drift check in the wild, and the failure lands on the derived artefact — the one place the format says compatibility is free. Worse, a rebuild that *drops* unknown entries turns a read-compatibility gap into data loss in the cache: an older tool touching the workspace strips the promotion rows, and the loss only surfaces when a newer tool next computes effective scope from the index. That case is not hypothetical — this workspace's own dogfooding nearly hit it with a v0.5.0 binary against a v0.7.0-era workspace.

## What Changes

- **The tolerance rule is extended from fields to entries**: future versions of the specification may add entry types; consumers ignore entries whose `type` they do not recognise.
- **A rebuild preserves unknown entries.** An implementation regenerating `index.yaml` MUST carry through entries whose `type` it does not recognise, byte-for-byte in canonical order, rather than dropping them.
- **A drift check does not report them.** Entries of unrecognised type are excluded from the comparison, so `index --check` passes across a version boundary.

## Capabilities

### New Capabilities
<!-- none -->

### Modified Capabilities
- `index-manifest`: the extension requirement covers entry types as well as fields, and gains the preserve-through-rebuild and drift-exclusion rules.

## Impact

- `README.md` — one paragraph in the `index.yaml` section.
- `openspec/specs/index-manifest/spec.md` — one requirement modified.
- Issue #16 — resolved with the suggested wording essentially as proposed; close with a pointer.
- `particulars-cli` — has offered to implement whichever closure is chosen; preserve-through-rebuild is the small change it anticipated.
