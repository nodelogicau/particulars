## Why

Recall by query's `limit` caps how many particulars come back, but each particular returns its whole lineage. In a workspace where a few particulars hold most of the claims, a one-word query returns almost everything whatever `limit` is: on the dogfood workspace, `limit: 1` still returns 140 entries. Recall by particular has the same gap. The spec defines no limit for it at all, and the reference implementation's `limit` keeps the last N entries in lineage order, which can drop `current`. Raised as #38, point 1. This change is option (1b) from that issue, as refined in its 2026-10-29 comment: the one fix that bounds a response whatever the query, and the one that doesn't wait on particulars-bench.

## What Changes

- **A per-particular entry cap, `entry_limit`, for recall by particular.** It is optional and must be a positive integer. When it is supplied, each particular's part of the response keeps at most that many entries, chosen in a fixed order: `current` first, then unsynthesised entries, most recent first, then the rest, most recent first. The kept entries are returned in lineage order with `current` identified, as now.
- **The same cap for recall by query,** passed through to each particular's stage-two recall. Within a particular, after `current` and the unsynthesised entries, entries marked as matched are kept ahead of the rest. `limit` keeps its meaning, the number of particulars.
- **Every capped particular reports `omitted`:** how many entries the cap removed, so an agent knows to call recall by particular for the rest. It does not count entries removed by `scope`, `author` or `include_retracted`.
- **The cap does not change which particulars are returned.** Ranking in recall by query counts terms against each particular's uncapped response, so supplying `entry_limit` never changes the order or what `limit` keeps.
- **When `entry_limit` is omitted, nothing changes.** Responses are exactly as today. No implementation default is allowed, because two implementations would then return different entries for the same call.
- **No format version.** This is tool behaviour. No file is read differently and no file stops validating.

Out of scope: the order of particulars and the flood of matched entries (#38 point 2, and the `C#` and `is` cases). Those are for a second change, whole-word matching and a document-frequency tiebreak, decided on particulars-bench numbers.

## Capabilities

### New Capabilities
- `recall-entry-limit`: the `entry_limit` parameter for recall by particular, the order that decides which entries a cap keeps, the `omitted` count, and the rejection of a non-positive cap.

### Modified Capabilities
- `recall-query`: *Recall by query resolves to particulars, then recalls structurally* passes `entry_limit` through to stage two and adds the matched tier to the selection order. *Each result says how it was resolved* says ranking counts terms against the uncapped response.

## Impact

- `README.md`: the `knowledge_recall` row in *MCP Server Tools*; *Recall by query*, a paragraph on the cap and why it keeps what it keeps; Status, an entry for #38 point 1 that leaves point 2 open.
- `openspec/specs/recall-query`: two requirements modified. `openspec/specs/recall-entry-limit`: new.
- `particulars-cli`: `internal/query/recall.go:166` keeps the last N in lineage order and can drop `current`. It needs the selection order, `omitted`, and `entry_limit` on both CLI and MCP. Its existing `limit` on recall by particular can stay as a deprecated synonym.
- `particulars-bench`: no change required. Passing `entry_limit` is a later choice for the bench.
- Existing callers: unaffected unless they pass `entry_limit`.
