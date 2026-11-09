## Context

The hash on a structured document reference is one half of drift checking. The other half is the quote. The hash says whether anything changed and the quote says whether the words are still there, and the drift table reads meaning from their disagreement. The table is only as good as the two implementations' agreement about what a hash *is*. Today they agree on nothing below `<algorithm>:<digest>`.

The reference CLI, `particulars-cli` `internal/dkf/document.go`:
- validates hashes against `^[a-z0-9][a-z0-9-]*:[0-9a-f]+$` and fails validation (`invalid_document`) on anything else;
- also fails a `sha256` digest that is not 64 characters;
- compares a stored hash with a computed one as strings;
- computes `sha256` with lowercase hex.

Those choices are sensible, but they are the implementation's, not the format's. A second implementation following the spec's text could write `sha256:9F2A…` and have every one of its claims fail the reference validator.

## Goals / Non-Goals

**Goals:** one grammar every implementation parses alike. A canonical form writers emit. A defined reading of every value a file might hold, including the wrong ones. No existing file becoming invalid.

**Non-Goals:**
- Changing *what* is hashed (CRLF→LF and nothing else stays).
- New algorithms (BLAKE3, SHA-3).
- Multihash, or SRI-style base64.
- RFC 9530 Digest Fields, a consumer-side fetch optimisation that belongs with #55.
- Hashing anything other than `source.document`.

## Decisions

### D1. Adopt the OCI digest grammar rather than invent one

`algorithm ":" encoded`, with
- `algorithm := component (separator component)*`, `component := [a-z0-9]+`, `separator := [+._-]`
- `encoded := [a-zA-Z0-9=_-]+`

This is the OCI image-spec descriptor digest grammar. It already has the `sha256:` shape, so every hash the spec's examples imply is valid under it unchanged. It is the most widely deployed `algo:digest` grammar in use, with parsers in every language that handles container images, so a DKF implementer has one to hand. It also has a registered-algorithm table, which gives a place to say "64 lowercase hex" without the format maintaining its own registry.

*Alternatives:*
- **Multihash:** a binary-prefix encoding that is unreadable in a diff, and it would change every existing value.
- **SRI (`sha256-<base64>`):** a different separator and encoding, so every existing value would change.
- **The IANA hash names (`sha-256`):** these name algorithms but define no `name:digest` grammar, and the hyphen would make `sha-256` and `sha256` compete. Readers accept the IANA spellings (D3); writers don't use them.
- **Write our own:** the problem is precisely that each implementation wrote its own.

### D2. Two registered algorithms; everything else is opaque and unverified

`sha256` (64 hex) and `sha512` (128 hex), lowercase in canonical form, as OCI registers them. Readers must implement `sha256`, the only algorithm writers write. `sha512` is registered so its digest shape can be checked, which catches truncation, not so that every reader computes it. An algorithm outside the table that matches the grammar keeps today's treatment: legitimate, opaque, reported as unverified, never invalid. Its `encoded` part is not interpreted.

### D3. Readers fold form, compare value, and say so in aggregate

For the registered algorithms, a reader accepts:
- hex in either case;
- an algorithm name in any case;
- the IANA spellings `sha-256` and `sha-512`.

It then compares the decoded digest, which in practice means lowercasing both and comparing strings.

**Why lenient:** under the current text every one of these forms is valid, since "readers SHALL accept any `<algorithm>:<digest>`". A file holding one cannot be rewritten, and the format's rule is that tightening a writer never invalidates an existing file. **Why say so:** a non-canonical form is evidence of a writer that didn't follow this text. It carries no action at any object, because the hash is right, so it is a corpus fact, `hash_noncanonical`, reported in aggregate like the legacy `uri` alias.

The alias set is closed: two IANA spellings, not a fuzzy rule. `SHA_256` and `sha2-256` are not recognised. They match the grammar, so they are unregistered algorithms and reported as unverified. A closed list is where implementations cannot part.

### D4. A malformed hash is read as no hash, as an empty quote is read as no quote

A value is **malformed** when:
- it doesn't match the grammar, e.g. `9f2a…` with no prefix, or `sha256:` with nothing after it; or
- it names a registered algorithm (after D3 folding) with a digest of the wrong length or with non-hex characters, e.g. a truncated `sha256:9f2a` or `sha256:<base64>`.

A reader verifies the reference as though the mapping carried no `hash`: by the quote alone where there is one, as the table's "none" rows say. A malformed hash with no quote leaves the reference unverified. The reader reports `hash_malformed` against the object.

**Why not drift:** the value never named the document. Under today's text a truncated digest reports context drift on every run, a false alarm that never clears. That is the "check that cries wolf" the quote rule was designed to avoid.

**Why not a validation failure (what the CLI does today):** the file is immutable, so a failure could never be satisfied by fixing it, and the current text made these values valid. This is the empty-quote precedent exactly: writers refuse, readers treat the field as absent, and a warning is the only way anyone learns it is there.

**Why a finding about the object rather than a corpus fact:** unlike `hash_noncanonical`, it is actionable at the object. In a `dkf/0.3` workspace, redacting `source.document.hash` removes it, and the redaction rules already say a redacted hash is verified as absent and never reported as drift. In a `dkf/0.2` workspace it is a finding that cannot yet be cleared, which is still the right category: the action exists, behind a migration the workspace can choose.

*Alternative:* keep the CLI's failure. Rejected because it makes a file that followed the spec invalid, and because the CLI's own empty-quote handling already chose the other way for the same reason.

### D5. Writers refuse, and say what canonical form is

A writer refuses a hash that is malformed (D4), and refuses a registered-algorithm hash that is not in canonical form, rather than silently normalising it. Normalising would accept `SHA-256:9F2A…` from a caller who thinks they wrote something else, and would hide that the caller's tool emits non-canonical hashes. The refusal names the canonical form. A writer that *computes* the hash itself, as `particulars-cli` does when given a local `ref`, already writes canonical form.

### D6. No format version

No file is read differently in the sense `format` exists to capture: no field disappears, nothing new appears, and an older reader meeting a newer workspace misreads nothing. Older readers simply report a malformed hash as drift and an uppercase hash as context drift, which this change corrects. No file that validated stops validating, and no file is newly required to change. This is a clarification, recorded in Status like the v0.2 erratum, and it binds writers from the day it lands.

## Risks / Trade-offs

- [Another implementation already writes base64 under `sha256:`] → None is known. If one exists, its hashes become `hash_malformed` warnings with the claims intact and verifiable by quote. Before this change they were silent false drift.
- [Leniency for uppercase hex lets a non-conformant writer persist unnoticed] → `hash_noncanonical` is reported on every run, in aggregate, and writers refuse the form.
- [The CLI loosens from failure to warning on malformed hashes] → Intended. The follow-up issue covers it, and the CLI's write-side refusal is kept.
- [OCI may register further algorithms] → DKF's registered set is stated in its own text and changes only by a DKF change. The grammar is borrowed; the table is not delegated.

## Migration Plan

None for workspaces. Implementations update their parser, their comparison and their two condition codes. Rollback is reverting the README text.

## Open Questions

- Should `hash_malformed` on a `dkf/0.2` workspace say that redaction requires migrating to `dkf/0.3`? Probably as message text, which is not normative.
