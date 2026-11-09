## 1. Review

- [x] 1.1 Post the proposal for review before applying (design-review origin, #56); fold in feedback, especially the D4 choice of a warning over the CLI's current validation failure — reviewed by the maintainer, who applied with D4 as proposed

## 2. README — Verifiable documents

- [x] 2.1 Replace "Writers should write `sha256`. Readers accept any `<algorithm>:<digest>`…" with the grammar, the two registered algorithms and their lengths, and canonical form; keep the reason unknown algorithms are unverified rather than invalid
- [x] 2.2 State writer refusal of non-canonical and malformed hashes, naming the canonical form, never normalising
- [x] 2.3 State reader leniency (hex case, algorithm case, `sha-256`/`sha-512`, a closed list), comparison by value, and `hash_noncanonical` in aggregate
- [x] 2.4 State the malformed rule: read as no hash, verified by quote alone, `hash_malformed` per object, never drift, never a validation failure, cleared by redacting the hash; cite the empty-quote precedent
- [x] 2.5 Mark the elided example digests (`sha256:9f2a…`) as elided, so that they don't read as truncated hashes

## 3. README — Drift, findings, references, status

- [x] 3.1 In *Drift*, say that a malformed hash takes the table's "none" rows
- [x] 3.2 In *Findings and facts*, add `hash_malformed` to findings about an object and `hash_noncanonical` to facts about the corpus
- [x] 3.3 Add the OCI image-spec descriptor digest grammar to References, under "Standards borrowed as grammars"
- [x] 3.4 Add a Status entry: a clarification, no format version, no file newly invalid, false context drift corrected (#56)

## 4. Verify and follow up

- [x] 4.1 Run `openspec validate pin-hash-grammar --strict` and fix any findings
- [x] 4.2 Check that no README or `openspec/specs/*` text still says readers accept any `<algorithm>:<digest>`
- [x] 4.3 Open a `particulars-cli` issue: read uppercase and `sha-256` forms and compare by value, downgrade a malformed hash from `invalid_document` to a `hash_malformed` warning, add `hash_noncanonical`, keep the writer refusal — nodelogicau/particulars-cli#31
