## 1. Reporting (#17)

- [x] 1.1 In the *Source* ambiguity paragraph of README.md, make both author conditions corpus facts: `author_ambiguous` and `author_unresolved`, each reported in aggregate, the ambiguity line carrying the candidates
- [x] 1.2 In *Findings and facts*, replace "it can never be cleared, because clearing it would mean rewriting an immutable file" with the "cannot be cleared at any object" form and its two reasons, and add the author conditions to the list of examples

## 2. The freeze argument (#18)

- [x] 2.1 Add the freeze sentence to the writer-rule paragraph in *Source*: writing the resolved URI freezes a resolution that was unambiguous at write time; a bare name becomes ambiguous retroactively, and an immutable claim stays so
- [x] 2.2 Say in the same paragraph that this is what answers "why write anything, names resolve at read time", and that it composes with the cross-workspace argument

## 3. Writer strictness (#19)

- [x] 3.1 Rewrite the writer-rule sentence in *Source* as the full table in prose: unknown id refused; URI written unchanged whether or not defined locally; explicit ambiguous name refused with candidates; default ambiguous name written unchanged
- [x] 3.2 State why defaults fall through and explicit names do not, and that a URI this workspace has not defined is the right identity, not an error

## 4. Relations (#20)

- [x] 4.1 Update the `knowledge_recall` tool row: results carry `relations`, a set of `asserted` and/or `reported`, never empty
- [x] 4.2 Add the both-relations case to the *Source* two-relations paragraph in one sentence

## 5. Index drift (#21)

- [x] 5.1 In the `index.yaml` section, state that a drift check does not report the absence of a MAY field from the committed index, and does report a MAY field present on both sides with different values

## 6. Deliberate person particulars

- [x] 6.1 In the `DPARTICULAR` people-and-agents paragraph, state that implementations never mint a person's particular as a side effect of `init` or of writing, and why a URN-minted author is worse than a name

## 7. Close out

- [x] 7.1 Verify every scenario in `specs/` is answered by a normative sentence in README.md
- [x] 7.2 Confirm the three MODIFIED blocks copy their baseline text in full
- [ ] 7.3 Comment on #17–#21 with the resolution and close them when the change is archived
- [ ] 7.4 Comment on `particulars-cli#7`: classification and refusals settled, `relations` a set, drift allowance instead of a CHANGELOG note, no minting in `init`; the skill line about when to pass `--author`
- [ ] 7.5 Record the round in the dogfood workspace
