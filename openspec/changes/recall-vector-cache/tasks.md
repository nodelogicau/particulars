## 1. README: recall by query

- [x] 1.1 In *Query Tools*, revise the `knowledge_recall` row: a `query` is resolved to particulars and then recalled exactly as by particular; each result carries `resolution` (`label`, `alias`, `lexical`, `semantic`)
- [x] 1.2 Add a *Recall by query* subsection after *Federation Tools* and before *What the server tells the model*: the two stages and why stage one returns no objects (D1, D2); the lexical baseline and why it always runs (D3); the `resolution` order and how `limit` respects it
- [x] 1.3 In the same subsection, state the semantic cache rules: what is embedded, outside the workspace tree, never committed or published, model-tagged, not read by validators, incremental by id; and that a stale cache loses recall but never returns a wrong object (D4)
- [x] 1.4 In the same subsection, state the remote-embedding rule: explicit configuration only, a scope ceiling defaulting to `public` computed on effective scope, configuration not in `dkf.yaml`, and why it belongs to the machine rather than the workspace (D5)
- [x] 1.5 In the `particular_resolve` row, add that it never uses a semantic stage and returns null rather than a nearest candidate

## 2. README: index and principles

- [x] 2.1 In *`index.yaml`*, where implementations may add entry fields, add the exclusion: no embedding vectors or model-dependent values, because the index is committed, crawled, and compared across implementations (D6)
- [x] 2.2 In *Design Principles*, extend *Files over databases*: a vector store, like a database, is an optimisation that finds a subject, never one that says what is true about it

## 3. Delta specs

- [x] 3.1 Confirm `specs/recall-query/spec.md` introduces no term the README does not define once 1.x lands (`resolution`, effective scope, merge equivalence class, lineage order)
- [x] 3.2 Confirm the MODIFIED `index-manifest` block is the baseline requirement verbatim plus the exclusion sentence and the *No embeddings in the index* scenario, and nothing else
- [x] 3.3 Run `openspec validate recall-vector-cache --strict` and fix anything it reports

## 4. Close out

- [x] 4.1 Verify each scenario in both delta specs is answered by a normative sentence in README.md
- [x] 4.2 In particulars-cli, find what `recall --query` does today; open an issue for the baseline (labels, aliases, content; case folding; whole query and terms) and the `resolution` marker, and a separate, optional issue for a semantic cache under the user cache directory keyed by `workspace.id` — done 2026-10-14: the CLI treats `query` as a synonym for `particular_id` (exact label/alias via `resolveOne`, no content matching); opened particulars-cli#12 (baseline, two stages, `resolution`) and #13 (optional semantic cache)
- [x] 4.3 Record in particulars-knowledge: `query` on `knowledge_recall` was unspecified from the first draft; the gap surfaced from comparing DKF with a RAG vector store; the decision is that similarity resolves subjects and structure answers — recorded 2026-10-14 in particulars-knowledge#41 on branch knowledge/recall-query as clm_01a1399c-a889-7d81-91be-5e2fef020bd0 (the gap) and clm_01a1399c-a8b9-7543-88cf-9cd4181a4324 (the decision)
