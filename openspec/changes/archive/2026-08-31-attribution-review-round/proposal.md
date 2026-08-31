## Why

`source-as-particular` was reviewed against the reference implementation before it could be built (`particulars-cli#7`), and the review held the design sound — D1, D3, D4, D6, D7 stand — while finding five things wrong with the text: one misclassification the spec's own criterion catches, one missing argument, one place the governing constraint was named and then not applied, one label that cannot hold what it is asked to hold, and one compatibility gap the change opens in the index. They are filed as #17–#21. Implementation waits on #17 and #19, which decide what gets written and reported, so this round is what unblocks the CLI.

## What Changes

- **Both author conditions are corpus facts, reported in aggregate** (#17). `author_ambiguous` was classified as a per-object finding; by the *Findings and facts* criterion — is there an action *at the object*? — it is not, any more than an unresolved author is. Both clear at the workspace, at no object. The ambiguity line names the candidates, which the aggregate rule already permits because they are identical across the group. The criterion's sentence "cannot be cleared without rewriting an immutable file" is widened to "cannot be cleared at any object", since these two can be cleared, just not there.
- **D2 gains the freeze argument** (#18). Writing the resolved URI freezes a resolution that was unambiguous at write time; a bare name left in the file becomes ambiguous retroactively when a second particular takes the alias, and an immutable claim stays that way. An id would freeze it too, but only inside the workspace. Text only; no requirement changes.
- **The writer rule is made strict where the constraint promised it** (#19). A writer SHALL refuse an author given as an id that resolves to nothing, and SHALL refuse an *explicitly given* name that matches more than one particular, listing the candidates. A default author — `defaults.source.author` or its environment equivalent — that matches zero or several particulars is written unchanged, because failing there would block every write in the workspace. A URI that resolves to no local particular is written unchanged and is not an error: it is the correct cross-workspace identity of someone not defined here.
- **The recall label is a set** (#20). One object can be both asserted by and reported from the same class; `relations: [asserted, reported]`, never a single value.
- **A drift check tolerates the absence of MAY fields** (#21). A newer implementation that writes `author` and `document-author` into entries must not fail every index committed before the field existed. A field present on both sides with different values is still drift; a field the committed index could not have known is not.
- **A person's particular is defined deliberately.** Implementations SHALL NOT mint one as a side effect of `init` or of writing a claim; the review showed a URN-minted author is opaque where a name was readable, with no cross-workspace gain. This answers the design's open question and lands as a requirement.

Nothing is **BREAKING**; every item narrows what a writer accepts or widens what a reader tolerates.

## Capabilities

### New Capabilities
<!-- none -->

### Modified Capabilities
- `source-attribution`: the writer rule gains its refusal cases and the unresolved-URI case; `author_ambiguous` becomes an aggregate fact; the recall label becomes a set; a new requirement that person particulars are never minted automatically.
- `condition-reporting`: the corpus-fact definition says "cannot be cleared at any object" and admits facts that a workspace-level action clears.
- `index-manifest`: the drift check does not report the absence of MAY fields in the committed index.

## Impact

- `README.md` — *Source* (writer-rule paragraph: strictness table and the freeze sentence; the ambiguity paragraph: both aggregate), *`DPARTICULAR`* (no automatic minting), *Findings and facts* (one sentence), *`index.yaml`* (drift tolerance), the `knowledge_recall` tool row (`relations`).
- **Closes #17, #18, #19, #20, #21** and unblocks `particulars-cli#7`, whose recommendation this adopts in full plus the unresolved-URI case and the minting rule.
- `particulars-cli` — nothing beyond what #7 already lists, with the classification and the writer refusals now settled; `author_ambiguous` and `author_unresolved` both go on the aggregation whitelist, and the drift check gains a MAY-field allowance instead of a CHANGELOG warning.
