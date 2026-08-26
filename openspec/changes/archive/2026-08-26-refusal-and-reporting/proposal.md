## Why

Two items from the reference implementation's review of `claim-evidential`, refined on [particulars-cli#4](https://github.com/nodelogicau/particulars-cli/issues/4) and decided there in substance.

First, the held-confidence rule names only validators. "Validators SHALL reject" leaves *writing* such a claim permitted, which is backwards for the one rule in this area a machine can settle — the mistake should be refused where it is made, not caught a review cycle later. And "reject" is ambiguous on the read side in a format where the file can never be fixed: a reader that refused to *read* a `held` + `confidence` file would strand it permanently.

Second, the specification's warning strategy assumes warnings get read, and nothing in it protects that assumption. Nearly everything settled recently is a warning — `scope_wider_than_inputs`, both drift states, unverifiable defects — and a validator whose output is 88 identical `undeclared` lines with one `quote_drift` in the middle spends all of that machinery. The reference implementation measured it: 104 lines of which the three actionable warnings were outnumbered seventeen to one, reduced to six lines once conditions were rendered by their nature.

## What Changes

- **Writers refuse; validators report and fail; readers never refuse to read.** The held-confidence requirement is reworded to name all three roles: writers SHALL refuse to create the claim, validators SHALL fail validation reporting `confidence_on_held`, and readers SHALL still read the file — it cannot be fixed, so refusing it would strand it.
- **Conditions are classified by nature, and the specification names the two kinds.** A **finding about an object** is something someone might act on — `quote_drift`, `context_drift`, `scope_wider_than_inputs`, an unverifiable defect, a dangling reference — and is reported per object, because the object is the unit of action. A **fact about the corpus** is something nobody can act on per object — `undeclared`, a legacy marker, `unverified_document` — and is reported in aggregate: its discovery value is spent the first time it is seen, its cost recurs forever, and it can never be cleared, because clearing it would mean rewriting an immutable file.
- **The rendering rule**: one condition, one line, with a count; the condition's message appears on the aggregate line only when it is uniform across the group, since attributing one object's reason to ninety-five is misreporting.
- The specification already sorts conditions into these piles without naming them — every "unverified rather than invalid" and "reported as an observation rather than a warning" is this distinction at work. This change names it once.

## Capabilities

### New Capabilities
- `condition-reporting`: the two kinds of condition, which existing conditions fall where, and the aggregate rendering rule.

### Modified Capabilities
- `claim-evidential`: the held-confidence requirement names writers, validators, and readers separately.

## Impact

- `README.md` — the Confidence subsection gains the three-role sentence; a short paragraph (likely under Design Principles or near the validation-adjacent prose) names the two kinds of condition.
- `openspec/specs/` — one capability added, one modified.
- particulars-cli — shipped the reporting half in `f6fe937` ahead of this change; the evidential surface, including write-time refusal, is planned but not built. Nothing here contradicts either.
- particulars-cli#4 — resolved by this change; close after applying.
