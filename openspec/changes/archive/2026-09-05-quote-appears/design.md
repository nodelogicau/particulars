## Context

`source-verification` has two comparison rules and states one of them. The hash is pinned to the byte: CRLF normalised to LF, nothing else altered, with the reason given — normalise what is an artefact of transport, leave every edit visible. The quote has only the word *appears*. The originating design (verifiable-provenance D2) treated it as self-evident: "did my span survive" becomes a substring search, and the drift table's fourth cell — quote absent, hash matches — was marked impossible on the grounds that the quote is a substring of the document. Its Open Questions listed normalisation as "real and unsolved" for the hash and did not mention the quote at all.

The reference implementation read *appears* literally. A quote that crossed a hard line wrap in an 80-column Markdown file did not appear (particulars-cli#9), and the "impossible" cell was the one reported, with a message that contradicted itself. Its fix (particulars-cli ac48d45, archived as `fold-quote-whitespace`) folds whitespace on both sides with `strings.Fields`, reserves a *never matched* message for the unchanged-hash case, and warns at assert time when a local quote does not match. #24 proposes that rule upstream; the review on #24 found the whitespace set unnamed, the "agrees with the hash" sentence over-broad, the no-hash states unnamed, and the empty quote undefined.

Constraints that shape every decision below: claim files are immutable, so a rule that makes an existing file invalid can never be satisfied by editing it; readers are lenient; two conformant implementations must report the same drift for the same claim and document, or the check is worthless as evidence.

## Goals / Non-Goals

**Goals:**
- One rule for *appears* that two implementations reproduce byte for byte, stated as precisely as the hash rule is.
- Every combination of the two signals named, including the ones the table left to inference.
- No existing claim regresses: everything that matched before matches after.
- The README's promise that a quote "survives insertion and reformatting" true as written.

**Non-Goals:**
- Format-aware matching: stripping blockquote or comment prefixes, unwrapping Markdown, reading code fences. The rule folds whitespace and nothing else, and says so.
- Fuzzy, case-insensitive, or Unicode-normalised matching. Those are edits under the hash rule, and the two signals agree about every edit that is not whitespace.
- Fetching. Verification stays best-effort and offline; nothing here changes which documents get checked, only how a checked one is compared.
- Prescribing a write-time check. An implementation that warns when a local quote does not match is being helpful, not conformant; the spec is silent.

## Decisions

### D1. Fold every run of Unicode White_Space to one space, on both sides, and trim the quote

*Appears* means: fold, then substring. Folding maps every maximal run of characters with the Unicode White_Space property to a single U+0020 and strips the quote's leading and trailing whitespace; the document is folded the same way. The quote appears when the folded quote is a substring of the folded document.

The set is named as a Unicode property rather than listed because a list is the gap this change closes. #24 and the reference implementation's delta spec both say "spaces, tabs, newlines, and blank lines"; the reference implementation actually folds `unicode.IsSpace`, which is White_Space and includes U+00A0 NBSP, U+0085 NEL, U+2028, U+3000 and the U+2000 block. An implementation reading the list would fold ASCII only and disagree on any quote copied from a web page, where NBSP is the commonest artefact. White_Space is stable across Unicode versions, defined in one place, and is what `strings.Fields`, Python's `str.split()`, and `\s` in JavaScript already implement.

*Alternatives:* fold only newlines, keeping spaces and tabs verbatim — re-opens the bug for any editor that converts tabs on save, and does not survive a re-indent. Fold ASCII whitespace only — reproducible, but loses the NBSP case for no gain. Exact match, with guidance to quote within a line — the state of affairs the issue exists to end.

Line-ending normalisation is not a separate step: CR is White_Space, so a CRLF checkout folds identically to an LF one. One step is easier to state and impossible to order wrongly.

### D2. Whitespace is where the two signals part, and the spec says so

The hash treats trailing whitespace as an edit; this rule treats it as nothing. That is not an inconsistency to paper over but the reason there are two signals. The hash asks *did anything change*; the quote asks *are the words still there*. A re-indented code block or a re-wrapped paragraph has changed and the words are still there, which is exactly what the table's middle row — context drift — was made to say. #24's sentence "the quote SHALL agree with the hash about what an edit is" is kept but scoped: for everything other than whitespace. Without the scope, a reader meets the trailing-whitespace scenario two paragraphs up and sees a contradiction.

The consequence is stated as a scenario: a whitespace-only edit inside the quoted span reports context drift. A claim whose subject is the whitespace itself — "the block is tab-indented" — loses its quote signal for that edit; the hash still reports it, and such claims are rare enough that the trade is right.

### D3. A paragraph break folds like any other whitespace

The alternative is to keep a blank line as a token, so a quote cannot silently join two paragraphs. Rejected for three reasons. The rule becomes two rules with a boundary to argue about (is a line of spaces a blank line? a `<br>`?). A substring test cannot police meaning either way: two adjacent sentences joined across a paragraph break are still adjacent, and a quote that misrepresents them does so in the writer's hand, visible to the reviewer reading it. And the reference implementation already folds all whitespace; a second rule would make it non-conformant for no interoperability gain.

### D4. Case, punctuation, and Unicode form are compared verbatim

NFC versus NFD, a curly quote for a straight one, a capital at a sentence start: under the hash rule each is an edit. If the quote folded them, the two signals would disagree about whether the document changed, and the middle row would fill with cases where the quote "survives" a document the hash says was edited *in the quoted span*. The point of two signals is that their disagreement is informative; that only holds if they agree about what counts.

### D5. Every cell of the table is named

Two signals, each of which can be present, absent, or unavailable, give more than three states. The requirement names them all:

| quote | hash | report |
|---|---|---|
| present | matches | nothing |
| present | differs | context drift |
| absent | differs | quote drift |
| absent | matches | quote drift, and the report SHOULD say the quote has never matched the unchanged document |
| present | none | nothing; the hash is unverified |
| absent | none | quote drift, without the never-matched inference |
| none | any | verification by hash alone, as today |

The unchanged-hash row is the one the originating design called impossible. It is what a miscopied quote, or a quote taken from a revision other than the one hashed, produces; it says the quote was wrong at the time of writing, not that the document moved. Saying so in the report matters because "the quote does not appear, though the document is unchanged" reads as a contradiction and sends the reader to check a document that never changed. The inference is available only when the hash matches — with no hash, nothing says whether the document moved, so the report says only that the quote is absent.

### D6. A quote that folds to nothing is not written, and is read as no quote

After folding, the empty string is a substring of every document, so an empty or whitespace-only quote would "appear" everywhere and verify nothing. The spec says a quote is verbatim text drawn from the document; nothing is not that.

Two enforcement points. A writer SHALL NOT write a quote that folds to nothing — the same footing as a `confidence` outside [0, 1]. A reader that meets one SHALL treat the mapping as carrying no quote, verify by hash alone, and SHOULD warn. Read-time leniency rather than invalidity because a claim file is immutable: a rule that rejects an existing file can never be satisfied, and the `uri` legacy alias is the precedent for "accept and warn" when the alternative is a file nobody can fix. Read as *no quote* rather than as *quote absent from the document* because quote drift is a condition about the source for a reader to resolve, and an empty quote is a malformed write; reporting it as drift would send someone to check a document that never moved. The reference implementation currently reports it as quote drift and will need a one-line change.

### D7. The rule is format-blind, and the spec says so beside it

Folding whitespace does not remove a `>` at the start of a blockquote's continuation line, a `//` inside a wrapped code comment, or a `#` in wrapped YAML. A quote spanning such a wrap still does not appear, and no whitespace rule can make it. Rather than grow toward format awareness — which would need to know the document's syntax, and would diverge between implementations on the first edge case — the spec names the limit so that a writer takes such quotes from a single line. This is the README's job; the requirement states the rule, the README states what it does not do.

### D8. The stored quote is never folded

Folding is a property of the comparison. The quote in the claim file is what the writer read, as they gave it, so a reviewer comparing by eye sees the source's own shape; this is the *Human audit without tooling* scenario, and it is why an offset was rejected in the first place. It also means no serialised byte of any existing claim changes, and no canonical-serialisation payload — and so no signature — is affected.

## Risks / Trade-offs

- [Two implementations disagree on the White_Space set across Unicode versions] → The property has not changed since Unicode 6.3 (2013), which removed U+180E; it is the most stable whitespace definition available, and naming the property rather than a list means a future addition is adopted identically everywhere.
- [A claim about whitespace itself loses its quote signal] → The hash still reports the edit as context drift. Accepted; see D2.
- [Folding a large document once per claim citing it] → Linear in the document, and the document is already read per claim for the hash. An implementation may fold once per document per run; the spec does not care.
- [The reference implementation changes behaviour for an empty quote] → One line, and no known workspace carries one. Filed for alignment alongside naming the property.
- [Writers rely on folding and stop taking care with quotes] → The quote must still match word for word, case for case; folding removes one class of false drift and adds no tolerance for anything else.
