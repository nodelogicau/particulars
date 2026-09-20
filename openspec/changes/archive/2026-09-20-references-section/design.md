## Context

The README cites inline where it borrows, unevenly: two RFCs are linked, two named, two standards and a protocol named without a pointer, one philosopher in one sentence, one algorithm in one word. The intentions README, which composes with this format, closes with a References section whose every entry names what it was borrowed for. The section there is the concrete form of a design principle, "Compose by reference, never by shared schema". Here it is the concrete form of a different principle: the format's own rule that an assertion says what backs it.

Writing the inventory showed that `timestamp` has no stated grammar. It is used in four load-bearing places — ordering syntheses, sharding retractions into months, the validator's clock check, and incremental fetching — and every use assumes a form no sentence gives.

## Goals / Non-Goals

**Goals:**
- A reader can find, in one place, everything the format borrows and the design each borrowing backs.
- Every entry is precise enough that it would survive the scrutiny the format applies to a claim's `source`.
- Timestamps have a grammar, a canonical written form, a comparison rule, and a month-derivation rule, stated once and inherited everywhere the specification uses them.

**Non-Goals:**
- Citing argumentation theory, epistemology, or provenance ontologies the text does not lean on. Toulmin, Brandom, W3C PROV and Dung are not sources of this format, whatever a dialectical knowledge format "should" cite.
- Linking every inline mention. Inline citations stay as they are; References is where the links and the reasons live.
- Changing the vocabulary of *The Approach*. Thesis, antithesis, synthesis are the words the format uses for its objects and they stay.
- A crediting line on particulars.fyi. The intentions site credits Heidegger under its hero; whether this site credits anyone is a landing-page question and a separate change if it is wanted.

## Decisions

### D1. References is a map of borrowings, not a bibliography

Each entry names the source and the field, rule, or design it backs — "RFC 9562, UUID version 7, for ids", not "RFC 9562". The intentions proposal that added its psychological sources put the discipline in one phrase: each naming the finding it supports. The form follows intentions exactly, so a reader of both sees one convention: a bold group label, entries separated by a middle dot, a link on each standard, and prose for the conceptual sources.

Groups, in order:

- **Standards borrowed as grammars.** RFC 9562 UUID version 7 for ids; RFC 3339 timestamps; RFC 8785 JSON Canonicalization Scheme for the signed payload; RFC 8141 URN syntax for the unregistered `urn:dkf:` namespace; YAML 1.2 as the file format, and the reason the typed-data-model rule exists; SHA-256, FIPS 180-4, as the document hash writers write.
- **Identity schemes admitted as author URIs.** ORCID; W3C Decentralized Identifiers, also the identity the reserved signature would bind; a GitHub profile URL. Admitted as examples of a URI that identifies a person, not required by the format.
- **Protocol.** The Model Context Protocol, against which the eleven-tool surface and the text the server tells the model are defined.
- **Models.** OpenSpec, the analogy *The Approach* draws — record how knowledge was formed, not its current state; iCalendar and RSS, the formats that specified the artefact and left the fetching to HTTP, which *Public Discovery* names as the shape of its publishing contract. The inventory (task 1.1) surfaced this group: each sentence loses its meaning without the source, which is the test in D2.
- **Conceptual sources.** Hegel, on *Aufhebung* and the movement of a contradiction into a richer position, behind synthesis carrying its inputs; Fichte, for the thesis–antithesis–synthesis triad in the form the README uses, and Chalybäus for attaching that form to Hegel; Page and Brin, PageRank, behind citation weight. Each entry says what it backs.
- **Ecosystem.** particulars-cli, the reference implementation whose feedback shaped the text; particulars.fyi, the visual introduction; intentions, the format that composes with this one for the prospective layer, as this one is its retrospective layer.

*Alternative: a bare bibliography.* Rejected. A list of RFC numbers tells a reader nothing the inline mentions do not, and the value of the section is the "for what".

### D2. Where it sits and what stays out

Intentions orders Status, References, License. This README has Contributing between Status and License, so References goes after Contributing and before License: the reader who has finished the spec and its process finds the sources, then the terms.

What stays out is anything the text does not lean on. The temptation in a format about claims and contradiction is to cite the argumentation literature. The README does not draw on it and the section does not pretend it does. The test for an entry is that a sentence of the README changes meaning if the source is removed.

### D3. The dialectic is attributed to where the words came from

The triad thesis–antithesis–synthesis, as three named steps, is Fichte's, from the *Wissenschaftslehre*; Hegel did not describe his own method in those words, and the attribution to him is Chalybäus's, from his 1837 history of German philosophy. What is Hegel's, and what the README already uses once, is *Aufhebung*: the contradiction is not discarded but taken up, preserved and overcome, in the position that resolves it — which is exactly what a synthesis carrying its `inputs` does. So the entry credits *Aufhebung* to Hegel, the triad to Fichte, and the popular attribution to Chalybäus, and *The Approach* keeps "Hegelian dialectic" as the reader's landmark with the References entry as the precise account behind it.

This is the one place a provenance format makes a provenance claim about its own founding idea, and it is the entry most worth getting right. The task that writes it verifies against primary sources before landing.

### D4. Timestamps are RFC 3339, written in UTC, read in any form

**RFC 3339, not ISO 8601.** RFC 3339 is a profile: one shape, `date-time`, with a mandatory offset. ISO 8601 admits `2026-08-20`, `20260820T110200Z`, week dates, and ordinal dates, any of which would make the sharding rule's "the month a timestamp falls in" need a parser the format never asked for. Intentions borrows ISO 8601 because it needs durations; this format needs instants, and RFC 3339 is the grammar of instants.

**Writers write UTC with `Z` at seconds precision.** Three of the four uses need timestamps to be comparable across writers who never met. Two files written in different zones with offsets compare correctly as instants and incorrectly as strings; two files written in UTC compare correctly either way, and a month is a substring. The format cannot rely on string comparison — see below — but it can make the conformant case the one where naive comparison happens to be right, so that a hand-written script over a conformant workspace gets the right answer. Seconds precision because assertion time is a human-scale fact and the reference implementation already writes it; sub-second precision on `timestamp` would suggest a resolution the field does not have.

**Readers accept any RFC 3339 form and compare as instants.** The writer/reader asymmetry is the rule everywhere else in this specification, and there is no reason to reject a hand-edited file carrying `+02:00` when its instant is unambiguous. Comparison is always as instants: `2026-08-20T09:02:00Z` is later than `2026-08-20T10:00:00+02:00`, and a string comparison says the opposite. The `current` synthesis rule and the validator's clock check therefore parse before they compare.

**Months are UTC months.** The sharding spec already says the id's month is the UTC month of its minting instant. It says the month of a retraction is where its `timestamp` "falls" and, with every timestamp so far written in `Z`, has never had to say in which zone. Now it does: the month of any timestamp is the month of the instant in UTC, stated once in this requirement and inherited by `workspace-layout` and `index-manifest` without editing either. A retraction at `2026-09-01T00:30:00+02:00` is an August retraction, and if August is sealed it is the validation failure `index-manifest` already describes.

**The data model carries the canonical string.** The signed-payload requirement already says the typed model formats a timestamp "back to the string this specification requires" and until now there was no such string. The canonical string is the instant in UTC with `Z`, with a fractional second present only when non-zero and with trailing zeros removed. So `2026-08-20T09:02:00Z` and `2026-08-20T11:02:00+02:00` build the same payload, as `0.9` and `0.90` already do, for the same reason: normalise the artefact, sign the assertion. Fractional seconds are kept rather than truncated because dropping digits a writer wrote would sign something other than what was asserted; a conformant writer writes none, so in practice the canonical string and the written string coincide.

*Alternative: permit offsets on write.* Rejected; it makes the conformant case the one where naive comparison is wrong, and buys nothing, since the offset carries no information the format uses.

*Alternative: require `Z` on read.* Rejected; it rejects files whose meaning is unambiguous, and the specification's reading rule is lenient everywhere else.

### D5. The requirement lives in `canonical-serialisation`

Not `object-identifiers`, which is about ids and already distinguishes minting time from assertion time without saying what either looks like. The timestamp rule is a serialisation rule — what a writer emits, what a reader accepts, what the data model holds — and the signed payload, which `canonical-serialisation` owns, depends on it. One requirement there, with the month-derivation clause, is inherited by every spec that uses a timestamp; the alternative was editing three specs to say the same thing.

## Risks / Trade-offs

- [The triad attribution is wrong in some detail] → Task 1.6 verifies against the primary sources before landing, and the entry is worded to claim no more than the sources support.
- [References rots as the spec grows] → The intentions practice: a proposal that borrows names its References entry in *What Changes*. Adopt the same practice here; the archived intentions proposals show it costs one clause.
- [A workspace holds a hand-edited timestamp with an offset near a month boundary] → Readers convert to UTC before deriving the month; the sharding guards and the validator already act on the derived month. The requirement makes explicit what the implementation already does.
- [Fractional seconds in the canonical string make two writers of the same instant disagree] → Only if one writes a fraction and the other does not, and a conformant writer writes none. The rule is stated for the non-conformant file, not the conformant one.
