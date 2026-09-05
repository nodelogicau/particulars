## Why

`source-verification` derives both drift states from whether a claim's `quote` "still appears in the fetched document" and never says what *appears* means. The same requirement pins the hash side to the byte — CRLF normalised to LF and nothing else altered — precisely so that two implementations agree on what an edit is; the quote side has no such rule, so two conformant implementations can already report different drift for the same claim and document, one folding whitespace and one not, and neither is wrong. The originating design (verifiable-provenance D2) called quote matching "a substring search" without arguing it, listed normalisation as "real and unsolved", and marked the cell *quote absent, hash matches* as "impossible; the quote is a substring of the document" — an impossibility that assumed the quote was taken from the same bytes the hash was.

The cost arrived on 2026-09-05. The reference implementation had read *appears* as an exact substring match, so a sentence quoted verbatim from prose wrapped at 80 columns could not be quoted across a line boundary at all (particulars-cli#9), and the "impossible" cell was the state it reported, with a message that read as a contradiction. The workaround — reproducing the wrap inside the quote — breaks the next time the document is re-wrapped, which is exactly the reformatting the spec's own rationale for a quote over an offset says a quote survives. The reference implementation adopted a folding rule ahead of the spec (particulars-cli ac48d45) and raised #24 asking the spec to settle it; the review on #24 found four things the proposal left open. This change settles all of them.

## What Changes

- **A quote appears in a document when, after folding whitespace on both sides, it is a substring of the document.** Whitespace is the Unicode White_Space property; every run of it folds to one space and the quote's ends are trimmed. Case, punctuation, and Unicode form are compared verbatim: for everything *other than whitespace*, the quote agrees with the hash about what an edit is. A quote that folds to nothing is never written, and a reader that meets one verifies by hash alone and warns. The stored `quote` stays verbatim as written; folding is a property of the comparison, never of the file.
- **Every combination of the two signals is named**, including the ones the table left implicit. Quote absent and hash unchanged is quote drift, and the report SHOULD say the quote has never matched the unchanged document, since it was miscopied or taken from another revision. With no hash, the quote is the whole signal: present is no drift with the hash unverified; absent is quote drift, without the never-matched inference.
- **A whitespace-only edit inside a quoted span is context drift**, not quote drift: the words the claim rests on did not change, the document around them did, and the hash reports it.
- **The rule is stated as format-blind.** It folds whitespace and nothing else, so a wrap whose continuation line carries a prefix — a Markdown blockquote's `>`, a code comment's `//` — still cannot be matched, and such a quote must be taken from a single line.

Not **BREAKING**: any quote that matched exactly still matches after both sides undergo the same folding, so no existing claim regresses. The one behaviour change is that a whitespace-only edit inside a quoted span moves from quote drift to context drift.

## Capabilities

### New Capabilities

None.

### Modified Capabilities

- `source-verification`: the requirement *Drift is determined from the quote and the document hash together* gains the definition of *appears*, the complete drift table including the no-hash and unchanged-hash states, and the whitespace-edit-is-context-drift rule; the requirement *A document reference may be structured* gains the rules that the stored quote is never normalised, that a writer refuses a quote folding to nothing, and that a reader treats such a quote as absent from the mapping.

## Impact

- `README.md` — Drift: the three-row table becomes complete, a paragraph defines *appears* and says why whitespace is where the two signals part, and the format-blind limit is stated beside it. The sentence "survives insertion and reformatting" becomes true as written.
- **Closes #24**, accepting its rule with the four review corrections: the whitespace set named, the "agrees with the hash" sentence scoped, the no-hash states named, the empty quote refused at write time and tolerated at read time.
- `particulars-cli` — already conformant on the matcher (`strings.Fields` is Unicode White_Space) and on the no-hash and unchanged-hash messages; its delta spec lists whitespace kinds rather than naming the property, and it reports an empty quote as quote drift where this change reads it as no quote. To be filed against particulars-cli for alignment.
- Dogfood: the claim on the spec particular recording #24 and its review (particulars-knowledge#38) wants a qualification synthesis once this lands.
