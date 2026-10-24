## Context

The `recall-query` baseline (from `recall-query-terms`, #36) splits a query into terms on `White_Space`. It then trims category P from the edges of each term and of the whole query, before case folding. The exact-match rule for `resolution: label | alias` is checked against the untrimmed, folded query: every character outside the occurrence of the label or alias must be category P.

Whitespace falls outside both rules. That doesn't matter for terms, which contain none, but the whole query can carry it (#37). Separately, the ordering keys within `label` and `alias` use the trimmed query, so they can't see a trailing `#` that the exact rule kept.

## Goals / Non-Goals

**Goals:**
- A name with whitespace at its edges, or between it and edge punctuation, resolves exactly.
- Edge whitespace changes nothing: not `resolution`, not the order, not what is marked matched.
- When several particulars are exact for one query, the one naming more of the query comes first.
- Every rule stays computable identically from the files, with no locale or model.

**Non-Goals:**
- Collapsing or normalising interior whitespace. `Project  X` (two spaces) is still not `Project X`.
- Unicode normalisation (NFC/NFKC). It is a separate question and isn't raised by #37.
- Changing the exact rule so that `C` stops being exact for `C#`. See the decisions below.
- Bounding response size or weighting common terms. Those belong to #38, which waits on particulars-bench results.

## Decisions

**Treat `White_Space` like category P at the edges, in both rules.** Removing whitespace only in the trim would fix ordering but not `Project X ?`, where the space sits between the name and the `?`. That case needs the exact rule to accept whitespace outside the occurrence as well. Two alternatives were rejected:
- *Pre-strip whitespace and then apply the current rules.* This is equivalent for leading and trailing whitespace, but still fails `Project X ?`.
- *Define edge characters as "not a letter, mark or number".* That would make symbols such as `+` (Sm) and `$` (Sc) edge characters, so `C++` would trim to `C`, which is the failure #36 avoided by choosing category P.

**Use the `White_Space` property, not category Z.** Terms are already split on `White_Space`, and line feed and tab are category Cc, not Z, yet they are what a client sends at the end of a line of input. Using the same property for the split and the trim keeps one definition of whitespace across the spec.

**Order by the longest exact label or alias first, within `label` and `alias`.** The exact rule can't tell a name's trailing `#` from trailing punctuation without consulting other labels. Changing it to do so would make one particular's `resolution` depend on which other particulars exist. So the rule stays as it is, and `C` is still `label` for the query `C#`. The order then prefers the particular whose label or alias covers more of the query. Length is counted in code points of the folded label or alias, which gives the same answer everywhere.

The key goes first because the keys after it can't break this tie: both labels contain the trimmed query `c`, and both match its single term. One alternative was rejected: comparing against the untrimmed query in the whole-query key. That would bring back the edge sensitivity #37 removes, with `C#?` no longer whole-query-matching `C#`.

**Leave `semantic` alone.** Its order stays implementation-defined, and the new key doesn't apply to it, since a semantic-only particular has no exact occurrence.

## Risks / Trade-offs

- [Some queries move from `lexical` to `label` or `alias`, which changes the order a conforming implementation returns] → This is the intended fix. Only particulars that are exact by the new rule move, and they move ahead of guesses.
- [`C` is still reported `label` for the query `C#`] → A caller reading `resolution` may over-trust it. The order makes sure `C#` is never cut in favour of `C`, and the README says why the rule isn't tightened.
- [Unrelated to this change: the trimmed term `c` matches nearly every object, so `C#` floods `lexical`] → Recorded as input to #38, not fixed here.

## Migration Plan

None for the format. particulars-cli#12 updates `isEdge`, the exact check and the ordering.
