## 1. The document, in the README

- [x] 1.1 Add `dkf.md` to the File Layout tree, marked optional, beside `dkf.yaml`
- [x] 1.2 Add `conventions:` to the `dkf.yaml` example with a comment (optional; relative path inside the workspace; default `dkf.md`)
- [x] 1.3 Add a `### dkf.md` subsection after `dkf.yaml`: what it is for and what it is not (prose for agents; nothing reads it but a model; cannot relax the spec); the default and the key; the lexical path rule and unset-with-warning; the steer that structurally modelled facts — authors, topics — belong in the format, not the prose; `AGENTS.md` as a legitimate value for a workspace that is its own agent scope; keep it short, it rides in every session

## 2. Delivery and register, in the MCP section

- [x] 2.1 Add a paragraph to MCP Server Tools: a server bound to a workspace with a conventions document SHOULD append it to its `initialize` instructions after its generic guidance under a heading naming the file, its discipline prompt carries the same text, it MAY expose the file as a resource; unreadable is a warning; the 16 KiB floor, character-boundary cut, and truncation note
- [x] 2.2 Reword the `claim_assert` row: content states a fact about the world; what was read goes in `source.document`; the subject is never the document or feed it was read in
- [x] 2.3 Reword the `particular_define` row: a particular is a thing in the world, not a document being read; global-URI examples are identities (a person's ORCID, a project's page)

## 3. Close out

- [x] 3.1 Verify each scenario in `specs/` is answered by a normative sentence in README.md
- [x] 3.2 Confirm the `workspace-config` MODIFIED block copies its baseline text in full
- [ ] 3.3 Comment on and close #23: accepted; filename `dkf.md` and why; invalid path lenient and why; floor not ceiling; register in the tool table; resource MAY
- [ ] 3.4 Add to `particulars-cli#7`: default renamed to `dkf.md`; invalid `workspace.conventions` warns instead of failing config validation; truncate on a character boundary; optional resource; README's stale "`.dkf` is an implementation extension"
- [ ] 3.5 Record in particulars-knowledge
