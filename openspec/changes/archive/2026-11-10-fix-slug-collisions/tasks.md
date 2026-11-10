## 1. Review

- [x] 1.1 Post the proposal on #62 for review before applying; settle the design's open questions (canonical caseless match vs case folding, a refusal code), and confirm D2 (diacritics refused) and D4 (no relabel; aliases added, never removed) — the maintainer applied with D2 and D4 as proposed; the two open questions stay open

## 2. README — Particulars and minting

- [x] 2.1 In *Particulars*, qualify "`particular_define`, being idempotent on URI, may rewrite its `label` and `aliases`": that holds for an explicit `uri`; a minted-URI define never relabels, and only adds aliases
- [x] 2.2 In *Minting URIs*, replace "two labels that slug identically resolve to the same particular" with the label-keyed rule: match on label or alias under Unicode case folding, across the merge class; supplied aliases don't count
- [x] 2.3 State the refusal: nothing written; names the existing `id`, `uri` and `label`; says to pass an explicit `uri` for a different thing, or use the URI or id for the same one. Give the `C` / `C#` example and why the slug can't decide identity
- [x] 2.4 Say why `Café` and `Cafe` are refused (a refusal costs one call; a silent conflation costs every later claim), and that disambiguating or spelling out punctuation in the slug were rejected

## 3. README — Tools and status

- [x] 3.1 Update the `particular_define` row in *MCP Server Tools*: idempotent on an explicit URI; without one, resolves only on a label or alias match, refuses otherwise, never relabels
- [x] 3.2 Add a Status entry: a clarification, no format version, no file reads differently or stops validating; define calls that silently merged two things are now refused; existing conflations aren't repaired (#62)

## 4. Verify and follow up

- [x] 4.1 Run `openspec validate fix-slug-collisions --strict` and fix any findings
- [x] 4.2 Check that no README or `openspec/specs/*` text still says labels that slug identically resolve to one particular
- [x] 4.3 Comment on nodelogicau/particulars-cli#32 with the rule: label/alias match under case folding, refusal naming the existing particular, no relabel without an explicit `uri`, aliases added only — commented on particulars-cli#32
- [x] 4.4 Open an issue for a label that slugs to nothing (e.g. `#`, or an all-CJK label), which currently mints a bare `<base-uri>` or `urn:dkf:<id>:` — #63
