## 1. Author as a particular reference

- [x] 1.1 In the `Source` section of README.md, state the three forms `author` may take — particular id, URI, bare name — and that readers resolve them by id, by `uri` through merges, and by label or alias respectively
- [x] 1.2 State that a value resolving to no particular is an opaque name that satisfies the source minimum and is reported as unresolved, never invalid
- [x] 1.3 State the writer rule: a defined particular is written as its `uri`, not its id; a bare name resolving to exactly one particular is written as that `uri`; on zero or several matches the name is written unchanged — and note this covers `defaults.source.author`
- [x] 1.4 Explain the asymmetry with `subject` in one paragraph: an author is the one particular that recurs across workspaces, so it carries the cross-workspace identifier
- [x] 1.5 State that `harness` and `model` remain strings, and why
- [x] 1.6 Add a paragraph to `DPARTICULAR` on people and agents as particulars: prefer a global URI (ORCID, DID, GitHub) for a person, and a person's particular carries the URI they are willing to be cited under at the widest scope their claims may reach

## 2. Who produced what was read

- [x] 2.1 Add `author` to the `Verifiable documents` mapping example, after `ref`, and update the field-order sentence to `ref`, `author`, `hash`, `quote`
- [x] 2.2 Define `document.author` as who produced what was read, distinct from `source.author` (who read it), in the same reference forms
- [x] 2.3 State why this is not a fourth evidential: testimony is `observed`, the utterance is the document, and the field that was missing names its producer
- [x] 2.4 Note that `ref` remains required and that an unrecorded utterance uses the existing unfetchable-`ref` form

## 3. The two relations

- [x] 3.1 Define **asserted by** and **reported from**, both computed over merge equivalence classes, and state that implementations never collapse them
- [x] 3.2 Extend the `Merge records` section: the class also governs attribution, and `source` values are never rewritten by a merge
- [x] 3.3 Update the `knowledge_recall` row in the tool table with the `author` parameter, its accepted forms, and the `asserted` / `reported` labelling
- [x] 3.4 Update the `particular_resolve` row: ambiguity is reported with candidates, never resolved by choice

## 4. Resolution and reporting

- [x] 4.1 State that a bare name matching more than one particular resolves to none of them
- [x] 4.2 Name `author_ambiguous` as a per-object finding and an unresolved author as an aggregate fact, consistent with the `Findings and facts` paragraph in Trust and Provenance
- [x] 4.3 Add `author` and `document-author` to the `index.yaml` example and to the "Entries MAY also carry" sentence

## 5. Trust and Provenance

- [x] 5.1 Retitle **Harness attribution** to **Asserter attribution**: `defect` counts against the asserting particular and the harness; `provenance-failure` against the cited document and its resolved `document.author`; `supersession` against nothing
- [x] 5.2 Add one sentence to **Cryptographic signing**: the identity a signature would naturally bind is the author particular's URI, with suites still reserved
- [x] 5.3 Add the disclosure statement beside the quote-disclosure text: promotion publishes the author URI; `document.author` discloses who is being quoted as completely as `quote` discloses what was said; particular files are not served, so the URI is the whole exposure

## 6. Consistency and close-out

- [x] 6.1 Re-read the `Object Model` diagram and the `Minimal spec, layered implementation` principle; add "source: who asserted it — a particular" only if the diagram's `← source` line needs it
- [x] 6.2 Verify every scenario in `specs/` is answered by a normative sentence in README.md
- [x] 6.3 Confirm no delta modifies a requirement that does not exist in the baseline (the four MODIFIED blocks copy their baseline text in full)
- [x] 6.4 Update Status: this is the first post-v0.1 change, additive, and the deferrals it touches without taking — DID binding, promotion by particular, synthesis `document`
- [x] 6.5 Raised as particulars-cli#7. Asked for: `--author` accepting id/URI/name with write-time URI resolution, `--document-author`, `recall --author`, the two index fields, `author_ambiguous`, and the skill instruction that who-told-you goes in `--document-author`
- [ ] 6.6 Record the decision in the dogfood workspace once applied, citing the deferral claims from PR #29 as inputs
