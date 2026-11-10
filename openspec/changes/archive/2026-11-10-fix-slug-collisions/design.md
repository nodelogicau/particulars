## Context

Minting turns a label into a URI by lower-casing, NFKD-folding, stripping combining marks, and collapsing every run outside `[a-z0-9]` to `-`. That makes URIs readable and stable, and it is lossy on purpose. The spec then uses the slug as the identity test: "two labels that slug identically resolve to the same particular". That puts more weight on a lossy function than it can carry:

| labels | slug |
|---|---|
| `C`, `C#`, `C++` | `c` |
| `F`, `F#` | `f` |
| `.NET`, `NET` | `net` |
| `Café`, `Cafe` | `cafe` |

The reference CLI resolves on the minted URI alone and, being idempotent on URI, overwrites the label with the one supplied, keeping the old one as an alias. Defining `C#` after `C` therefore turns `C` into `C#` and reports `created: false`.

The two halves of the original intent are compatible. The slug keeps the URI readable. Something closer to the caller's words has to decide identity.

## Goals / Non-Goals

**Goals:**
- Re-running define with the same label in a later session still finds the same particular.
- A define for a different thing never lands on an existing particular silently.
- One rule that every implementation applies the same way, with no tables and no locale.
- No existing file changes meaning or validity.

**Non-Goals:**
- Changing the slug algorithm or any minted URI.
- Detecting or splitting particulars that are already conflated.
- Fuzzy or similarity matching ("did you mean…").
- A label that slugs to nothing (e.g. `#`, or a label entirely in a non-Latin script). The current text mints a bare `<base-uri>` or `urn:dkf:<id>:` for it. That is a separate defect, worth its own issue.

## Decisions

### D1. Match the label against the existing particular's label and aliases, under Unicode case folding

When the minted URI already names a particular, define resolves to it only when the supplied label equals that particular's `label` or one of its `aliases` under Unicode case folding. Case folding is what recall by query already uses for labels and aliases, so implementations have it to hand and the two features agree on when two labels are the same.

Only the supplied `label` counts, not the supplied `aliases`. `particular_define(label: "C#", aliases: ["C"])` does not match `C`. The label says what is being defined, and letting an alias steer the match would bring back the same conflation one level down.

When the minted URI names a particular through a merge record, the comparison is against the labels and aliases of every particular in that merge class. A merge says those labels are one thing.

*Alternatives:*
- **Compare slugs** (today): the defect.
- **Compare after the slug's own folding (NFKD, strip marks), but keep punctuation:** this makes `Café` and `Cafe` match. It also adds a third notion of "same label" beside case folding and the slug, and it treats a mark as noise when it can distinguish words (`résumé` / `resume`). See D2.
- **Exact string match:** an agent that writes `project x` one session and `Project X` the next would be refused. That is the case the original rule was written for.

### D2. Diacritics differ, so `Cafe` after `Café` is refused

Under D1, `Cafe` and `Café` are different labels, so the second define is refused. The two failure modes are not symmetric. A refusal costs one more call, which can pass the URI or add the alias. A silent conflation costs every claim written afterwards, and nothing reports it. When identity is in doubt, refuse.

### D3. A non-matching collision is refused, naming what it collided with

Nothing is created or changed. The refusal names the existing particular's `id`, `uri` and `label`. It also says what to do: a different thing needs an explicit `uri`, and the same thing can be reached by its URI or id, or its label can be added as an alias. This follows the existing pattern for an ambiguous author name, which is refused with the candidates listed because the caller can pass a URI instead.

*Alternatives:*
- **Disambiguate the slug** (`c`, `c-2`, …): the minted URI would depend on what else the workspace holds. The same label would mint different URIs in different workspaces, and a second define of `C#` would need a label lookup anyway to avoid minting `c-3`. It ends up as D1 plus a counter.
- **Spell punctuation in the slug** (`c-sharp`, `c-plus-plus`): this moves the collision (`C#` and `C sharp`) rather than removing it. It needs a symbol table, and it changes the minted URI of every existing label containing one, which breaks idempotency for existing workspaces.

### D4. A minted-URI define never relabels; supplied aliases are added

When a minted-URI define resolves to an existing particular, its `label` is left alone and any supplied aliases not already present are added. None are removed. Under D1 the supplied label already matches the label or an alias, so a relabel could only change case, or promote an alias to be the label. Neither is worth an implicit write. Keeping the label means repeated defines are no-ops when they add nothing, and an agent's casing can't churn the label.

A rename is a deliberate act and goes through the explicit `uri`. Today the spec doesn't say what a define that resolves through an alias does to the label. This decision settles it.

*Alternative:* replace the aliases with the supplied list. A define that omitted aliases would then delete them, which is a destructive side effect of a call meant to be idempotent.

### D5. An explicit `uri` is unchanged

With a `uri`, the caller has named the particular. Define stays idempotent on it and may rewrite `label` and `aliases`, as the spec says now. This is how two different things that share a slug coexist (`C#` given a Wikidata URI beside the minted `c`), and how a rename is done.

### D6. No format version

Nothing in a file is read differently. The change narrows when one write operation succeeds. Calls that used to succeed by merging two things are now refused, which is a behaviour change for callers, and it goes in Status in the same form as the hash-grammar clarification.

## Risks / Trade-offs

- **[An agent that relied on slug folding gets refusals]** For example, `Project-X` after `Project X`: both slug to `project-x`, and today they resolve to one particular. → The refusal names the existing particular, so the next call is one retry with its URI, or with `Project-X` added as an alias.
- **[Already-conflated particulars stay conflated]** A workspace where `C` was relabelled `C#` has one particular with label `C#` and alias `C`, and the format can't distinguish that from a deliberate alias. → No detection. The fix is the existing one: define the other thing with an explicit `uri` and assert its claims there. Status says that the change prevents new conflation and does not repair old.
- **[Case folding vs. normalisation]** Two labels that differ only in Unicode normal form (precomposed `é` vs `e` + combining acute) don't match under case folding alone. → Refused under D2's reasoning, at the cost of a retry. Matching under NFC plus case folding would avoid it. That is left as an open question rather than adding a second normalisation now.

## Open Questions

- Should D1 compare under NFC + case folding (canonical caseless match) rather than case folding alone? It avoids refusing visually identical labels and doesn't touch diacritics. It would also be worth applying to recall by query's label matching, so it may belong in a separate change that does both.
- Should the refusal carry a stable code (e.g. `slug_collision`) so clients can branch on it? Other refusals in the spec have none.
