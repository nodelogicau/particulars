## Why

The README borrows from a handful of standards and two ideas, and credits each where it occurs or not at all. RFC 9562 and RFC 8785 are linked; RFC 8141 and YAML 1.2 are named; SHA-256 and the Model Context Protocol are named without a pointer; ORCID and DID appear as examples; the dialectic is credited to Hegel in one sentence and citation weight to PageRank in one word. A reader who wants to know what the format leans on, and for what, has to read all seventeen hundred lines. The intentions specification, which composes with this one, gathers its borrowings in a References section that names each source and the design it backs. This format asks every claim to say what backs it — "a claim that does not say what backs it is not one this format can reason over" — and its own README should meet the standard it sets.

Taking the inventory surfaced a gap. `timestamp` is compared — the current synthesis is the latest by `timestamp`, ties broken by id — sharded by — a retraction's month is where its `timestamp` falls — checked against a clock — a validator warns on a timestamp later than now — and offered to consumers for incremental fetching. No sentence in the README or in any spec says what a timestamp is. Every example writes `2026-08-20T11:02:00Z`; the reference implementation writes RFC 3339 in UTC at seconds precision and reads any RFC 3339 form; the dogfood workspace holds two hundred and twenty-one timestamps, every one of them `Z`. The behaviour is settled and unstated, and the one place it matters is the one the sharding rules did not cover: a retraction written `2026-09-01T00:30:00+02:00` falls in August in UTC and in September on the writer's wall clock, and only one of those is a month the format seals.

## What Changes

- **A References section.** After *Contributing* and before *License*, in the intentions form: standards borrowed as grammars, each with the field or rule it governs; identity schemes admitted as author URIs; the protocol the tool surface is defined against; the conceptual sources, each with the design it backs; and the ecosystem — particulars-cli, particulars.fyi, intentions. Only what the text leans on. Nothing added for completeness.
- **The dialectic is credited precisely.** Thesis, antithesis and synthesis stay the working vocabulary of *The Approach*. The References entry credits the triad in that form to Fichte, and its attachment to Hegel to Chalybäus's summary of him, and credits *Aufhebung* — which the README already uses — to Hegel himself, so that the one provenance claim a provenance format makes about its own idea is right.
- **Timestamps are specified.** A new requirement in `canonical-serialisation`: every timestamp field is an RFC 3339 `date-time`; writers write UTC with the `Z` designator at seconds precision; readers accept any RFC 3339 form and compare timestamps as instants; wherever the specification derives a calendar month from a timestamp, the month is the instant's UTC month; the typed data model carries a timestamp as its canonical string, so a file written with an offset signs identically to the same instant written in UTC. The README says so under *Identifiers*, beside the sentence that already distinguishes minting time from assertion time, and *Sharding* says which month an offset timestamp falls in.

Not **BREAKING**: every file a conformant writer has produced already satisfies the writer rule, and readers become more permissive, not less.

## Capabilities

### New Capabilities

None.

### Modified Capabilities

- `canonical-serialisation`: a new requirement defines the timestamp grammar, the writer/reader asymmetry, UTC month derivation, and the data-model form the signed payload carries.

## Impact

- `README.md` — *References*: new section between *Contributing* and *License*; *Identifiers*: a paragraph giving the timestamp grammar after the minting/assertion paragraph; *Sharding*: the month a retraction's `timestamp` falls in is its UTC month; *Trust and Provenance*: "the string this specification requires" gains its referent; *The Approach*: unchanged.
- `particulars-cli` — already conformant: `FormatTime` writes `Z` at seconds precision and `ParseTime` accepts any RFC 3339 form and returns UTC. One thing to confirm: that month derivation for retractions and the payload builder both take the parsed UTC instant rather than the string. Open an issue only if they do not.
- Dogfood: a claim in particulars-knowledge recording that the timestamp grammar went unstated from the first draft through v0.1 and twenty-five days past it, and that the gap was found by writing the bibliography — the inventory of what the format borrows is what showed it had borrowed one thing without saying so.
