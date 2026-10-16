## Context

`recall-query` defines a model-free lexical baseline so that two conforming implementations, given the same workspace and query, resolve the same particulars. #33 showed that a whitespace-only split leaves punctuation on terms, which hides the most specific term of almost every question. The review on #33 added two gaps. The text never says how terms combine. And `limit`, which applies to particulars, makes the order within a `resolution` value part of the response, even though `recall-vector-cache`'s D3 said stage-one order "never reaches the response".

## Goals / Non-Goals

**Goals:**
- A question's terms match as the words they are.
- Exact names still resolve as `label` / `alias` when a query wraps them in punctuation.
- Two conforming implementations return the same particulars, in the same order, for any query whose candidates are all baseline-resolved.
- The rule needs no tokeniser, locale, stemmer, stopword list or corpus statistic.

**Non-Goals:**
- Stemming, stopwords, possessives (`dog's` still doesn't match "dog").
- Splitting on interior punctuation, which would break the identifiers the baseline guarantees.
- Fixing the order of `semantic` particulars, which depends on a model by definition.

## Decisions

### D1. Trim category P at the edges, of terms and of the whole query

Terms are maximal runs of non-`White_Space` characters. From each term and from the whole query, leading and trailing characters of Unicode general category P (Pc, Pd, Ps, Pe, Pi, Pf, Po) are removed. Interior characters are kept. Trimming is applied to the query as written, then case folding applies as before, so the result doesn't depend on how a folding table treats punctuation.

*Why P and not P plus S.* Category S holds `+`, `$`, `<`, `>`, `|` and backtick. Trimming it would turn `C++` into `C`, and backticks are rare in agent queries next to `?`. P covers the question mark, full stop, comma, quotes, brackets, colon and exclamation mark, which is what #33 found.

*Alternative considered:* strip all non-alphanumerics. Rejected because it breaks `PROJ-1234` and `v1.2.3`.

### D2. Exact match is "only punctuation around it", not "equal after trimming"

The issue proposed comparing the trimmed query with the label. That loses names that end in punctuation: `C#?` trims to `C`, and so does `C#` itself, so the label `C#` is never exact (`Yahoo!`, `Acme Ltd.`, `U.S.` and `__init__` fail the same way). Comparing both as written and trimmed fixes `C#` but still misses `C#?`.

The rule chosen is that the case-folded label or alias occurs in the case-folded query, and every character of the query before and after that occurrence is of category P. This covers `Project X?`, `"Project X"`, `(C#)` and `C#?`. The query `C` does not match `C#`, because `c#` doesn't occur in `c`. It includes the as-written case, where nothing surrounds the occurrence. The query is not otherwise trimmed for this test.

*Alternative considered:* also trim the label, comparing `trim(query) = trim(label)`. Rejected because then the query `C` would exactly match the label `C#`.

### D3. OR, and what "matched" means

A text matches when the trimmed whole query, or any non-empty trimmed term, is a substring of it under case folding. A particular is resolved by the baseline when its label, an alias, or the `content` of one of its claims or syntheses matches. An object is marked matched when its `content` matches.

*Why OR.* AND would make recall depend on every word of a question appearing in one claim, so `what is the session timeout` would resolve nothing. Precision comes from the ordering in D5, not from refusing to resolve.

### D4. An empty query resolves nothing

If the whole query is empty after trimming, every term is too, and nothing is resolved. The response is empty and is not an error. Without this, the empty string is a substring of everything, and `?` resolves the whole workspace.

### D5. A fixed order within `label`, `alias` and `lexical`

Particulars are ordered by `resolution` (`label`, `alias`, `lexical`, `semantic`). Within each of the first three values:

1. Particulars where the trimmed whole query matches come first.
2. Then particulars matching more distinct trimmed terms. Terms are deduplicated after case folding, and a term counts if it matches the label, an alias, or the `content` of an object in that particular's response.
3. Then ascending id of the particular. For a merge class, that is the lowest id in the class.

`limit` keeps the first particulars in this order. Within `semantic` the order is implementation-defined.

*Why count over the response, not every object.* Stage two has already applied scope, author and retraction. Counting a retracted or out-of-scope claim would let an object the caller can't see decide what the caller does see.

*Why this and not BM25.* It needs no corpus statistic, every implementation computes it identically, and it already ranks `auth timeout` above `the`. Implementations that want better ranking have the semantic stage.

This corrects `recall-vector-cache` D3, which said stage-one ordering never reaches the response. That design stays in the archive as the record of what was believed.

## Risks / Trade-offs

- [Common words still match nearly everything] → They now rank last within `lexical` under D5, and `limit` cuts them. Stopword lists stay out because they are language-specific.
- [Ordering requires knowing each particular's response before truncating] → Stage two already computes it. The cost is one count per resolved particular, bounded by the candidate set.
- [A name followed by `'s` is not exact (`Project X's`)] → Accepted. The apostrophe and `s` aren't both category P, so it resolves as `lexical`, as the issue's *Not proposed* section agrees.
- [Implementations with a conforming whitespace baseline change results] → Intended. They match more and order deterministically. Nothing in a workspace changes.

## Migration Plan

None for workspaces. particulars-cli#12 adopts the rule before it ships.

## Open Questions

None.
