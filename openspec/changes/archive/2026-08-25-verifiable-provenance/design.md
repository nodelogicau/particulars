## Context

This change comes out of a design review comparing DKF against an independently-developed personal knowledge graph, which reached many of the same conclusions from a different direction — claims as the atom, immutability, append-only correction, never deleting to improve quality. Where the two designs diverge is instructive: that system treats provenance as a non-null foreign key to an immutable `(document, revision, span)`, while DKF treats it as an optional URI string. Both call provenance the product. Only one of them can check.

The relevant constraints are unchanged from prior rounds. DKF is files in git, reviewed by humans in pull requests and written mostly by agents. Readers are lenient and writers strict. A consumer that ignores a feature must still get valid, readable YAML. And the format has now had three rounds of feedback, so the bar for adding surface is higher than it was: anything introduced here has to pay for itself against a process that needs it.

One piece of history matters. The README has claimed since the first draft that recording `source.harness` "enables downstream reasoning about the reliability of a synthesis chain in a given domain." No implementation has ever done this, and none could: the format records who produced a claim and never whether the claim was sound. This change is the first that makes that ambition reachable.

## Goals / Non-Goals

**Goals:**
- Make a claim checkable against the text it came from, by a human in a diff or by a tool.
- Detect when a source has changed under a claim that cites it.
- Separate the two signals currently collapsed into a free-text retraction reason.
- Keep every one of these optional, so unhashable sources and offline consumers remain first-class.

**Non-Goals:**
- Requiring provenance to be verifiable. A claim from a conversation is a legitimate claim.
- Fetching, caching, or archiving source documents. DKF says how to record a reference, not how to preserve what it points at.
- Deciding whether a claim actually misstates its quote, which needs a reader.
- The evaluative-versus-evidential distinction on claims, deferred deliberately.

## Decisions

### D1. `source.document` may be structured, and a string still works

```yaml
source:
  author: ben
  harness: claude
  document:
    uri: https://example.com/docs/architecture.md
    hash: sha256:9f2a…          # of the document as fetched, optional
    quote: |                    # verbatim, optional
      The billing service listens on port 8443 behind the ingress.
```

`document: https://…` remains valid and means exactly what it means today. This is the same shape as every prior extension in this format: additive, ignorable, and degrading to something a human can still read.

*Alternative considered:* a separate top-level document object with its own id, as the comparison system uses. Rejected — that system needs document identity because many claims share a source and it enforces provenance as a foreign key. DKF has no referential integrity to enforce and no join to optimise, and a fourth knowledge object would cost far more than it returns. The URI is already the identity.

### D2. The locator is a verbatim quote, not an offset

Line ranges and byte offsets are the obvious choice and the wrong one for this format. DKF does not control its sources; they are edited by other people, and an insertion anywhere above a span moves it without changing it. Offsets would therefore report drift for edits that touched nothing relevant — and a check that cries wolf is a check reviewers learn to skip, which is the failure mode this project already reasoned through when specifying `scope_wider_than_inputs`.

A quote is content-addressed. "Did my span survive" becomes a substring search, insertion above is a non-event, and the quote survives reformatting that offsets would not. It also does something no offset can: it makes the claim auditable by a person reading the pull request, with no tooling and no network — which is the review model DKF actually runs on.

The cost is duplication: the quote is source text copied into the claim file. That is real, and it is the price of a format whose files must be self-describing.

### D3. Drift is the disagreement between two hashes

Hashing the quote alone is insufficient, because decontextualisation pulls in meaning the quote does not contain. A document reading "In staging, the billing service listens on 443" yields the claim "the billing service listens on 443"; changing "staging" to "production" falsifies the claim without touching a character of the quote. Hashing only the document is sufficient but noisy — every typo anywhere flags every claim citing the file.

Recording both makes the interesting state observable:

| quote present | document hash | meaning |
|---|---|---|
| yes | matches | nothing moved; the claim rests where it was |
| yes | differs | **context shifted around the quote** — review |
| no | differs | the cited text itself is gone or changed — review |
| no | matches | impossible; the quote is a substring of the document |

Row two is the case that motivated this and it is invisible with either hash alone. Row three is the louder failure and the easier one. Neither is an error: both are conditions a reader resolves, in keeping with how every other structural signal in this format works.

### D4. Retraction kind is declared, not derived

The tempting derivation is that a retraction with no `superseded-by` is a defect and one with a replacement is a supersession. It does not survive contact:

| | `superseded-by` present | absent |
|---|---|---|
| **defect** | the typo fix — which is the workflow the reference implementation documents | the claim was invented; the source never said it |
| **supersession** | a value changed, 443 → 8443 | the service was decommissioned; nothing replaces the fact |

All four quadrants occur, so the axes are independent, and the top-left is fatal to the rule: the most common defect ships *with* a replacement. `superseded-by` answers "did anything replace this", which is a different and also useful question, but it does not classify why the claim died.

So `kind` is declared by the retractor, who knows. What a validator can do is contradict them where the source is reachable — a `supersession` recorded against a document whose hash is unchanged is a warning, because nothing moved to supersede it. Declared value, mechanical cross-check: the same division of labour used for conflict detection and for derived disclosure.

### D5. Three kinds, because there are three joints

`defect`, `supersession`, and `provenance-failure` are not a taxonomy someone chose. They are the places the chain can break:

```
   claim ─────────▶ source ─────────▶ world
     │                 │                │
     ▼                 ▼                ▼
 misreads what    the source        the world
 the source says  was wrong         moved on
     │                 │                │
  defect      provenance-failure   supersession
```

This matters because a list invented by category tends to grow — the comparison system explicitly guards against exactly that explosion by keeping its open axes open. A closure derived from structure is stable: there is no fourth joint.

Their consequences differ, which is what makes the distinction worth recording at all. A `defect` impeaches the process that produced the claim, so it is evidence about that `source.harness` and about sibling claims from the same run. A `supersession` impeaches nothing. A `provenance-failure` impeaches the document, and therefore everything else citing it.

### D6. Verification is best-effort, everywhere

No requirement obliges anyone to fetch anything. A validator without network access, or a source behind a paywall, or a claim drawn from a conversation, all produce "not checked" rather than "invalid". A `kind` on an unverifiable retraction stands unverified. This is stated rather than implied, because a format that made auditability mandatory would push authors toward citing only what is convenient to cite, which is worse provenance than an honest unverifiable one.

## Risks / Trade-offs

- [**A quote copies source text into the claim file, and scope applies to the claim, not the source**] → This is derived disclosure again, in a new place: a claim scoped `public` quoting a `personal` document publishes that document's words. Issue #15 established the shape of the answer — warn, do not forbid, because no tool can judge what prose reveals — and the same treatment applies here. It should be named explicitly in the spec rather than discovered later, because unlike a synthesis summarising its inputs, a quote is *verbatim* and the exposure is total.
- [Whole-document hashing is noisy] → Accepted, and mitigated by row two of D3 being distinguishable from row three. Noise in the safe direction; the alternative is silence in the unsafe one.
- [Hashing requires fetching, which a validator may not want to do] → Optional by D6, and the drift check is naturally a separate, explicitly-invoked operation rather than part of routine validation.
- [Text normalisation will produce false drift] → Real and unsolved here. Line endings, trailing whitespace, and Unicode normalisation all change a hash without changing meaning. See Open Questions.
- [Adds surface to a format that has just absorbed three rounds] → The test applied throughout this project is whether a process needs the field before it can act. Two do: drift checking needs the hash and quote, harness attribution needs the kind. Contrast the fields this review found that nothing consumes — `weight`, `method`, `role`, `confidence` — which is the failure mode being avoided.

## Open Questions

- **Normalisation before hashing.** A CRLF checkout and an LF checkout of the same file produce different hashes and therefore false drift. Options are to pin a normalisation (strip trailing whitespace, normalise line endings, NFC), to hash the raw bytes and accept the noise, or to say nothing and let it bite. Pinning a normalisation is probably right and is not written here because it deserves its own argument.
- **Algorithm agility.** `sha256:` as a prefixed value allows other algorithms later, but the spec should say whether a consumer may reject an algorithm it does not know, or must treat it as unverifiable.
- **Should the quote be size-bounded?** Nothing stops a quote from being the entire document, at which point the claim file has swallowed its source. A recommendation rather than a limit seems right, but a workspace of unbounded quotes is a real outcome worth naming.
- **Does a synthesis have a document at all?** A synthesis is derived from its inputs, not read from a source, so `source.document` on a synthesis is arguably a category error today and this change makes that more visible rather than less.
