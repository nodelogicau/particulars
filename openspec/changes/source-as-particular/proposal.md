## Why

`source.author` is a bare string. In the dogfood workspace every one of 150 objects says `author: ben`, and nothing in the format can say *which* Ben — not across two workspaces, not across a federation, not to the signature the Trust section reserves for "the publisher's DID". The format made particulars the anchor for everything it knows about the world and then left the one particular that recurs in every workspace — the person or agent asserting — as a label on a leaf. Two consequences follow. "Everything Jane said" is a full-text search, and Jane's reliability cannot be computed even though the format already records what would compute it: retraction `kind: defect` "counts against the process that produced the claim", and today that process is identified only by `harness`.

The second gap is the one a knowledge format written mostly by agents hits first. Most of what an agent records is testimony — *Jane said the split happened in Q2* — and DKF, rightly, has no reportative evidential: someone looked, and what they looked at is the `document`. But the document mapping has no way to say **who produced what was read**, so the speaker of every reported claim lives in prose, where it can be neither queried nor joined.

Why now: v0.1 is declared and the deferred list has no opener. Three of its items — signature suites and DID binding, promotion by particular, and whether a synthesis has a `document` — all turn on whether identities become particulars. This change is additive, breaks no reader, and pulls those three toward a decision without taking any of them.

## What Changes

- **`source.author` may identify a particular.** A value that is a particular id or URI identifies that particular; a bare name is resolved best-effort against labels and aliases and otherwise stands as an opaque name, exactly as today. Writers SHOULD write the particular's **URI** — not its `par_` id — when the author is a defined particular, because an author is the one particular whose identity must survive leaving the workspace. The `source` minimum (author or harness) is unchanged.
- **The structured `document` gains an optional `author`**: who produced what was read. Same value forms. This is the reportative case — "Jane said X" is a claim by whoever recorded it, `observed`, whose document is Jane's utterance and whose document author is Jane. `ref` remains required; an unrecorded utterance already has a `ref` form.
- **Two attribution relations are defined**, both computed through merge equivalence classes: an object is **asserted by** the particular its `source.author` resolves to, and **reported from** the particular its `source.document.author` resolves to. `knowledge_recall` gains an `author` filter returning both, distinguished. Index entries MAY carry `author` and `document-author` so the filter runs without opening files.
- **Resolution never guesses.** A name matching more than one particular resolves to none of them, and `particular_resolve` reports ambiguity rather than picking — the spec currently says only what happens on zero matches.
- **Asserter attribution generalises harness attribution**: the retraction-kind observation the Trust section defines for `harness` applies to any resolved author, so a defect rate is computable per person or agent, not only per harness.
- **Disclosure is stated, not gated.** A promoted claim discloses its author URI with it, and a `document.author` discloses *who is being quoted* as completely as a `quote` discloses what they said. The spec says so, in the register the quote-disclosure rule already uses. Particulars do not gain a scope in this change.

Nothing here is **BREAKING**: every existing file is valid and reads as before, and a reader that ignores the new fields loses the join and nothing else.

## Capabilities

### New Capabilities
- `source-attribution`: author references resolving to particulars; `document.author`; the asserted-by and reported-from relations over merge classes; the writer-URI and reader-lenient rules; resolution that never guesses; asserter attribution; the disclosure statement; the `knowledge_recall` author filter.

### Modified Capabilities
- `source-provenance`: `author` may be a particular reference (id, URI, or name); the minimum-content rule is restated to cover the reference forms.
- `source-verification`: the document mapping gains optional `author`, written after `ref`.
- `merge-records`: the equivalence class also governs attribution queries, not only subject queries.
- `index-manifest`: entries MAY additionally carry `author` and `document-author`.

## Impact

- `README.md` — `Source` gains the reference forms and the writer-URI rule; `Verifiable documents` gains `author` in the mapping and its field order; `DPARTICULAR` gets a paragraph on people and agents as particulars (a person's URI is the one they are willing to be cited under at the widest scope their claims may reach); `knowledge_recall` and `particular_resolve` rows change in the tool table; `index.yaml` example and baseline-fields paragraph; `Trust and Provenance` "Harness attribution" becomes asserter attribution and notes that the reserved signature's natural binding is the author particular's URI.
- **Deferrals touched, none taken.** DID-signed retractions without author/harness stay with the signing change, but the identity a signature would bind is now nameable. Promotion by particular stays deferred. Whether a synthesis carries `document` stays open; `document.author` applies wherever `document` does and sharpens the question rather than settling it.
- **Not in this change:** a `kind`/sortal on particulars — explored alongside this and worth its own proposal; `harness` as a particular reference, which stays a string; a scope on particulars.
- `particulars-cli` — `claim assert` accepts `--author` as id/URI/name and `--document-author`; `particular define` is how a person becomes citable; `recall --author`; index gains the two fields; `validate` reports an unresolvable-but-well-formed reference as unverified, never invalid. Its agent skill needs one new instruction: when the user names who told them something, put it in `--document-author`, not in the content.
- Existing workspaces: `author: ben` claims become asserted-by Ben the moment a particular with alias `ben` is defined — retroactively and without touching a file, which is the payoff of resolving names at read time rather than requiring writers to have known.
