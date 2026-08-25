## Why

DKF's first design principle is that provenance is non-negotiable, and its weakest field is provenance. `source.document` is an optional, unvalidated URI string: it carries no revision, no location within the source, and nothing that could later be checked. Three consequences follow, and all three are live today.

A claim cannot be **audited**. Nothing records which part of the document was read, so a claim that subtly misstates its source — the characteristic failure of LLM extraction, where the misreading is invisible precisely because the output is fluent — is undetectable by any means the format provides.

A claim cannot **detect drift**. DKF tracks staleness inward, reporting syntheses whose inputs were retracted, but nothing looks outward. A document edited after a claim cites it silently changes what that claim rests on, and the workspace continues to present the claim as current belief.

A retraction cannot be **classified**. There is one mechanism and a free-text `reason`, so "the claim misread its source" and "the source was right then and is wrong now" are indistinguishable. They carry opposite signals — the first impeaches the process that produced the claim, the second is ordinary knowledge evolution — and collapsing them means neither can be acted on. This is why `source.harness` has been recorded since the first draft while the harness attribution it was recorded for has never been computable: the format captures who produced a claim but never whether they produced it correctly.

## What Changes

- **`source.document` MAY be a structured reference** carrying `uri`, an optional `hash` of the document as fetched, and an optional `quote` giving the verbatim text the claim was drawn from. A bare string remains valid, so existing workspaces stay conformant and a consumer that ignores the structure still gets a readable URI.
- **The span is a verbatim quote, not an offset.** Line and byte ranges break when text is inserted above them, producing drift reports for edits that touched nothing relevant. A quote is content-addressed, survives insertion, and can be checked by a human reading the diff with no tooling.
- **Drift is defined over both hashes.** Whether the quote still appears in the source and whether the document hash still matches are two signals, and their disagreement is the informative case: a quote that survives inside a document that changed means the *context* around the claim moved, which can falsify a claim whose text is untouched.
- **`retracted` gains an optional `kind`**: `defect` (the claim misread its source), `supersession` (the source was right then, wrong now), or `provenance-failure` (the source itself was wrong). These are not a taxonomy but the three joints in the chain `claim → source → world`.
- **The kind is declared and cross-checked, never inferred.** The retractor knows why; a validator that can reach a hashed source can contradict them — a `supersession` against an unchanged document is a warning, because nothing moved.
- **Verification is best-effort throughout.** Sources that cannot be hashed — a conversation, a recollection, a paywalled page — remain first-class. A `kind` on such a retraction stands unverified rather than invalid, and no requirement obliges a consumer to fetch anything.

## Capabilities

### New Capabilities
- `source-verification`: the structured document reference, quote-as-locator, the drift states derived from the two hashes, and the best-effort rule for sources that cannot be fetched or hashed.

### Modified Capabilities
- `source-provenance`: `document` may be a structured reference as well as a string.
- `retraction`: the `retracted` block gains an optional `kind`, with the cross-check against source drift.

## Impact

- `README.md` — the Source subsection gains the structured form and the drift states; Retraction gains `kind`; Trust and Provenance can finally say what harness attribution is computed from.
- `openspec/specs/` — one new capability, two modified.
- Issues — none open; this originates from a design review rather than reported feedback, and would be worth raising with the reference implementation before it is applied.
- `particulars-cli` — `validate` gains a drift check and a kind cross-check, both requiring network access for remote sources and therefore both optional. The `retract` verb gains `--kind`. Nothing existing becomes invalid.
- **Deliberately out of scope**: the evaluative-versus-evidential distinction on claims, which came out of the same review and is the more consequential idea, but touches how synthesis and conflict detection work rather than how provenance is recorded. Also out of scope: reporting retracted objects that leave a particular with no surviving belief, which needs no new fields and belongs with conflict semantics.
