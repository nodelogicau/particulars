## 1. Identifiers and examples (#1)

- [x] 1.1 Add an "Identifiers" subsection under Core Object Types: `<prefix>_<uuidv7>` format, prefixes `par|clm|syn|mrg`, monotonic minting, lenient read regex, minting-time vs `timestamp`
- [x] 1.2 Regenerate every example id in README.md as a valid lowercase UUIDv7 with the right prefix, consistently across particular/claim/synthesis/index examples
- [x] 1.3 Update the Status section: ID format is no longer "subject to change"

## 2. Source and context on objects (#9, #10.1, #10.2)

- [x] 2.1 Add a "Source" subsection defining the shared `source` shape, the "at least one of `author`/`harness`" rule, and that agent-only sources are valid
- [x] 2.2 Replace `produced-by` with `source` (including `harness`) in the DSYNTHESIS example and the Object Model diagram; note `produced-by` as a readable legacy alias for v0.1
- [x] 2.3 Rename `synthesis_create(..., produced_by)` to `synthesis_create(..., source)` in the MCP tool table
- [x] 2.4 State that `context` and `context.scope` are required on disk, `topics` optional, defaults applied by writers only; update the `claim_assert` row to say the default is applied at write time
- [x] 2.5 Update "Harness attribution" under Trust and Provenance to reference `source.harness`

## 3. Synthesis rules (#10.3, #10.4)

- [x] 3.1 State that inputs may have a different `subject` than the synthesis, with a pointer to the conflict-semantics caveat
- [x] 3.2 Document `unresolved: None identified` as the conventional empty value; reject absent/null/empty

## 4. Retraction (#2, #3)

- [x] 4.1 Add a "Retraction" subsection after DSYNTHESIS with the `retracted` block example, the only-permitted-modification rule, never-removed rule, reinstatement-by-new-object rule, and applicability to claims, syntheses, and merges
- [x] 4.2 Document optional `superseded-by`, its must-exist validation, and that it is not synthesis
- [x] 4.3 Under "Cryptographic signing", define the signed payload as the object minus `retracted` and `signature`
- [x] 4.4 Update the `claim_retract` row to reference the `retracted` block

## 5. URIs and workspace config (#4, #5)

- [x] 5.1 Change the DPARTICULAR `uri` comment and prose to "globally unique; resolvable once published"; keep the preference for Wikidata/ORCID/etc.
- [x] 5.2 Add the minting convention (`<base-uri><slug>` / `urn:dkf:<workspace-id>:<slug>`), the slug algorithm, the one-sentence claim of `urn:dkf:`, and the published-URI immutability rule
- [x] 5.3 Add `dkf.yaml` to the File Layout with the example, required keys, discovery-by-walking-up, writer-only defaults, and ignore-unknown-keys
- [x] 5.4 Update the `particular_define` row to note URI minting when `uri` is omitted

## 6. Index (#6)

- [x] 6.1 Rewrite the index paragraph: derived and regenerable, files are the source of truth, must not cause wrong local results when missing/stale, stays committed for HTTP consumers
- [x] 6.2 Extend the `index.yaml` example with `scope`, `topics`, `timestamp`, `retracted: true`, and a merge entry with `uris`; state that extra fields are allowed and unknown ones ignored
- [x] 6.3 Mention rebuild and drift-check operations as expected implementation behaviour

## 7. Merge records (#7)

- [x] 7.1 Add `/merges/mrg_….yaml` to the File Layout and a "Merge records" subsection with the example, field rules (exactly two `uris`, `source`, `timestamp`, optional `reason`), and no-rewrite guarantee
- [x] 7.2 Define equivalence-class semantics (symmetric, transitive, non-retracted only) for `knowledge_recall`, `conflict_detect`, and `lineage_trace`
- [x] 7.3 Update the `particular_merge` row to reference the record; add `/knowledge/merges/` as an optional feed in the `.well-known` example
- [x] 7.4 Reword the "Minimal spec, layered implementation" principle to "three knowledge objects plus two records (retraction, merge)"

## 8. Conflict semantics (#8)

- [x] 8.1 Add a "Conflict semantics" subsection (under Object Model or Query Tools) defining `current`, `unsynthesised`, `stale`, the reporting rule, and priority `|unsynthesised| + |stale|`
- [x] 8.2 Redefine "the current belief about any particular" in terms of `current`, with later claims surfaced as unsynthesised
- [x] 8.3 State the retraction cascade (stale, not mutated), that `superseded-by` is not synthesis, and that cross-particular inputs do not synthesise the other particular
- [x] 8.4 Update the `conflict_detect` row to say it returns structural sets and leaves contradiction judgement to the harness

## 9. Review and close out

- [x] 9.1 Read README.md end-to-end for consistency: every example id, field name, and tool signature agrees with the new rules; no dangling reference to `produced-by` except the legacy note
- [x] 9.2 Verify each spec scenario in `openspec/changes/address-reference-impl-feedback/specs/` is answered by a normative sentence in README.md
- [x] 9.3 Update the Status section to reflect which details are now fixed and what remains open (signing, `.well-known` crawling)
- [ ] 9.4 Commit with a message referencing #1–#10; after merge, comment on each issue with the resolving section and close it
