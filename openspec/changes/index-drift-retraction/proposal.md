## Why

`attribution-review-round` (D5, closing #21) let a drift check tolerate a MAY field absent from the committed index, so that a newer implementation writing `author` into entries would not fail every index committed before the field existed. The rule is one word too wide. `retracted: true` is a MAY field, and its absence is not "unknown to the writer" — it is the value *false*. A claim retracted after the index was committed appears in the rebuild as `retracted: true` and in the committed index as nothing, and the rule as written tolerates exactly that. Retraction is the one mutation an immutable object permits, which makes it the one staleness a drift check exists to catch (#22).

The design saw the hazard from the other side — it rejected comparing baseline fields only because "`scope` and `retracted` are MAY fields whose staleness the check exists to catch" — and then wrote a rule with the same weakness for absence.

## What Changes

- **The tolerance is stated by its reason, and the reason excludes `retracted`.** A drift check exists to catch the index lagging *changes to the workspace*. A presence difference in a field that mirrors an **immutable** property of the object — `scope`, `topics`, `timestamp`, `author`, `document-author` — cannot be a change, so it is not drift. `retracted` mirrors the only mutable property, so it is compared as present with its meaning: absent is `false`. The next MAY field classifies itself by asking whether what it mirrors can change.
- **The tolerance is symmetric.** Immutability makes a presence difference a non-change in either direction, so a field present in the committed index and absent from an older tool's rebuild is no more drift than the reverse. #21 only tolerated absence from the committed side.
- **A rebuild preserves unknown fields**, as #16 made it preserve unknown entry types. Without this, an older tool's rebuild strips `author` from every entry and the newer tool's next check — now symmetric — tolerates the stripping, so nobody learns the cache degraded. Cache loss rather than data loss, since the files are the truth, but the sentence that fixed types costs nothing to extend.
- **One scenario lands verbatim from #22:** a committed entry with no `retracted` and a regenerated entry with `retracted: true` is reported, because the object was retracted after the index was committed.

Not **BREAKING**: every existing index remains valid; the check becomes stricter in one case where it was wrong and looser in one direction where it was already right.

## Capabilities

### New Capabilities
<!-- none -->

### Modified Capabilities
- `index-manifest`: the drift-check tolerance is restated on the immutability criterion, made symmetric, and `retracted` is compared as present; a rebuild preserves unknown fields as well as unknown entry types.

## Impact

- `README.md` — the `index.yaml` section: the tolerance paragraph rewritten (criterion, `retracted`, symmetry) and the preserve sentence widened from entry types to fields.
- **Closes #22**, and answers the two extensions the review of it raised: symmetry, and unknown-field preservation.
- `particulars-cli` — per the implementation note on #22: mask the rebuilt entries to the committed entries' presence of the *immutable* MAY fields before encoding, then compare bytes as before; an old index passes, formatting drift is still caught, a new retraction fails. Preserving unknown fields on rebuild is the field-level twin of what #16 already required. To be added to `particulars-cli#7`'s list.
