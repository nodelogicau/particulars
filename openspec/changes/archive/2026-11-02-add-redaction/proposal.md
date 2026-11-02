## Why

The format can say that a claim is wrong, but it has no way to say that a claim's text should no longer be readable. Retraction keeps the content on purpose: "Retraction is recorded, not deletion." That is right for correcting mistakes. It is wrong for a true claim that should never have been written down, such as a third party's medical detail, or for a quote that discloses too much of a private source. Today the only remedy is to edit an immutable file by hand, which the format forbids and validation cannot see. As particulars is considered as the memory store for an assistant, "forget that" has to be something a conformant implementation can do.

This change is about hiding and hygiene, not legal erasure. It defines what redaction does to the **current object**, and nothing more. Who may read earlier versions is left to the implementation. A git workspace keeps them, and a database-backed implementation can restrict access to them. YAML diffs stay readable. Nothing is encrypted.

## What Changes

- **A `redacted` block, separate from `retracted`.** Retraction answers "is it true?" and redaction answers "should it be readable?". The two are independent: a true claim can be redacted, a wrong one can stay readable, and an object can carry both blocks. Redaction is not a retraction `kind`, because `kind` drives harness reliability and a redaction is no evidence against the process that produced the claim.
- **Redaction removes the listed fields and records what it removed.** The block carries `timestamp`, `reason`, `source`, and `fields`. The fields that may be redacted are `content`, a synthesis's `unresolved`, the document's `ref`, `quote` and `hash`, and a retraction's `reason`. None of these is mirrored in the index. Fields the index mirrors (`subject`, `scope`, `topics`, `timestamp`, `author`, `document-author`) cannot be redacted, so no sealed segment ever changes.
- **Redacting `content` withdraws the object.** A withdrawn object is excluded wherever a retracted one is: it leaves recall, cannot be `current`, and makes everything citing it `stale`. Redacting only evidence (`quote`, `ref`, `hash`) leaves the claim live and makes its evidence unverifiable.
- **Redaction is irreversible and never inferred.** The content is gone, so there is no un-redact; reinstatement is a new claim. Nothing redacts implicitly.
- **No cascade, but candidates are reported.** Syntheses whose own `content` may restate a redacted input, inferred claims whose basis was redacted, and the `superseded-by` successor are not modified. They are reported as `restates_redacted`, so a person can decide whether to redact them too.
- **An index `redacted` list.** Like `retracted`, it is keyed by the month of the redaction and lives in the root and in sealed segments. It holds the ids of withdrawn objects only. Evidence-only redactions change nothing the index mirrors.
- **Signatures:** the signed payload excludes `redacted` as it excludes `retracted`. A signature over a redacted field can no longer verify, and this is reported as a fact rather than an error.
- **The semantic cache drops vectors of redacted text,** because an embedding can disclose what it was computed from.
- **What redaction does not promise is stated:** earlier versions in version control, clones, caches, crawlers and anything already fetched are untouched. A git implementation says so when it redacts.
- **A `knowledge_redact` tool and a `particulars redact` command.**
- **BREAKING:** a workspace that contains a redaction is `format: dkf/0.3`. A `dkf/0.2` reader would see a claim with no `content` and either reject it or recall an empty belief. The workspace-config rule that a reader refuses a format it does not implement turns that into a clean refusal. Migrating from `dkf/0.2` rewrites only `format`. A writer refuses to redact in an older workspace until it is migrated.

Out of scope: particulars (labels, aliases, minted URIs), merge and promotion `reason` fields, `topics`, `document.author`, erasure from history, and encryption.

## Capabilities

### New Capabilities
- `redaction`: the `redacted` block, the redactable fields, withdrawal and evidence-only redaction, irreversibility, the `restates_redacted` finding, the withdrawn-equals-retracted rule for recall, conflict sets and author relations, drift and validation parity for the index list, what redaction does not guarantee, and the tool surface.

### Modified Capabilities
- `retraction`: adding a `retracted` block is no longer the *only* permitted modification to an object file. Redaction is the second, and it may remove a retraction's `reason` while the block itself remains.
- `index-manifest`: the root and sealed segments carry a `redacted` list beside `retracted`, keyed by the redaction's month, and a segment's shape is `format`, `entries`, `retracted`, `redacted`.
- `canonical-serialisation`: the signed payload excludes `redacted`, and a redacted signed object's signature is unverifiable rather than invalid.
- `recall-query`: the semantic cache must drop embeddings of redacted fields and must never consult them.
- `workspace-config`: `dkf/0.3` is a valid `format`, naming the sharded layout with redaction.

## Impact

- `README.md`: a new *Redaction* section after *Retraction*. Edits to Retraction ("only permitted modification"), Conflict semantics (withdrawn), `index.yaml` (the `redacted` list), Trust and Provenance (the signed payload, and `restates_redacted` among the findings), Recall by query (the cache), the MCP tool table (twelve tools), Migration (`dkf/0.2` → `dkf/0.3`), Design Principles ("Provenance is non-negotiable" and "nothing is deleted" restated precisely), and Status.
- `particulars-cli`: implementation, plus the skill and `dkf.md` guidance on when to redact rather than retract. To be filed as an issue.
- `particulars-knowledge`: record the decision.
- Existing workspaces: nothing changes until someone first redacts, which requires migration to `dkf/0.3`.
