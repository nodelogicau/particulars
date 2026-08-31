# Dialectical Knowledge Format (DKF)

An open format for portable, interoperable knowledge — designed to work across
AI harnesses, applications, and the public internet.

**[particulars.fyi](https://particulars.fyi)** — a visual introduction for
practitioners.

---

## The Problem

AI assistants are increasingly how people capture, organise, and reason over
knowledge. But every harness — Claude, ChatGPT, Gemini, and others — stores
what it learns in a proprietary silo. Knowledge shared with one is invisible to
another. There is no equivalent of `.ics` for calendar data: no open, portable
format that any application can publish, consume, and reason over.

Existing memory frameworks solve parts of this — persistence within a harness,
cross-session recall, vector search — but none address the deeper problem: that
knowledge evolves through contradiction, and current formats treat contradiction
as an error to eliminate rather than signal to preserve.

---

## The Approach

DKF draws on the structure of Hegelian dialectic: a **thesis** is confronted by
an **antithesis**, and their reconciliation produces a **synthesis** — a richer
claim that carries the reasoning that produced it. That synthesis becomes the
new thesis, available to be contradicted and refined again.

This makes contradiction a first-class citizen of the format. Rather than
silently overwriting a stale fact, DKF records what was believed, what
challenged it, how it was resolved, and what remains unresolved. Any harness
consuming the result inherits not just the conclusion but the reasoning chain.

The approach is analogous to what OpenSpec does for code: rather than storing
the current state of knowledge, DKF records the process by which knowledge
was formed — making it portable, inspectable, and trustworthy across systems.

---

## Core Object Types

The format defines three knowledge object types — particular, claim, and
synthesis — and records that describe events about them: retraction, merge,
and publish. Everything else is implementation.

### Identifiers

Every object and record id is `<prefix>_` followed by a lowercase canonical
UUID version 7 ([RFC 9562](https://www.rfc-editor.org/rfc/rfc9562)):

| Prefix | Type |
|---|---|
| `par_` | particular |
| `clm_` | claim |
| `syn_` | synthesis |
| `mrg_` | merge record |
| `pub_` | promotion record |

```
clm_01916f03-b680-71a3-974f-9401ba374e1f
```

UUIDv7 is time-ordered, so `ls claims/` is a chronological log and new files
cluster at the end of a diff. Implementations MUST mint with a monotonic
counter so that ids created within the same millisecond still sort in creation
order.

The time embedded in an id is the **minting** instant. The `timestamp` field on
an object is the **assertion** time and may be earlier — for example when
recording a dated document. Consumers MUST NOT require the two to agree.

Readers MUST accept any id matching `^(par|clm|syn|mrg|pub)_[A-Za-z0-9-]+$`, so
that workspaces written with other schemes (including earlier drafts of this
specification) remain readable. Validators MAY warn on ids that are not
UUIDv7.

### Field order

The order in which fields are shown for each type below is that type's
**canonical order**. Writers SHOULD emit fields in it; readers MUST accept
them in any order and MUST NOT reject a file because its fields are arranged
differently. Fields an implementation adds beyond this specification are
written after all specified fields, keeping their relative order among
themselves.

Canonical order is what makes a workspace reviewable as a git diff: two
implementations that agree on it produce byte-identical files for identical
knowledge. That is its whole justification — the [document
hash](#verifiable-documents) covers bytes, but the reserved signature never
did; it is defined over the data model, where file layout is invisible. See
[Trust and Provenance](#trust-and-provenance).

### Source

Claims, syntheses, retractions, merge records, and promotion records all
carry a `source` block of the same shape:

```yaml
source:
  author: ben                 # a person — an id, URI, or name; see below
  harness: claude             # the AI harness, if one was involved
  model: claude-sonnet-4-6    # the model, if known
  document: https://…         # what was read to make the assertion
```

All four fields are optional individually, but a `source` MUST contain at
least one of `author` or `harness`. An agent acting with no human in the loop
is a valid source (`{harness, model}`); a person working without an assistant
is a valid source (`{author}`). A `source` with neither is malformed.
Syntheses additionally require `source.harness` — see below.

**`author` is a reference to a particular**, and may take three forms: a
particular id, a particular URI, or a bare name. Readers resolve an id by
exact match, a URI by the particular's `uri` — including through merge
records — and a bare name by label or alias. A value that resolves to no
particular is an opaque name: it satisfies the minimum above exactly as it
always has, and is reported as *unresolved*, never invalid. Resolution
happens when a file is read, which is what lets an existing workspace become
attributable without a file changing: the moment a particular with alias
`ben` is defined, every claim carrying `author: ben` is asserted by it.

Writers prefer the URI, and are strict where they can be. When the author
is a defined particular, a writer writes its `uri` rather than its `par_`
id. An id that names no particular is refused — nobody is *called*
`par_01a0…`, so it is a typo, as an unknown subject is. A URI is written
unchanged whether or not a local particular carries it: an ORCID this
workspace has never defined is the right identity of someone defined
elsewhere, not an error. A bare name that resolves to exactly one particular
is written as that particular's `uri`, and one that resolves to none is
written unchanged, since a person not yet defined is legitimate. A bare
name that resolves to *several* splits on who supplied it: given explicitly
by the caller, it is refused with the candidates listed, exactly as subject
resolution refuses, because the caller can pass a URI instead; taken from
`defaults.source.author` or its equivalent, it is written unchanged and
reported in aggregate, because failing there would block every write in the
workspace until someone edits an alias, and a write is not where that should
be discovered.

Why write anything at all, when names resolve at read time? Because writing
the resolved URI **freezes a resolution that was unambiguous at write
time**. Define a second particular with alias `ben` next year and a claim
written as `author: https://github.com/benfortuna` is still Ben's; a claim
that kept the bare name is ambiguous from that day on, and being immutable
it stays so until an alias is removed or a merge is written. Read-time
resolution is for reaching back; write-time freezing is what stops the same
mechanism degrading under later definitions. An id would freeze it too, but
only inside the workspace — which is where the second argument takes over.

This is the one place the format prefers a URI over an id, and the
asymmetry with `subject` is deliberate. A subject is a
workspace-local anchor whose file travels with the workspace, so a local id
is the right key. An author is the one particular that recurs across
workspaces: the same person has a different `par_` id in every workspace
they write in and the same URI in all of them, and a `source` block is the
part of a claim most likely to be read outside its workspace — it is what a
signature would identify. So it carries the identifier that survives the
trip. A URI is also what merge records join, which makes a URN in one
workspace and an ORCID in another the same asserter the moment a merge says
so.

`harness` and `model` remain strings. A harness is a process rather than an
individual, and the attribution that matters for it — see [Trust and
Provenance](#trust-and-provenance) — already works on the string.

Two relations follow, and they are never collapsed. An object is **asserted
by** the particular its `source.author` resolves to, and **reported from**
the particular its `source.document.author` resolves to (see [Verifiable
documents](#verifiable-documents)). Both are computed over the merge
equivalence class of the resolved particular. "Everything Jane said" is the
union, but the halves mean different things about Jane: a defect in a claim
she asserted is her misreading; a defect in a claim reported from her is the
recorder's, and a provenance failure in one is hers. One object can stand in
both relations — Ben recording his own earlier remark — and is then reported
as both, never as one.

A bare name that matches more than one particular resolves to **none of
them**. Resolution never guesses: `particular_resolve` reports ambiguity
with the candidates rather than choosing. A validator reports both author
conditions as facts about the corpus, in aggregate: `author_ambiguous` with
its count and the candidates — which are a property of the name, not the
object, so the aggregate line can carry them — and `author_unresolved` with
its count. Neither is reported per object, because the action that clears
each — an alias or a merge, or defining the particular — is at the workspace
and clears every occurrence at once (see [Findings and
facts](#trust-and-provenance)).

#### Verifiable documents

`document` may be a bare URI, as above, or a mapping that makes the claim
checkable:

```yaml
source:
  author: ben
  harness: claude
  document:
    ref: docs/architecture.md   # URI, workspace path, or an unfetchable source
    author: urn:dkf:01a0…:jane  # who produced what was read — optional
    hash: sha256:9f2a…          # optional
    quote: |                    # verbatim, optional
      The billing service listens on port 8443 behind the ingress.
```

Both forms are valid and a bare string is not inferior provenance. `ref` is
required in the mapping form; `author`, `hash` and `quote` are optional, and
the fields are written in the order shown.

**`ref` identifies the source**, and holds one of three things: a URI, a path
resolved against the workspace root, or an identifier for something that
cannot be fetched at all — `chat session 2026-08-22`, a recollection, a page
behind a login. Resolution is best-effort: an implementation may try a `ref`
as a URI and as a workspace path, and where it is neither the reference is
simply *unverifiable*. That third case is not a courtesy. An unfetchable
source can still carry a quote, and quoting what someone said, with nothing
to fetch and no hash, is provenance a reviewer can weigh. A field called
`uri` could not hold it.

Readers accept `uri` as a legacy alias for `ref` and should warn. The warning
matters for a reason particular to this format rather than out of tidiness: a
file carrying `uri` can never be rewritten, since appending a retraction is
the only permitted modification, so readers must go on accepting it and a
warning is the only way anyone learns it is there.

**`author` names who produced what was read.** It is a particular reference
in the same three forms as `source.author` — id, URI, or bare name — and it
answers a different question: `source.author` is who read the document and
made the claim; `document.author` is who made the document. "Jane said the
split happened in Q2", recorded by Ben, is a claim asserted by Ben whose
document is Jane's utterance and whose document author is Jane. This is why
the format has no *reportative* evidential, though languages that mark
evidentiality grammatically always have one: testimony is `observed` —
someone looked, and what they looked at is the utterance — and what was
missing was not a fourth value but a field naming the utterance's producer.
An unrecorded utterance needs nothing new: `ref` stays required and already
holds an unfetchable source, so `ref: conversation with Jane, 2026-08-30`
with an `author` and a `quote` is a complete, unverifiable, reported claim.
An unresolvable `document.author` is reported as unresolved, never invalid.

**The hash** is taken over the document with CRLF sequences normalised to LF
and *nothing else* altered — not trailing whitespace, not Unicode form, not a
final newline. The rule is to normalise what is an artefact of the transport
and leave every edit visible: line endings differ by platform, so hashing raw
bytes would report drift on every claim in a workspace checked out on
Windows, while trailing whitespace differs because somebody edited the file,
and normalising it would blind the check to a class of real change.

Writers should write `sha256`. Readers accept any `<algorithm>:<digest>` and
report an algorithm they do not implement as unverified rather than invalid —
otherwise two conformant implementations could be unable to check each
other's hashes, which defeats the point of recording one.

**The locator is a verbatim quote, never an offset.** Line and byte ranges
break the moment anyone inserts text above them, which would report drift for
edits that touched nothing relevant — and a check that cries wolf is a check
reviewers learn to skip. A quote is content-addressed, so it survives
insertion and reformatting, and it does something no offset can: it lets a
reviewer audit the claim against its source while reading the pull request,
with no tooling and no network.

#### Drift

A structured reference can be checked later, and two signals matter rather
than one: whether the quote still appears in the document, and whether the
document still hashes the same.

| quote | document hash | meaning |
|---|---|---|
| present | matches | nothing moved; the claim rests where it was |
| present | differs | **context drift** — the text around the quote changed |
| absent | differs | **quote drift** — the cited text is gone or altered |

The middle row is why hashing the quote alone is not enough. A document
reading "In staging, the billing service listens on 443" yields the claim
"the billing service listens on 443"; changing *staging* to *production*
falsifies the claim without touching a character of the quote. Hashing only
the document catches it, at the cost of flagging every unrelated typo — so
recording both is what separates "something moved near my claim" from
"something moved somewhere in this file".

Drift is a condition for a reader to resolve, never a validation failure. A
claim whose source has drifted stays valid, readable, and citable.

**Verification is best-effort.** Nothing obliges a consumer to fetch
anything. A source that cannot be fetched, hashed, or quoted — a
conversation, a recollection, a page behind a login — is a legitimate source,
and such provenance is reported as *unverified* rather than absent or
invalid. A validator running offline reports references as not checked and
does not fail.

**A quote carries source text.** It reproduces the source verbatim inside the
claim file, so the claim's effective scope governs the exposure of that text.
Implementations SHOULD warn when a claim's effective scope is wider than the
material it quotes, where that is known. Unlike a synthesis, which summarises
its inputs, a quote discloses its source completely.

The same is true of attribution. Promoting an object publishes its
`source.author` URI with it, and a `document.author` discloses *who is being
quoted* as completely as the quote discloses what they said. Neither is a
gate — no promotion is refused on this basis — but a reviewer should read
both as disclosures. Particular files are never served in a feed, so the URI
is the whole exposure, and it is the URI the person chose to be cited under.

---

### `DPARTICULAR`

A particular is a specific, identifiable thing in the world — a person,
project, concept, place, or organisation. Claims are anchored to particulars.
The term is used in its philosophical sense: a concrete individual instance,
distinct from a universal or category.

```yaml
id: par_01916f03-b680-71a2-bad4-40b49d5a5a6d
type: particular
uri: https://example.com/particulars/project-x   # globally unique; resolvable once published
label: Project X                                  # human-readable, non-canonical
aliases:
  - ProjectX
  - project_x
```

The `uri` field is what makes cross-source reasoning possible. Two independent
publishers pointing at the same URI are making claims about the same thing,
regardless of local IDs or labels. For well-known subjects, existing URIs —
Wikidata, DBpedia, ORCID, a DOI, a GitHub URL — are preferred over minting new
ones.

People and agents are particulars too, and the ones that matter most for
provenance: a claim's `source.author` and a document's `author` are
references to particulars (see [Source](#source)). Prefer a global URI for a
person — an ORCID, a DID, a GitHub profile — over a minted one, because an
author is the one particular that recurs across workspaces and needs the
same identity in each. A person's particular carries the URI they are
willing to be cited under at the widest scope their claims may reach:
particular files are never served in a feed, so that URI is the whole of
what a public consumer learns about them. For the same reason an
implementation never mints a person's particular as a side effect — not on
`init`, not when applying `defaults.source.author`, not when writing a
claim. A minted `urn:dkf:…:ben` is opaque where `ben` was readable and,
being workspace-local by construction, carries none of the cross-workspace
identity that is the whole value of an author URI. Until the person defines
themselves, their name is written unchanged and reported as unresolved.

A URI must be **globally unique**. It is not required to be resolvable until
the particular is published to `public` scope: most things an agent learns
about — a module, a decision, an internal service — have no public URL.

#### Minting URIs

When `particular_define` is called without a `uri`, the implementation mints
one:

- `<base-uri><slug>` when the workspace declares a `base-uri` (see
  [`dkf.yaml`](#dkfyaml)), e.g. `https://example.com/particulars/project-x`;
- otherwise `urn:dkf:<workspace-id>:<slug>`, e.g.
  `urn:dkf:01916cb5-32a0-7001-90a6-6195d31a5bb6:project-x`.

`slug` is derived from the label: lower-case it, apply Unicode NFKD and strip
combining marks, collapse every run of characters outside `[a-z0-9]` to a
single `-`, and trim leading and trailing `-`. `Café Société` becomes
`cafe-societe`. Because `particular_define` is idempotent on URI, two labels
that slug identically resolve to the same particular — which is what stops an
agent re-inventing a subject under a slightly different name each session.

This specification claims the `urn:dkf:` namespace for this purpose, and at
v0.1 it is **deliberately unregistered**. The NID syntax conforms to
RFC 8141, every minted URN embeds the workspace UUID — so colliding with any
other use of the NID requires colliding a UUID — and formal registration,
which would change no identifier, may be pursued after v0.1. Publishers are
encouraged to configure a `base-uri` instead, and a merge record can later
join a URN to a public URI.

A particular's `uri` may change only while the particular has never been
published. After publication, the only way to join two URIs is a
[merge record](#merge-records).

---

### `DCLAIM`

A claim is an assertion about a particular, with full source provenance.

```yaml
id: clm_01916f03-b680-71a3-974f-9401ba374e1f
type: claim
subject: par_01916f03-b680-71a2-bad4-40b49d5a5a6d
content: |
  Project X uses a microservices architecture, with separate
  services for auth, billing, and core API.
source:
  author: ben
  harness: claude
  model: claude-sonnet-4-6
  document: https://example.com/docs/architecture.md
context:
  scope: organisation       # personal | organisation | public — required
  topics:                   # optional
    - architecture
    - distributed-systems
timestamp: 2024-08-20T09:00:00Z
evidential: observed        # observed | inferred | held — required
confidence: 0.9
```

`context` and `context.scope` are **required on disk** for every claim and
synthesis. `context.topics` is optional and defaults to empty. When a caller
omits scope, the *writer* applies the workspace default (or `personal`) before
the file is written.

The value in the file is the object's **asserted** scope. Because claims are
immutable it never changes; an object is shared more widely by adding a
[promotion record](#promotion-records), which yields its *effective* scope.
Readers never infer a scope from configuration: eligibility for a feed is
decided by the object file together with the promotion records, and by nothing
else.

#### What backs a claim

Every claim declares an **`evidential`**, answering what would settle it:

| value | the claim is backed by |
|---|---|
| `observed` | someone or something looked |
| `inferred` | reasoning from other claims |
| `held` | nothing external; it is a position |

It is **required, and there is no default.** A writer must not choose a value
on the caller's behalf: if absence meant `observed`, the laziest path would
produce the most authoritative-looking output, which is the failure
`context.scope` is required on disk to prevent.

Readers are lenient, as everywhere else in this format. A claim written
before this field existed is valid, readable, and citable, and its warrant is
reported as **`undeclared`** — which is not a fourth value, is not something
a writer may emit, and is not a synonym for `observed`. It means the warrant
cannot now be established. Claims are immutable, so there is no way to
backfill one; the distinction ages out as new claims are written rather than
being migrated, and that is the honest outcome — backfilling would mean
inventing warrants for claims nobody can still interrogate.

A note on the third value: `held` is not strictly an evidential. Languages
that mark evidentiality grammatically mark *sources of information* —
witnessed, reported, inferred — and none of them mark "this is my opinion",
because a value judgement is not information-sourced. The axis here is
therefore what *backs* a claim, and `held` is the value meaning nothing
external does.

#### Confidence

`confidence` is the inverse probability that the claim is mistaken. It
applies to `observed` claims, whose evidence may have been misread, and to
`inferred` ones, whose reasoning may be invalid.

**A `held` claim carries no confidence.** Writers refuse to create one;
validators fail validation on one, reporting `confidence_on_held`; and
readers still read the file — it cannot be corrected, so a reader that
rejected it would strand it permanently. It is the first rule where the
write-side and read-side verbs genuinely differ, which is why all three are
named. A position is not mistaken in the way a
probability describes: it is not on the scale rather than scoring badly on
it. Attaching a number to a claim nothing backs is the one place this format
would let you assert weight without warrant — and in a format written mostly
by agents, a fluent unsourced judgement carrying `confidence: 0.9` is the
most plausible bad claim it will ever hold.

There is deliberately no field recording strength of conviction. It is a
different quantity, and a numeric one would launder social force into
something that sorts and aggregates; where it matters it belongs in
`content`, which is where this format keeps reasoning. Confidence on an
`undeclared` claim is reported as unverified rather than rejected — every
existing workspace has some.

Claims are immutable once created. Correction happens through synthesis or
retraction, never overwriting. Retraction is recorded, not deletion —
provenance must always be traversable.

---

### `DSYNTHESIS`

A synthesis is a resolved claim derived from one or more thesis/antithesis
inputs. It extends `DCLAIM` — it is itself a valid claim and may serve as a
thesis or antithesis input to further syntheses. No intermediate derived-claim
object is needed.

```yaml
id: syn_01933034-b1a0-705f-b788-2c7c58c46e29
type: synthesis
subject: par_01916f03-b680-71a2-bad4-40b49d5a5a6d
content: |
  Project X ran microservices from 2022–2024, with separate services
  for auth, billing, and core API. The architecture was consolidated
  into a monolith in November 2024 to address latency at scale, though
  service boundaries were preserved as internal modules. The auth
  service remains separately deployable for compliance reasons.
inputs:
  - id: clm_01916f03-b680-71a3-974f-9401ba374e1f
    role: thesis
    weight: primary
  - id: clm_01932b8b-c300-70c4-b1f5-270e927328ce
    role: antithesis
    weight: primary
  - id: clm_01932f48-7ce0-72e1-8c4e-af7596e72997
    role: thesis
    weight: qualifying
unresolved: |
  The compliance basis for retaining a separate auth service is
  asserted but not sourced. Flagged for verification.
source:
  harness: claude
  model: claude-sonnet-4-6
method: reconciliation
timestamp: 2024-11-15T14:23:00Z
context:
  scope: organisation
  topics:
    - architecture
    - distributed-systems
confidence: 0.85
```

A synthesis carries `source` exactly as a claim does, and `source.harness` is
required: every synthesis records the harness that produced it. (Earlier
drafts used a separate `produced-by` field. Readers MAY treat a legacy
`produced-by` block as `source` during v0.1 and SHOULD warn.)

Every claim and synthesis carries exactly one `subject`, and it is always
supplied by the caller: `synthesis_create` takes a `particular_id`, and
implementations MUST NOT derive a synthesis's subject from its inputs.

A synthesis declares no `evidential`. It is backed by argument from its
inputs — that is what a synthesis is — so the value is implied and cannot
vary. What does vary is `method`, which names the kind of question that was
at issue:

| `method` | the inputs |
|---|---|
| `reconciliation` | disagreed about a fact, and this settles it |
| `qualification` | are each true, in different contexts |
| `positions` | disagree in a way no evidence settles |

The two are orthogonal: a synthesis is reached by argument whether the
question was factual or evaluative. A `positions` synthesis **may** still
take a position — Aufhebung produces a new position rather than surveying and
declining — but it says what would move it, and `unresolved` is where it
records that the question is not one evidence closes. Recording an evaluative
conclusion as `reconciliation` is invalid: no factual disagreement was
settled.

Marking a claim `held` does not exempt it from reconciliation. Two conflicting
positions are still unsynthesised and still want a synthesis — one of a
different kind. The label changes what the work is, not whether there is
work.

Inputs MAY have a different `subject` than the synthesis. A claim about a
library can legitimately inform a synthesis about the project that uses it.
Note that citing it does not count as synthesising it for the library's own
particular — see [Conflict semantics](#conflict-semantics). This is also why
the subject cannot be inferred: for a synthesis about project X citing a claim
about library Y, first-input, most-common-input, and all-inputs-agree each
give the wrong answer.

The `unresolved` field is required. A synthesis that makes no acknowledgement
of what it could not reconcile is considered malformed. When the producer
considered the question and found nothing outstanding, the conventional value
is the exact string `None identified`; this lets tooling distinguish
"considered and empty" from "forgotten". A missing, null, or empty
`unresolved` is invalid.

Consumers that do not implement synthesis reasoning MUST treat a `DSYNTHESIS`
as a `DCLAIM` using its `content` field, ignoring synthesis-specific fields.

---

### Retraction

Retraction is recorded by appending a `retracted` block to the retracted
object's own file:

```yaml
# claims/clm_01a01ed5-c040-73b0-ba7b-da8a27ab53a6.yaml
id: clm_01a01ed5-c040-73b0-ba7b-da8a27ab53a6
type: claim
subject: par_01916f03-b680-71a2-bad4-40b49d5a5a6d
content: The billing service listens on port 443.
source: {author: ben, harness: claude}
context: {scope: organisation}
timestamp: 2026-08-20T11:02:00Z
retracted:
  timestamp: 2026-08-21T09:12:00Z
  reason: "Port is 8443, not 443 — deploy/config.yaml:12"
  source: {author: ben}
  kind: defect                                             # optional
  superseded-by: clm_01a02396-7ca0-718d-9a6e-86fd10508af1  # optional
```

Rules:

- Adding a `retracted` block is the **only permitted modification** to an
  existing object file. `timestamp`, `reason`, and `source` are required.
- It is never removed. Reinstatement is a new claim or synthesis that cites
  the retracted object.
- Syntheses are claims and may be retracted. Merge records may be retracted.
- The index mirrors it as `retracted: true`.

The marker lives on the file rather than in a separate object because the
consumer most likely to misuse a retracted claim is one that opens only that
claim's file. A reader that ignores the format entirely still sees the
retraction beneath the claim.

**`kind`** is optional and records *why* the claim died. It has three values,
which are not a taxonomy but the three joints in the chain the claim depends
on:

```
   claim ─────────▶ source ─────────▶ world
     │                 │                │
     ▼                 ▼                ▼
 misreads what    the source        the world
 the source says  was wrong         moved on
     │                 │                │
  defect      provenance-failure   supersession
```

There is no fourth joint, which is why this closure should stay closed.

`kind` is **declared**, never guessed. In particular it MUST NOT be derived
from whether `superseded-by` is present: that field answers whether anything
replaced the claim, which is a different question. The most common defect —
a typo-grade misreading — is corrected by asserting the right value and
pointing at it, so defects routinely carry a replacement; and a claim
retracted because its subject was decommissioned is an honest supersession
with nothing to point at.

Where the retracted object cites a document that can be fetched, an
implementation should report the observed drift alongside the declared kind
as an observation, and leave the judgement to the reader.

It must **not** treat an unchanged hash as evidence against a declared
`supersession`. Drift is a signal about the *source* joint; supersession
asserts that the *world* moved, and the format has no way to tell a document
that describes current state from one dated by design. A claim sourced from
an architecture decision record, an incident report, or a commit-pinned URL
cites something that is supposed to stay byte-identical while the world moves
on, so the check would fire on the ordinary case forever.

The sound check runs the other way: a `defect` declared against a document
that *has* drifted is **unverifiable**, because the text the claim is said to
have misread is no longer the text a reviewer can read. That is a statement
about what can be checked rather than a guess about intent. Checking covers
retracted objects for this reason — the finding is about the retraction, not
about a live claim.

Where the source carries no hash or cannot be fetched, the kind stands
unverified and no warning is due.

**`superseded-by`** is an optional pointer for typo-grade corrections where a
full thesis/antithesis synthesis would be ceremony. It MUST reference an
existing claim or synthesis; validators reject a dangling target. It is
informational — for readers and `lineage_trace` — and does not make the target
an input of anything, nor does it count as synthesis for conflict detection.

---

### Merge records

`particular_merge` declares that two URIs denote the same particular. It
produces a merge record and rewrites nothing:

```yaml
# merges/mrg_01a023a7-e1c0-70a7-9232-ad5090460a2d.yaml
id: mrg_01a023a7-e1c0-70a7-9232-ad5090460a2d
type: merge
uris:
  - https://example.com/particulars/project-x
  - urn:dkf:01916cb5-32a0-7001-90a6-6195d31a5bb6:projectx
reason: Same project; the URN was minted before the public URI existed.  # optional
source: {author: ben, harness: claude}
timestamp: 2026-08-21T09:30:00Z
```

`uris` contains exactly two URIs, and the fields are written in the order
shown: `id`, `type`, `uris`, `reason`, `source`, `timestamp`. Merges are keyed
on URIs rather than local ids because a merge routinely spans sources where
only one side has a local particular.

Non-retracted merge records are **symmetric and transitive**: the particulars
they join form an equivalence class. `knowledge_recall`, `conflict_detect`,
and `lineage_trace`, given any member of a class, operate over the whole
class, and so do the asserted-by and reported-from relations of
[Source](#source), computed over the class of the resolved author. Claims
keep their original `subject` and their original `source` values; nothing is
moved or rewritten. A merge is undone by retracting it, which removes only
that edge.

---

### Promotion records

Claims are immutable, so a claim's scope cannot be rewritten to share it more
widely. `knowledge_publish` instead records the decision:

```yaml
# publishes/pub_01a0f3c1-4d20-7b8e-9a11-6c2f4e7d9b03.yaml
id: pub_01a0f3c1-4d20-7b8e-9a11-6c2f4e7d9b03
type: publish
claims:
  - clm_01916f03-b680-71a3-974f-9401ba374e1f
  - syn_01933034-b1a0-705f-b788-2c7c58c46e29
scope: public
reason: Architecture history cleared for the public docs site.   # optional
source: {author: ben, harness: claude}
timestamp: 2026-08-22T09:30:00Z
```

`claims` lists at least one claim or synthesis id, and the fields are written
in the order shown: `id`, `type`, `claims`, `scope`, `reason`, `source`,
`timestamp`.

An object's **effective scope** is the widest scope named by a non-retracted
promotion record covering it, or its asserted `context.scope` when none does,
ordering `personal` < `organisation` < `public`. Feed eligibility is computed
from the object file together with the promotion records — never from
`dkf.yaml`.

**Promotion may only widen.** A record naming a scope narrower than an
object's asserted scope is invalid. This fixes the direction in which the
format fails: a consumer that ignores `/publishes/` and honours
`context.scope` will withhold something that was in fact authorised, but it
can never expose something that was not. If narrowing were expressible, that
same consumer would read `public` on a file that had since been restricted and
leak it. Narrowing is done by retracting the promotion — which is visible on
the file a naive consumer already opens — or by retracting the object.

**Promotion does not cascade.** Promoting a synthesis does not promote the
claims it cites, so a public consumer may receive a synthesis citing input ids
it cannot resolve. That is the intended default: cascading would silently
widen an entire lineage, and promotion is meant to be explicit and deliberate.
Publishers who want a traversable public chain promote the inputs too.

**A synthesis may be wider than its inputs, and that is warned rather than
forbidden.** Reconciling narrowly-scoped evidence into a conclusion that can
be shared is a legitimate reason to synthesise, and no tool can judge whether
the resulting prose discloses its sources — so the judgement belongs to
whoever reviews the change. Implementations SHOULD warn when a synthesis's
effective scope is wider than the effective scope of any input it cites, and
report that condition as `scope_wider_than_inputs`. They must not reject the
synthesis, and must not try to decide whether its content in fact reveals its
inputs.

The comparison is between *effective* scopes on both sides, which matters in
both directions: an input promoted to match the synthesis is no longer a
concern, while a synthesis promoted past inputs that were never widened is.
For the same reason the condition belongs to workspace state rather than to
the synthesis file — a promotion can create it, or clear it, without either
file changing. Implementations evaluate it when a synthesis is created, when
`knowledge_publish` promotes one, and during validation.

A promotion is retracted like any record, after which the objects it covered
revert to their asserted scope and leave future feeds. Retraction cannot
recall what an external consumer already fetched; nothing in this format can.

---

## Object Model

```
DPARTICULAR   the anchor — a specific, identifiable thing, people included

DCLAIM        an assertion about a particular
                ← source: who/what asserted it — author is a particular
                ← subject: which particular it concerns
                ← context: scope (required) and topics

DSYNTHESIS    extends DCLAIM
                ← inputs[]: N claims with role and weight
                ← unresolved: what wasn't fully reconciled
                ← source.harness: required
                → is itself a valid input to further syntheses

records       retraction — a block appended to any of the above
              merge      — joins two particular URIs
```

The lineage graph is a directed acyclic graph of claims. The full graph is
always preserved and traversable.

### Conflict semantics

Without an LLM in the loop, "contradiction" is not computable. What *is*
computable is what has not been reconciled, and every consumer can rely on
that. For a particular (or merge equivalence class):

- **current** — the most recent non-retracted synthesis whose `subject` is in
  the class, ordered by `timestamp`, ties broken by id.
- **unsynthesised** — non-retracted claims and syntheses with `subject` in the
  class that are not in the transitive `inputs` of `current`.
- **stale** — non-retracted syntheses with `subject` in the class that cite a
  retracted input, directly or transitively.

**The current belief about a particular is `current`**, even when claims
post-date it. Those later claims are not silently the new belief; they are
surfaced as `unsynthesised` until a synthesis absorbs them.

`conflict_detect` reports a particular when:

- `current` exists and `unsynthesised` is non-empty; or
- `current` does not exist and `unsynthesised` has two or more members; or
- `stale` is non-empty.

The suggested synthesis priority is `|unsynthesised| + |stale|`. Whether any
two members actually contradict is the reasoning harness's judgement, not the
tool's.

Two consequences follow:

- **Retraction does not cascade by mutation.** Retracting an input leaves the
  syntheses that cite it untouched — they are immutable and were already
  reasoned. They are reported as `stale` until a newer synthesis supersedes
  them. A `superseded-by` pointer is not synthesis: the replacement object is
  `unsynthesised` like any other.
- **Cross-particular inputs are per class.** A claim about Y cited by a
  synthesis about X is not thereby synthesised for Y.

Merge records take part in this, because they decide which particulars share a
class. Promotion records do not: they are not knowledge, they form no class,
and they change no conflict set.

---

## File Layout

```
/dkf.yaml                      workspace marker and configuration
/.dkf                          optional pointer, when tools start elsewhere

/particulars/
  par_01916f03-b680-71a2-bad4-40b49d5a5a6d.yaml

/claims/
  clm_01916f03-b680-71a3-974f-9401ba374e1f.yaml
  clm_01932b8b-c300-70c4-b1f5-270e927328ce.yaml

/syntheses/
  syn_01933034-b1a0-705f-b788-2c7c58c46e29.yaml

/merges/
  mrg_01a023a7-e1c0-70a7-9232-ad5090460a2d.yaml

/publishes/
  pub_01a0f3c1-4d20-7b8e-9a11-6c2f4e7d9b03.yaml

/index.yaml                    derived cache — see below
```

### `dkf.yaml`

A workspace is identified by a `dkf.yaml` at its root. Implementations find
the workspace by walking up from the working directory, exactly as git finds
`.git`.

```yaml
format: dkf/0.1
workspace:
  id: 01916cb5-32a0-7001-90a6-6195d31a5bb6   # bare uuidv7; used in urn:dkf: URIs
  base-uri: https://example.com/particulars/  # optional; MUST end in '/'
defaults:                                     # optional
  scope: personal
  source:
    author: ben
    harness: claude
```

`format` and `workspace.id` are required; everything else is optional.
Implementations MUST ignore unknown keys so the file can be extended.

`defaults` are applied by **writers only**, when a tool call omits a value:
`scope` fills `context.scope`; `source` fields fill an incomplete `source`.
Readers never consult `defaults` — every object file is interpretable on its
own.

#### Discovery

Explicit configuration wins: a workspace argument, then an environment
variable. Failing those, implementations walk up from the working directory
and at each ancestor:

1. a `dkf.yaml` makes that directory the workspace;
2. otherwise a `.dkf` file redirects to the workspace it names.

A `.dkf` holds a path on its first non-blank, non-comment line, resolved
relative to the directory containing the pointer or taken as absolute:

```
repo/
  .dkf            → "knowledge"
  knowledge/
    dkf.yaml
  src/            ← a tool started here finds repo/knowledge
```

This exists because tools usually start *above* a workspace rather than
inside one — at a repository root, in an agent session, in a checkout the
session did not choose — and without it every verb fails until someone
supplies a path.

Pointers do not chain: the named directory MUST contain `dkf.yaml`, and a
pointer whose target does not is an error naming both paths. A `.dkf` is not a
workspace marker — it carries no configuration, and a workspace remains
discoverable from inside it whether or not any pointer exists. The redirect is
deliberately not a `dkf.yaml` with a `root:` key, because that file *is* the
marker to every conformant reader, which would make the repository root look
like an empty workspace.

### `index.yaml`

The index is a lightweight manifest of all IDs, types, subjects, and
relationships. It enables recall and conflict detection without parsing every
file.

The object and record files are the **source of truth**. The index is a
derived, regenerable cache: it MUST be fully reconstructible from the files,
and a local consumer MUST NOT return wrong results because it is missing or
stale (it may be slower). Two branches that each add a claim will both touch
`index.yaml`; the conflict is resolved by regenerating it, never by hand.

The index nonetheless stays committed, because HTTP consumers cannot list a
directory — for them it is the enumeration mechanism, and they should treat it
as potentially lagging the files.

```yaml
# index.yaml
format: dkf/0.1
entries:
  - id: par_01916f03-b680-71a2-bad4-40b49d5a5a6d
    type: particular
    uri: https://example.com/particulars/project-x
  - id: clm_01916f03-b680-71a3-974f-9401ba374e1f
    type: claim
    subject: par_01916f03-b680-71a2-bad4-40b49d5a5a6d
    scope: organisation
    topics: [architecture, distributed-systems]
    timestamp: 2024-08-20T09:00:00Z
    author: https://orcid.org/0000-0002-1825-0097
  - id: clm_01a01ed5-c040-73b0-ba7b-da8a27ab53a6
    type: claim
    subject: par_01916f03-b680-71a2-bad4-40b49d5a5a6d
    scope: organisation
    timestamp: 2026-08-20T11:02:00Z
    retracted: true
  - id: syn_01933034-b1a0-705f-b788-2c7c58c46e29
    type: synthesis
    subject: par_01916f03-b680-71a2-bad4-40b49d5a5a6d
    inputs:
      - clm_01916f03-b680-71a3-974f-9401ba374e1f
      - clm_01932b8b-c300-70c4-b1f5-270e927328ce
      - clm_01932f48-7ce0-72e1-8c4e-af7596e72997
    scope: organisation
    timestamp: 2024-11-15T14:23:00Z
  - id: mrg_01a023a7-e1c0-70a7-9232-ad5090460a2d
    type: merge
    uris:
      - https://example.com/particulars/project-x
      - urn:dkf:01916cb5-32a0-7001-90a6-6195d31a5bb6:projectx
  - id: pub_01a0f3c1-4d20-7b8e-9a11-6c2f4e7d9b03
    type: publish
    scope: public
    claims:
      - clm_01916f03-b680-71a3-974f-9401ba374e1f
      - syn_01933034-b1a0-705f-b788-2c7c58c46e29
```

Baseline fields: every entry has `id` and `type`; particulars have `uri`;
claims and syntheses have `subject`; syntheses have `inputs`; merges have
`uris`; promotions have `claims` and `scope`. Entries MAY also carry `scope`,
`topics`, `timestamp`, `retracted: true`, and `author` and `document-author`
— the last two mirroring the object's `source.author` and
`source.document.author` as written — so that `knowledge_recall` can filter
without opening files.
Implementations MAY add further fields, and future versions of this
specification MAY add further entry types; consumers MUST ignore fields and
entries they do not understand.

An implementation that rebuilds the index MUST **preserve** entries whose
`type` it does not recognise, unchanged and in their canonical order — a
rebuild that dropped them would turn a read-compatibility gap into data loss
in the cache, stripping (say) the promotion rows every time an older tool
touched the workspace, with the loss surfacing only when a newer tool next
computes effective scope from the index. For the same reason a drift check
MUST NOT report unrecognised entry types as differences: a check must not
fail on evidence of a newer conforming writer.

Implementations are expected to provide an operation that rebuilds the index
from the files, and a check that reports — without modifying anything —
whether the committed index has drifted from the files, suitable for CI.
The check tolerates what the committed index could not have known: a field
this specification marks MAY that is absent from a committed entry is not
drift, so a newer implementation that writes `author` into entries does not
fail every index committed before the field existed. A MAY field present on
both sides with different values is drift, as is any missing or extra
entry. This is the local form of the tolerance remote consumers already
have — an index may lag the files — and it is generic, so the next MAY field
costs nothing.

---

## MCP Server Tools

A reference MCP server implementation exposes eleven tools grouped into four
areas.

### Particular Tools

| Tool | Description |
|---|---|
| `particular_define(uri?, label, aliases[])` | Create or update a particular. Idempotent on URI. When `uri` is omitted one is minted from the label (see [Minting URIs](#minting-uris)). |
| `particular_resolve(query)` | Find a particular by ID, URI, label, or alias. Returns null if no match; when a label or alias matches more than one particular, reports the candidates and resolves none. |

### Claim Tools

| Tool | Description |
|---|---|
| `claim_assert(particular_id, content, evidential, source, context, confidence, scope)` | Create a new claim. `evidential` is required and has no default; `held` with a `confidence` is refused. If scope is omitted the workspace default (or `personal`) is written into the file. |
| `claim_retract(claim_id, reason, source)` | Append a `retracted` block to a claim or synthesis. Never deletes — provenance is preserved. |

### Synthesis Tools

| Tool | Description |
|---|---|
| `synthesis_create(particular_id, content, inputs[], unresolved, source)` | Record a synthesis the calling LLM has already reasoned. `particular_id` accepts an id, URI, label, or alias and MUST be supplied — the subject is never derived from the inputs. `source.harness` is required. The LLM reasons; this tool stores. |

### Query Tools

| Tool | Description |
|---|---|
| `knowledge_recall(particular_id \| query, author?, scope, include_retracted, limit)` | Retrieve claims and syntheses about a particular or topic, or by `author` — an id, URI, label, or alias — returning objects asserted by or reported from that particular's merge class, each carrying `relations` — a set of `asserted` and/or `reported`, never empty. Combinable with the other filters. Returns in lineage order, identifying `current`. Operates across merged particulars. |
| `conflict_detect(particular_id \| claim_ids[])` | Return the structural `current` / `unsynthesised` / `stale` sets and a suggested synthesis priority (see [Conflict semantics](#conflict-semantics)). Judging actual contradiction is left to the harness. |
| `lineage_trace(claim_id, depth)` | Traverse the provenance chain of any claim or synthesis, including `superseded-by` successors. Returns a structured tree. |

### Federation Tools

| Tool | Description |
|---|---|
| `feed_index(uri, topics[])` | Crawl and index an external knowledge source publishing DKF. Topics enable selective crawling. |
| `particular_merge(uri_a, uri_b, source)` | Declare two URIs as the same particular. Writes a [merge record](#merge-records) without rewriting claims. |
| `knowledge_publish(claim_ids[], scope, source, reason?)` | Promote claims from personal or organisation scope to public by writing a [promotion record](#promotion-records). Widening only. Explicit and deliberate — not a default. |

The typical LLM reasoning loop is:

```
particular_resolve → knowledge_recall → conflict_detect
  → [reason internally] → synthesis_create
```

---

## Public Discovery

Publishers exposing DKF knowledge on the public internet place a manifest at
a well-known path:

```yaml
# https://example.com/.well-known/knowledge.yaml
format: dkf/0.1
index: /knowledge/index.yaml
feeds:
  - /knowledge/claims/
  - /knowledge/syntheses/
  - /knowledge/merges/        # optional
  - /knowledge/publishes/     # optional; lets a crawler verify effective scope
topics:
  - distributed-systems
  - knowledge-management
publisher:
  uri: did:web:example.com
  label: Example Organisation
```

`format`, `index`, and `feeds` are required; `topics` and `publisher` are
optional; unknown keys are ignored, as everywhere else in this format. Paths
resolve against the site root. Every published object is fetchable at a feed
path plus `<id>.yaml`, the index enumerates every published object, and a
remote consumer treats the index as potentially lagging the files.

A feed serves only objects whose **effective scope is `public`**. Serving the
promotions feed lets a consumer verify that filtering for itself; a publisher
that omits it asks to be trusted on it. An authenticated private surface — an
organisation's search index, an exporter behind a tenant login — is not a
feed and is not bound by this contract, which governs publishing to the open
internet.

The `topics` field enables targeted crawling — a reasoning task scoped to a
domain only fetches sources that declare relevance. Beyond that, this
specification deliberately defines no crawl protocol: fetch scheduling,
change detection, and politeness are properties of consumers, not of the
format. The publishing contract above is the whole contract, and index
`timestamp` fields already give incremental fetching what it needs — the
model that served `.ics` and RSS, which specified the artefact and left the
fetching to HTTP.

---

## Trust and Provenance

**Cryptographic signing** — claims may be signed with the publisher's DID.
Signatures are optional in v0.1 but the field is reserved, and the payload it
would cover is defined: the object parsed to its data model with `retracted`
and `signature` removed, canonicalised per
[RFC 8785](https://www.rfc-editor.org/rfc/rfc8785) (JSON Canonicalization
Scheme). Not the file bytes — so a signature survives reformatting, field
reordering, and the later appending of a retraction, none of which change
what was asserted, and `confidence: 0.9` and `0.90` sign identically for the
same reason CRLF and LF hash identically: normalise the artefact, sign the
assertion.

The payload is built from the parsed, *typed* data model, never from a
generic YAML-to-JSON conversion — a YAML 1.2 parser returns an unquoted
timestamp as a native time value, and only the typed model formats it back to
the string this format requires. In the data model, keys are strings; values
are strings, numbers, booleans, arrays, and mappings; every field this
specification defines as textual — timestamps, ids, references — is a string;
`confidence` is a number. Aliases are resolved before the data model exists
and never affect the payload; object files must not use YAML anchors and
aliases at all, as a file-format safety rule — alias expansion is a
resource-exhaustion vector — and validators should reject files carrying
them. Signature *suites* — algorithms, key formats, DID binding — remain
reserved: v0.1 defines only what the bytes would be. The identity a
signature would naturally bind is the author particular's URI — which is why
`source.author` prefers a URI (see [Source](#source)) — though that binding,
like the suites, is left to the signing specification.

**Citation weight** — a synthesis that cites a claim increases that claim's
standing in downstream reasoning, analogous to PageRank. Consensus across
independent syntheses is a stronger signal than source confidence alone.

**Asserter attribution** — every synthesis records the harness that produced
it in `source.harness`, and the model in `source.model` where known; every
object whose `source.author` resolves records the particular that asserted
it. The observation this is assessed from is the retraction `kind`: a
`defect` counts against the process that produced the claim — the asserting
particular and the harness; a `supersession` counts against nothing; and a
`provenance-failure` counts against the cited document and, where one
resolves, its `author` — which also makes the other claims citing that
document, or reported from that person, identifiable as candidates for
review. Recording who produced a claim is only half of it; without a record
of whether they produced it correctly there is nothing to reason over. While
authors were strings this was computable only per harness; it now applies
to any person or agent, and nothing requires the count — implementations
may report it.

**Scope isolation** — claims whose effective scope is `personal` or
`organisation` are never surfaced in public feeds. Effective scope is the
object's asserted `context.scope` widened by any [promotion
record](#promotion-records) covering it, and promotion is an explicit act
recorded with a source. Both halves live in committed files, so the decision
never depends on workspace configuration — and because promotion can only
widen, a consumer that reads the object file alone can withhold too much but
never expose too much.

**Findings and facts** — a reportable condition is one of two kinds, and the
distinction governs how it is reported. A *finding about an object* is
something someone might act on at that object — drift on a claim's source, a
synthesis wider than its inputs, an unverifiable defect, a dangling
reference — and is reported per object, because the object is the unit of
action. A *fact about the corpus* carries no per-object action — an
`undeclared` evidential, a legacy compatibility marker, a document that
cannot be verified, an author name that resolves to no particular or to
several — and is reported in aggregate: its discovery value is spent the
first time it is seen, its cost recurs on every run, and it cannot be
cleared at any object — either because clearing it would mean rewriting an
immutable file, or because the action that clears it is at the workspace and
clears every occurrence at once. An aggregate line carries a count always,
and the condition's message
only when it is identical across the group — attributing one object's reason
to ninety-five is misreporting. The format's design leans on warnings being
read, so their legibility is load-bearing rather than cosmetic; a validator
whose output is dominated by permanent unactionable lines has spent
`scope_wider_than_inputs` and both drift states along with them.

---

## Design Principles

**Contradiction is signal, not error.** The format is built around preserving
disagreement, not resolving it silently.

**Provenance is non-negotiable.** Nothing is overwritten. Appending a
retraction is the only modification to an existing file; synthesis is the
only way to change what is believed. The full reasoning chain is always
traversable.

**Minimal spec, layered implementation.** Three knowledge objects —
particular, claim, synthesis — are the complete core, plus records —
retraction, merge, publish — that are events about objects rather than
knowledge. Entity types, ontologies, topic taxonomies, and trust hierarchies
are implementation concerns.

**Backward compatibility by design.** A consumer that ignores synthesis-
specific fields gets a valid claim. A consumer that ignores `/merges/` still
reads every claim correctly. A consumer that ignores the format entirely gets
readable YAML. Reading does not require full implementation; writing a
conformant claim does, since a claim that does not say what backs it is not
one this format can reason over.

**Files over databases.** The canonical store is a directory of YAML files
in a git repository. Git provides version history, authorship, and diff
visibility for free. The index is a cache of the files, never the reverse.
Databases are an implementation optimisation, not a requirement.

---

## Status

This specification is in early draft. The object model, tool list, identifier
format, canonical field order, the retraction, merge and promotion
representations, the evidential, and the structural conflict semantics are
stable, as are the signed payload's definition, the public discovery
contract, and the namespace position. The evidential was the last breaking
change before v0.1, folded in rather than deferred because declaring v0.1 is
the invitation for a second implementation to appear, and breaking the format
is cheap only while one exists.

**v0.1 was declared on 2026-08-26** (tag `v0.1`). Nothing was left open
before it, and declaring it was a deliberate act rather than a side effect of
the last change landing.

The first change after it is additive: `source.author` and a document's
`author` are references to particulars, so who asserted a claim and who is
being reported are structural rather than prose — see [Source](#source). No
existing file changes validity and no existing reader changes its results.
It touches three items deferred past v0.1 — DID binding for the reserved
signature, promotion by particular, and whether a synthesis carries a
`document` — and takes none of them; each is easier to decide now that an
author has a URI.

A reference implementation,
[`particulars-cli`](https://github.com/nodelogicau/particulars-cli), exists
and its feedback shaped the current text.

Feedback on the spec itself — object model, field names, missing cases — is
the most valuable contribution at this stage.

---

## Contributing

Open an issue to discuss changes to the object model or field definitions
before submitting a pull request. The spec is a human document first;
implementation follows from it, not the other way around.

See [CONTRIBUTING.md](CONTRIBUTING.md) for guidance on proposing changes,
the RFC process for breaking changes, and how to submit a reference
implementation.

---

## License

The specification is released under [CC0 1.0 Universal](LICENSE). Reference
implementations are released under the MIT License. You are free to implement
the format without restriction.
