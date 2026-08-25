## 1. The cross-check

- [x] 1.1 Replace the cross-check paragraph in README.md: implementations report the observed drift state alongside the declared `kind` as fact, and an unchanged hash is not evidence against a declared `supersession`
- [x] 1.2 State why — drift is a signal about the source joint, supersession asserts the world moved, and the format cannot distinguish a living document from a dated one
- [x] 1.3 Add the sound inverse: `defect` declared against a drifted document is unverifiable, because the misread text is no longer readable

## 2. The reference

- [x] 2.1 Rename `uri` to `ref` in the `document` mapping example and its field list
- [x] 2.2 State that `ref` holds a URI, a workspace-relative path, or an identifier for a source that cannot be fetched, and that resolution is best-effort
- [x] 2.3 State that readers accept `uri` as a legacy alias and warn, because a file carrying it can never be rewritten
- [x] 2.4 Change the example to a repository-relative path, so the pattern that gets copied is the one that is cheap to verify

## 3. The hash

- [x] 3.1 Define the hash as taken over the document with CRLF normalised to LF and nothing else altered
- [x] 3.2 State the reasoning — normalise the transport artefact, leave every edit visible — and name what is deliberately not normalised
- [x] 3.3 State that writers should write sha256 and readers accept any algorithm, reporting an unknown one as unverified
- [x] 3.4 Remove text normalisation from the open items in Status, since it now has an answer
- [x] 3.5 State that checking covers retracted objects, since the unverifiable-defect finding is about the retraction

## 4. Review and close out

- [x] 4.1 Verify each scenario in `specs/` is answered by a normative sentence in README.md
- [x] 4.2 Confirm the MODIFIED header matches its baseline, and that the retraction rename is applied before its modification at archive time
- [x] 4.3 Check no surviving reference to `document.uri` or to the supersession cross-check anywhere in README.md or the baseline specs
- [x] 4.4 Post the proposal on particulars-cli#3 **before** applying, and give them a chance to respond — the ordering the previous round got wrong
- [ ] 4.5 After applying, note on the issue that `ref` and the LF rule are settled, so their first mapping is written against the final shape
