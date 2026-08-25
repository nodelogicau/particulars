## Context

Reported feedback with the fix proposed by the reporter, like rounds #1–#15 — not a spec-first change, so it applies directly and closes with a comment. The reporter found it by running an older build against a newer workspace in CI; the dogfooding workspace nearly reproduced the data-loss variant independently the same week.

## Goals / Non-Goals

**Goals:** an older conforming implementation neither fails a drift check nor destroys cache rows when a newer record type appears.
**Non-Goals:** version negotiation, index schema versioning, or any change to what entries carry.

## Decisions

### D1. Preserve, don't drop — the reporter's word is the load-bearing one

Ignoring unknown entries on *read* is the easy half. The half that matters is the **rebuild**: `index` regenerates the file from the objects it knows, so without an explicit rule, tolerance on read coexists with destruction on write. "Preserve" makes the rebuild carry unrecognised entries through unchanged. The alternative — dropping them and calling the index authoritative only for known types — would mean the cache silently diverges by tool version, and a newer tool computing effective scope from the index gets wrong answers traceable to a tool that reported success.

One consequence worth stating: a preserved entry can go stale (its record retracted by a newer tool is fine — but its record *deleted* cannot happen in this format, which is what makes preservation safe). The only source of a wrong preserved entry is a workspace edited by hand, which the format already excludes.

### D2. Drift checks compare only what the checker understands

`index --check` compares a rebuild against the committed file. With D1, the rebuild contains the unknown entries verbatim, so in the common case the comparison passes naturally. The explicit rule matters for the checker that cannot rebuild (read-only contexts): entries of unrecognised type are excluded from the comparison rather than reported as `extra`. A check must not fail on evidence of a newer conforming writer.

## Risks / Trade-offs

- [A malformed entry could hide behind an unknown type] → Accepted; the entry is a cache row, and the object files remain the source of truth that validation actually reads.
- [Preserved entries make the rebuild not-a-pure-function of the files the tool knows] → Deliberate: the index is a cache of the *workspace*, not of one tool's view of it.
