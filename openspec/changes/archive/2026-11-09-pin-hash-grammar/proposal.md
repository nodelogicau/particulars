## Why

`source.document.hash` is specified as `<algorithm>:<digest>` and nothing more. The spec doesn't say whether the digest is hex or base64, which case hex is written in, how algorithm names are spelled, or what a reader does with a value it can't parse. Two conformant implementations can therefore write hashes the other cannot compare. The failure is quiet: under the current text, `sha256:<base64>` or a truncated `sha256:9f2a` is a syntactically acceptable hash that never matches, and is reported as **context drift on every check, forever**. The reference implementation has filled the gap with rules of its own (lowercase hex, 64 digits for `sha256`, a validation failure otherwise) that the spec never states and that contradict "readers SHALL accept any `<algorithm>:<digest>`". Raised as #56.

## What Changes

- **The grammar is pinned to the OCI digest grammar.** A hash is `algorithm ":" encoded`. The algorithm is `[a-z0-9]+([+._-][a-z0-9]+)*` and the encoded part is `[a-zA-Z0-9=_-]+`. Every hash written as the spec's examples show is unchanged.
- **Two algorithms are registered, as in OCI:** `sha256` (64 lowercase hex digits) and `sha512` (128). Writers write `sha256`. Readers implement `sha256` and MAY implement `sha512`. Any other grammatical algorithm is reported as unverified, as now.
- **Writers are strict.** A writer refuses a hash that is not in canonical form: a registered algorithm with the exact digest length in lowercase hex, or an unregistered algorithm matching the grammar.
- **Readers are lenient about form and exact about the value.**
  - Uppercase hex, an algorithm name in another case, and the IANA spellings `sha-256` and `sha-512` are accepted for the registered algorithms and compared by the digest value.
  - Accepting them is reported as `hash_noncanonical`, a fact about the corpus, reported in aggregate.
- **A malformed hash is read as no hash.** A malformed hash is one that doesn't match the grammar, or a registered algorithm with a digest of the wrong length or alphabet. A reader verifies the reference as though the mapping carried no `hash`, by the quote alone where there is one, and reports `hash_malformed` as a finding about the object. It is never reported as drift, and it never fails validation, because the file cannot be rewritten. Redacting `source.document.hash` (`dkf/0.3`) clears it. This mirrors the existing rule for a quote that folds to nothing.
- **No format version.** No file is read differently, and no file that validated stops validating. Some references move from a false *context drift* to *hash unverified*, which corrects a report rather than changing the format.

## Capabilities

### New Capabilities

_None._

### Modified Capabilities
- `source-verification`: *A document reference may be structured* drops "readers SHALL accept any `<algorithm>:<digest>`" and points to two new requirements: *A hash has one grammar and a canonical form* (the OCI grammar, the registered algorithms, writer refusal, reader leniency, `hash_noncanonical`) and *A malformed hash is read as no hash* (verify as if the hash were absent, `hash_malformed`, never drift, never a validation failure).

## Impact

- `README.md`: *Verifiable documents* (the hash paragraphs), *Drift* (a malformed hash is "none"), *Findings and facts* (`hash_malformed`, `hash_noncanonical`), References (OCI image spec), and Status.
- `openspec/specs/source-verification`: one requirement modified, two added.
- `particulars-cli`: it currently **fails validation** on a malformed or uppercase hash, which this change makes conformant only as a warning. It also compares hashes as strings. A follow-up issue will cover reading uppercase and `sha-256` forms, the two condition codes, and keeping the writer refusal it already has.
- Ordering: this change comes from design review (#56), so it is **posted for review before applying**.
