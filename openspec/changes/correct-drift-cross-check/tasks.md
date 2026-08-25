## 1. The cross-check

- [ ] 1.1 Replace the cross-check paragraph in README.md: implementations report the observed drift state alongside the declared `kind` as fact, and an unchanged hash is not evidence against a declared `supersession`
- [ ] 1.2 State why — drift is a signal about the source joint, supersession asserts the world moved, and the format cannot distinguish a living document from a dated one
- [ ] 1.3 Add the sound inverse: `defect` declared against a drifted document is unverifiable, because the misread text is no longer readable

## 2. The reference

- [ ] 2.1 Rename `uri` to `ref` in the `document` mapping example and its field list
- [ ] 2.2 State that `ref` holds a URI or a path resolved against the workspace root, and why relative paths must be expressible
- [ ] 2.3 Change the example to a repository-relative path, so the pattern that gets copied is the one that is cheap to verify

## 3. The hash

- [ ] 3.1 Define the hash as taken over the document with CRLF normalised to LF and nothing else altered
- [ ] 3.2 State the reasoning — normalise the transport artefact, leave every edit visible — and name what is deliberately not normalised
- [ ] 3.3 Remove text normalisation from the open items in Status, since it now has an answer

## 4. Review and close out

- [ ] 4.1 Verify each scenario in `specs/` is answered by a normative sentence in README.md
- [ ] 4.2 Confirm the MODIFIED header matches its baseline, and that the retraction rename is applied before its modification at archive time
- [ ] 4.3 Check no surviving reference to `document.uri` or to the supersession cross-check anywhere in README.md or the baseline specs
- [ ] 4.4 Post the proposal on particulars-cli#3 **before** applying, and give them a chance to respond — the ordering the previous round got wrong
- [ ] 4.5 After applying, note on the issue that `ref` and the LF rule are settled, so their first mapping is written against the final shape
