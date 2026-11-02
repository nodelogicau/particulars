## 1. Resolve the open questions

- [x] 1.1 Confirm or revise design Open Questions 1–3 (one block vs a list; how `restates_redacted` clears; whether content redaction requires prior retraction), and update the `redaction` spec if any answer changes

## 2. The Redaction section

- [x] 2.1 Add a *Redaction* section to README.md after *Retraction*. Include an example file carrying both `retracted` and `redacted`, the block's fields and canonical position, and the closed set of redactable paths with why it is closed. Cover the bare-string and mapping `document` rules, and one block with a union of `fields`.
- [x] 2.2 State why redaction is not a retraction `kind`: the two questions are orthogonal, and `kind` feeds reliability.
- [x] 2.3 Define **withdrawn** (retracted or content-redacted). State that evidence-only redaction leaves an object live, and that `unresolved`-only redaction leaves a synthesis eligible to be `current`.
- [x] 2.4 State irreversibility and that nothing redacts implicitly, and that the reason must not restate what was removed.
- [x] 2.5 Add `restates_redacted`: who is a candidate, no cascade, per-object reporting, and when it clears.
- [x] 2.6 State what redaction does not remove: history, clones, crawlers and fetched copies. Add the git output requirement and the note that a store controlling history MAY restrict it.

## 3. Edits elsewhere in README.md

- [x] 3.1 *Retraction*: "only permitted modification" becomes one of two. A redacted `reason` leaves the block standing.
- [x] 3.2 *Conflict semantics*: replace "non-retracted" and "a retracted object" with "withdrawn" in the three set definitions, and add a sentence that redaction, like retraction, does not cascade by mutation.
- [x] 3.3 *`index.yaml`*: add the `redacted` list to the root and segment examples and to the prose. Keyed by redaction month, content redactions only. Explain why entries never change. Extend the filtering bound and drift/validation parity.
- [x] 3.4 *Verifiable documents* / *Drift*: a redacted quote or ref yields an unverifiable result, never drift, and an unverifiable `defect`.
- [x] 3.5 *Trust and Provenance*: the signed payload also excludes `redacted`. Add `signature_redacted` as a corpus fact and `restates_redacted` as an object finding.
- [x] 3.6 *Recall by query*: the semantic cache never consults, and deletes, embeddings of redacted fields.
- [x] 3.7 *MCP Server Tools*: add `knowledge_redact(object_id, fields[], reason, source)`, change "eleven" to "twelve", and make `knowledge_recall`'s `include_retracted` say it also covers redacted objects.
- [x] 3.8 *`dkf.yaml`* / *Migration*: add `dkf/0.3`. Migration from `dkf/0.2` rewrites `format` only, and `dkf/0.1` goes through `dkf/0.2`. Writers refuse to redact before `dkf/0.3`.
- [x] 3.9 *Design Principles* and *Unbounded History*: restate "nothing is overwritten" and "nothing is deleted" precisely. Two kinds of modification exist, both recorded in the file, and redaction removes text but never an object, an id, or a place in the graph.
- [x] 3.10 *Status*: record redaction as the change that introduced `dkf/0.3`, and why it is breaking.

## 4. Close out

- [x] 4.1 Verify that each scenario in `specs/` is answered by a normative sentence in README.md
- [x] 4.2 Confirm that every MODIFIED block copies its baseline requirement in full
- [x] 4.3 Run `openspec validate add-redaction --strict`
- [x] 4.4 Filed as nodelogicau/particulars-cli#23: a `particulars-cli` issue for the implementation: `migrate --to dkf/0.3`, `redact`, the index lists, `restates_redacted`, `signature_redacted`, the cache deletion, git-history warning, and skill/`dkf.md` guidance on redact vs retract
- [x] 4.5 Record the decision in `particulars-knowledge`: four claims on DKF (branch `record-redaction-design`). The synthesis, which qualifies clm_01a021ab-17bd ("only permitted modification"), waits until this change merges, because that claim stays true on `main` until then
