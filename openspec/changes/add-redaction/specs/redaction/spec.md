## ADDED Requirements

### Requirement: Redaction is a block on the object file that lists what it removed
A redaction SHALL be represented by removing one or more fields from a claim's or synthesis's YAML file and adding a `redacted` block to that file, with fields `timestamp` (required), `reason` (required), `source` (required, see `source-provenance`), and `fields` (required, a non-empty list of the paths removed). Every path in `fields` SHALL be absent from the file. A field that the specification otherwise requires SHALL be valid when absent if and only if `fields` lists it. Redaction SHALL be independent of retraction: an object MAY carry `redacted`, `retracted`, both, or neither, and redaction SHALL NOT be expressed as a retraction `kind`. In canonical order, `redacted` SHALL follow `retracted`. Merge records, promotion records and particulars SHALL NOT carry a `redacted` block.

#### Scenario: Redacting a claim's content
- **WHEN** `knowledge_redact(clm_X, fields: [content], reason, source)` is called
- **THEN** `content` is absent from `clm_X`'s file, a `redacted` block with `timestamp`, `reason`, `source` and `fields: [content]` is present, and no other field changes

#### Scenario: A required field missing without a redaction
- **WHEN** a claim file lacks `content` and carries no `redacted` block listing it
- **THEN** validation fails as it always has

#### Scenario: Redacted and retracted
- **WHEN** a retracted claim is later redacted
- **THEN** the file carries both blocks, `retracted` first, and the retraction's `kind` is unchanged

#### Scenario: A merge record
- **WHEN** an implementation is asked to redact a merge or promotion record or a particular
- **THEN** it refuses

### Requirement: Only fields the index does not mirror are redactable
`fields` SHALL contain only paths from this set: `content`, `unresolved` (syntheses only), `source.document.ref`, `source.document.quote`, `source.document.hash`, and `retracted.reason`. A path outside the set SHALL be refused by writers and SHALL fail validation. `subject`, `context`, `timestamp`, `source.author`, `source.document.author` and every field mirrored by the index SHALL NOT be redactable, so that redaction never changes an index entry. When `source.document` is a bare string, it is its `ref`, and redacting `source.document.ref` SHALL remove `source.document` entirely. When it is a mapping, the members not listed SHALL remain.

#### Scenario: Redacting a quote
- **WHEN** a claim's `source.document` is a mapping with `ref`, `author`, `hash` and `quote`, and `source.document.quote` is redacted
- **THEN** `ref`, `author` and `hash` remain and `quote` is absent

#### Scenario: Redacting a bare-string document
- **WHEN** a claim's `source.document` is the string `https://example.com/notes` and `source.document.ref` is redacted
- **THEN** the claim carries no `source.document`

#### Scenario: An index-mirrored field
- **WHEN** a writer is asked to redact `context.topics` or `source.document.author`
- **THEN** it refuses and names the field as not redactable

#### Scenario: A retraction reason that restates the claim
- **WHEN** a retracted claim's `content` and `retracted.reason` are both redacted
- **THEN** the `retracted` block remains with `timestamp`, `source`, and any `kind` and `superseded-by`, and has no `reason`

### Requirement: Redacting content withdraws the object
A claim or synthesis whose `redacted.fields` includes `content` SHALL be **withdrawn**. A retracted object SHALL also be withdrawn. Wherever this specification excludes retracted claims or syntheses, it SHALL exclude every withdrawn object, including from `current`, `unsynthesised`, recall with `include_retracted: false`, and the asserted-by and reported-from relations. Wherever it treats citing a retracted object as making the citer `stale`, citing a withdrawn object SHALL do the same. A redaction that does not include `content` SHALL leave the object live.

#### Scenario: A redacted synthesis is not current
- **WHEN** the most recent synthesis about a particular has its `content` redacted
- **THEN** `current` is the most recent synthesis that is not withdrawn, or absent

#### Scenario: Citers go stale
- **WHEN** `syn_1` cites `clm_1` and `clm_1`'s `content` is redacted
- **THEN** `syn_1` is in `stale` and its file is unchanged

#### Scenario: Evidence-only redaction
- **WHEN** only `source.document.quote` is redacted from `clm_1`
- **THEN** `clm_1` is returned by recall, can be unsynthesised or synthesised as before, and makes nothing stale

#### Scenario: Including withdrawn objects
- **WHEN** recall is called with `include_retracted: true` over a content-redacted claim
- **THEN** the claim is returned with its `redacted` block and without `content`

#### Scenario: Synthesis unresolved only
- **WHEN** only a synthesis's `unresolved` is redacted
- **THEN** the synthesis remains eligible to be `current`

### Requirement: Evidence-only redaction makes the evidence unverifiable
When `source.document.ref`, `source.document.quote` or `source.document.hash` is redacted, verification SHALL proceed with what remains. Where what remains cannot establish drift, the claim SHALL be reported as unverifiable, never as drifted. A retraction declaring `kind: defect` against an object whose quote or ref is redacted SHALL be reported as unverifiable, as for a drifted source.

#### Scenario: Quote redacted, hash kept
- **WHEN** a claim's `quote` is redacted and its `ref` and `hash` remain
- **THEN** drift is determined by the hash alone

#### Scenario: Ref redacted
- **WHEN** a claim's `source.document.ref` is redacted
- **THEN** its source is unverifiable and no drift is reported

### Requirement: Redaction is irreversible and never inferred
The `redacted` block SHALL NOT be removed, and a redacted field SHALL NOT be restored to the file. Reinstatement SHALL be a new claim or synthesis. A file SHALL carry at most one `redacted` block. A further redaction of the same object SHALL replace the block's `timestamp`, `reason` and `source` and SHALL set `fields` to the union of the old and new paths. No operation other than an explicit redaction SHALL redact. In particular, retraction, promotion, merge and synthesis never redact.

#### Scenario: Attempting to restore
- **WHEN** an implementation is asked to restore a redacted field
- **THEN** it refuses and directs the caller to assert a new claim

#### Scenario: A second redaction
- **WHEN** `clm_X` has `fields: [source.document.quote]` and `content` is then redacted
- **THEN** the file carries one `redacted` block with `fields: [content, source.document.quote]` and the newer `timestamp`, `reason` and `source`

### Requirement: Redaction does not cascade, and objects that may restate it are reported
Redacting an object SHALL NOT modify any other object. When an object's `content` is redacted, an implementation SHALL report as `restates_redacted` each object that is not withdrawn and that cites it through `inputs` or `basis`, or that is the target of its `retracted.superseded-by`, because the candidate's own text may repeat what was removed. `restates_redacted` is a finding about an object and SHALL be reported per object, naming the redacted object. It SHALL cease to be reported when the candidate is withdrawn. Implementations SHALL NOT judge whether the candidate's text in fact restates the redacted content.

#### Scenario: A synthesis citing a redacted claim
- **WHEN** `syn_1` cites `clm_1` and `clm_1`'s `content` is redacted
- **THEN** `syn_1` is reported as `restates_redacted` naming `clm_1`, and is also `stale`

#### Scenario: A supersession successor
- **WHEN** `clm_1` is retracted with `superseded-by: clm_2` and `clm_1`'s `content` is then redacted
- **THEN** `clm_2` is reported as `restates_redacted`

#### Scenario: Clearing the finding
- **WHEN** `syn_1`'s own `content` is then redacted
- **THEN** `syn_1` is no longer reported as `restates_redacted`

### Requirement: Index drift and validation treat `redacted` as they treat `retracted`
In a `dkf/0.3` index, the drift check SHALL compare the `redacted` lists of the root and of each differing segment exactly as it compares `retracted` lists, and validation SHALL regenerate each sealed month's `redacted` list from the files and report a difference naming the object and the segment. A redaction whose `timestamp` falls in a sealed month SHALL be a validation failure. Only withdrawn-by-redaction ids, those whose `fields` include `content`, SHALL appear in `redacted`. Where a later redaction adds `content`, the id SHALL be listed under the month of the block's current `timestamp`.

#### Scenario: A redaction after the index was committed
- **WHEN** a claim's `content` is redacted and the committed root does not list it under `redacted`
- **THEN** the drift check reports it

#### Scenario: Evidence-only redaction and the index
- **WHEN** only a claim's `quote` is redacted
- **THEN** no index document changes

### Requirement: Redaction states what it does not remove
The specification SHALL state that redaction removes text from the object's current file and from what a conformant implementation reads, recalls, serves and embeds, and that it makes no claim about earlier versions held by version control, clones, caches, crawlers, or consumers that already fetched the object. An implementation whose store is a git repository SHALL say, in the output of a redaction, that the removed text remains in the repository's history. An implementation whose store controls access to prior versions MAY restrict that access. The redaction `reason` SHOULD NOT restate what was removed, and the specification SHALL say so.

#### Scenario: Redacting in a git workspace
- **WHEN** `particulars redact clm_X --field content --reason …` runs in a git-backed workspace
- **THEN** the output states that the removed text remains in git history

#### Scenario: A public object already crawled
- **WHEN** a public claim is redacted after a crawler fetched it
- **THEN** the served file is the redacted one, and the specification makes no claim about the crawler's copy

### Requirement: Redaction is exposed as a tool and requires `dkf/0.3`
A reference MCP server SHALL expose `knowledge_redact(object_id, fields[], reason, source)`, which writes a redaction as defined here and refuses any path outside the redactable set. A writer SHALL refuse to redact in a workspace whose `format` is earlier than `dkf/0.3`, and SHALL name the migration. Migrating a `dkf/0.2` workspace to `dkf/0.3` SHALL rewrite only `format` in `dkf.yaml`. No object moves and no payload changes.

#### Scenario: Redacting in a `dkf/0.2` workspace
- **WHEN** `knowledge_redact` is called in a workspace with `format: dkf/0.2`
- **THEN** it refuses, writes nothing, and names the migration to `dkf/0.3`

#### Scenario: Migration preserves signatures
- **WHEN** a `dkf/0.2` workspace is migrated to `dkf/0.3`
- **THEN** only `dkf.yaml` changes, and every signature that verified before verifies after
