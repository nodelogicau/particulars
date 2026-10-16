## Why

`recall-query`'s baseline splits a query on whitespace and nothing else, so a term keeps whatever punctuation touches it. Agents send questions, and questions end in `?`. For `what is the session timeout?` the distinguishing term is `timeout?`, which matches no claim that says "timeout". The whole-query comparison fails the same way, so `Project X?` never resolves as `label` and can be cut by `limit` to make room for a guess. Another stage can't repair this honestly, because `resolution` has no value for a particular found by a trimmed second pass (#33).

Reviewing #33 exposed two further gaps that came in with `recall-vector-cache`. First, the spec never says whether terms combine with AND or OR. "Matching both the whole query and each whitespace-separated term" can be read as requiring all of them, and under that reading one punctuated term makes the claim not resolve at all. Second, the design said stage-one order never reaches the response. That's false: `limit` truncates particulars, and with OR, common words resolve nearly everything as `lexical`. Order within `lexical` therefore decides what survives, and the spec leaves it open, so two conforming servers return different particulars for the same query. The baseline exists to make them agree.

## What Changes

- **Edge punctuation is trimmed.** Each whitespace-separated term, and the whole query, lose their leading and trailing characters of Unicode general category P before matching. Interior characters are kept, so `PROJ-1234`, `v1.2.3`, `o'brien` and `auth/session` match as written. A term that is empty after trimming is ignored. A query that is empty after trimming resolves nothing, and that is not an error.
- **An exact match can be wrapped in punctuation.** A particular is resolved as `label` or `alias` when its label or alias, under case folding, occurs in the query with only category P characters before and after it. `Project X?` and `"Project X"` match label `Project X`. `C#?` matches label `C#`, which trimming alone would reduce to `C`. `C` does not match `C#`.
- **Terms combine by OR.** A text matches when the trimmed whole query or any trimmed term is a substring of it. An object whose `content` matches this way is marked as matched.
- **Order within a resolution value is fixed.** Particulars are ordered by `resolution`. Within `label`, `alias` and `lexical`, those whose text contains the trimmed whole query come first, then those matching more distinct trimmed terms, then ascending particular id. Within `semantic` the order is implementation-defined. `limit` keeps the first particulars in this order.

Not **BREAKING** for workspaces: no file or field changes. A baseline that already conforms will now match more queries, and its order within `lexical` becomes fixed.

## Capabilities

### New Capabilities

None.

### Modified Capabilities

- `recall-query`: *A lexical baseline is required and always runs* gains edge trimming, the empty-query rule and OR. *Each result says how it was resolved* gains the punctuation-tolerant exact match and the fixed order within each value. *Recall by query resolves to particulars, then recalls structurally* says what "matched" means.

## Impact

- `README.md`, *Recall by query*: *The baseline* and *`resolution`* paragraphs restate the term rule, OR, the empty query and the order. The sentence saying implementations may rank as they like inside stage one, if one appears, is corrected.
- `particulars-cli`: fold this into #12 before it lands. Comment there with the rule and the new scenarios.
- Archive: `recall-vector-cache`'s `design.md` keeps its D3 as written. It is the record of what was believed. This change's design records the correction.
- Dogfood: a claim in particulars-knowledge that the baseline's term rule, its combination rule and its order were all unstated in `recall-vector-cache`, found by an issue raised from the reference implementation within two days.
