## Why

`recall-query-terms` trims Unicode general category P from the edges of the whole query, but not whitespace (#37). So a name with a space or newline beside it loses its exact match: `Project X ?` (French typography), ` Project X`, `Project X\n`. A trailing space also changes the whole-query ordering key. Implementations that strip whitespace first, as most input handling does, return a different `resolution` and a different order from those that follow the text literally, and both believe they conform.

Reviewing #37 turned up a second gap in the same rule. The exact rule allows punctuation on both sides of the occurrence, so a label `C` is exact for the query `C#`. The ordering keys then use the trimmed query, which for `C#` is `c`. That makes labels `C` and `C#` tie on every key, and particular id decides which one `limit` keeps.

## What Changes

- Leading and trailing characters with the Unicode `White_Space` property are removed from the whole query alongside category P. Terms can't carry whitespace, so for them nothing changes. Interior whitespace stays significant.
- In the exact-match rule, a character outside the label or alias occurrence may be category P or `White_Space`.
- A query of whitespace alone is empty after removal, and so resolves nothing without an error, like `?!`.
- Within `label` and `alias`, particulars are ordered first by the length of the longest label or alias that makes them exact, longer first. The whole-query, term-count and id keys follow as before.
- New scenarios:
  - whitespace beside a name;
  - a line of input with leading and trailing whitespace;
  - edge whitespace not changing the order;
  - the `C`/`C#` order;
  - a whitespace-only query;
  - a punctuation-only label not being resolved by a punctuation-only query.
- README *Recall by query* updated to match.

## Capabilities

### New Capabilities

None.

### Modified Capabilities

- `recall-query`:
  - *A lexical baseline is required and always runs*: whitespace is trimmed from the edges of the whole query.
  - *Each result says how it was resolved*: whitespace is allowed around an exact occurrence; longest exact label or alias first within `label` and `alias`.

## Impact

- README.md *Recall by query*: the baseline and `resolution` paragraphs.
- `openspec/specs/recall-query/spec.md`: two requirements.
- particulars-cli#12. The baseline in `234a9cd` trims only `unicode.IsPunct` (`internal/query/recall_query.go:55`) and has no longest-exact key. Both need updating to conform.
- Not a breaking change for conforming clients. Some queries that resolved as `lexical` now resolve as `label` or `alias`, and the order within `label` and `alias` changes only where several exact particulars tie.
