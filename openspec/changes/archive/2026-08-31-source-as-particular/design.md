## Context

This came out of an exploration on 2026-08-31 of two possible additions to the particular: a coarse kind, and the ability to stand as the source of a claim. The second is taken here; the first is left for its own proposal. It touches three items already deferred past v0.1 — signature suites and DID binding, promotion by particular, and whether a synthesis carries a `document` — and takes none of them, which is deliberate: each becomes easier to decide once authors are particulars, and harder if this change tried to decide them on the way through.

Current state. `source.author` and `source.harness` are strings; `source.document` is a string or a mapping of `ref`, `hash`, `quote`. `particular_resolve` accepts an id, URI, label, or alias and is specified only for the zero-match case. Merge records form equivalence classes that `knowledge_recall`, `conflict_detect`, and `lineage_trace` honour for *subjects*. The Trust section computes harness attribution from retraction `kind`. Particular files are not served in any feed — the manifest lists claims, syntheses, merges, and promotions — so a public consumer learns a particular's URI from the index and nothing else about it.

Three constraints from earlier rounds govern what follows. Writers strict, readers lenient. A field earns its place only if a process needs it before it can act. And claims are immutable, so whatever is written today is what readers must go on accepting.

## Goals / Non-Goals

**Goals:**
- Make "who asserted this" and "who is being reported" structural, so they can be queried and joined across merge classes rather than searched for in prose.
- Give the reserved signature an identity to bind to without specifying signing.
- Let the retraction-kind attribution the format already defines apply to people and agents, not only harnesses.
- Change no existing file's validity and no existing reader's results.

**Non-Goals:**
- A `kind` or sortal on particulars. Explored in the same session; separate proposal.
- `harness` or `model` as particular references. A harness is a process, not an individual, and the attribution that matters for it already works on the string.
- A scope on particulars. See D6 for why this change does not need one.
- A fourth, reportative evidential. See D3.
- Signature suites, DID resolution, or a rule for author-less signed retractions. Still the signing change's.
- Deciding whether a synthesis carries `document`. Still open; see Open Questions.

## Decisions

### D1. `author` becomes a particular reference, and a name is still a valid one

The value of `source.author` may be one of three things, and readers accept all three:

```
  written as                   resolves by            example
  ───────────────────────────────────────────────────────────────────────
  particular id                exact id               par_01a0…
  URI                          uri, through merges    https://orcid.org/0000-…
  bare name                    label or alias,        ben
                               exactly one match
```

Resolution is best-effort and lenient in the same register as document verification: a reference that resolves to nothing is **unresolved**, not invalid. `author: ben` in a workspace with no Ben particular means today exactly what it meant yesterday — an opaque name that satisfies the source minimum.

*Why not a new field* (`author-ref`, `asserter`): two fields for one fact is the shape that produces drift between them, and the existing field already holds the identity — it just held it as a string nobody could join. Widening the value forms is what `particular_id` tool parameters already do ("accepts an id, URI, label, or alias"); this applies the same rule to a field.

*Why names resolve at read time rather than only at write time:* it is what makes the change retroactive without touching a file. The dogfood workspace has 150 objects saying `author: ben`; defining one particular with alias `ben` attributes all of them. Claims are immutable, so this is the only way an existing workspace could ever benefit.

### D2. Writers emit the URI, not the id

When the author is a defined particular, a writer SHOULD write its **URI**. This is the one place the format prefers a URI over a `par_` id, and the asymmetry with `subject` needs stating because it looks like an inconsistency:

```
  subject     workspace-local anchor by design; the particular file
              travels with the workspace; a par_ id is the right key.

  author      the one particular that recurs across workspaces.
              Ben has a different par_ id in every workspace he writes in
              and the same URI in all of them. A source block is also the
              part of a claim most likely to be read outside its
              workspace — it is what a signature identifies — so it
              carries the cross-workspace identifier.
```

A URI is also what merge records join, so an author written as `urn:dkf:<ws>:ben` in one workspace and as an ORCID in another becomes one asserter the moment a merge record says so. A `par_` id is joinable only via the particular file's URI, one hop that a consumer holding a single claim file cannot take.

When a writer is given a bare name — including from `defaults.source.author` — and it resolves to exactly one particular, the writer SHOULD write that particular's URI. On zero or several matches it writes the name unchanged. This means a workspace's claims begin carrying `author: https://…` from the moment the person is defined, which is a visible change in every diff thereafter; that visibility is the point, and the URI is readable where a `par_` id would not be.

### D3. Reported speech lives on the document, not on a new evidential

"Jane said X" tempts a `reported` evidential — the reportative is exactly what languages with grammatical evidentiality mark. DKF chose three values for what *backs* a claim, and testimony is backed by someone having looked: the recorder observed Jane's utterance, and the utterance is the `document`. What was missing is not a fourth value but a field for **who produced what was read**:

```yaml
source:
  author: https://orcid.org/0000-0002-…        # who put it in the workspace
  harness: claude
  document:
    ref: meetings/2026-08-30.md                # what was read
    author: urn:dkf:01a0…:jane                 # who produced what was read
    quote: we went microservices in Q2
```

`document.author` sits after `ref` and before `hash` because it identifies the source, and identification precedes verification. `ref` stays required: an unrecorded utterance already has a `ref` form (`conversation with Jane, 2026-08-30`), and this change does not need to relax anything there.

The decomposition is clean because it matches the joints the format already has. The chain is claim → source → world. `source.author` is who made the claim; `source.document` is what they read; `document.author` is who made *that*. A `provenance-failure` retraction — "the source was wrong" — now has a person it can count against as well as a URL.

### D4. Two relations, never collapsed

An object is **asserted by** the particular its `source.author` resolves to, and **reported from** the particular its `source.document.author` resolves to. Both are computed over merge equivalence classes, like every other particular relation. "Everything Jane said" is the union, but the two halves are always distinguishable in results, because they mean different things about Jane's reliability: a defect in a claim Jane asserted is Jane's misreading; a defect in a claim reported from Jane is the recorder's, and a provenance-failure in one is Jane's.

`knowledge_recall` gains an `author` filter returning both, labelled. This is the process that needs the field before it can act, and the only tool change.

### D5. Resolution never guesses

A bare name matching more than one particular resolves to **none**. `particular_resolve`, specified today only for zero matches, reports ambiguity rather than picking. The reference implementation already exits 2 with candidates; the spec catches up. Ambiguity is a per-object finding (`author_ambiguous`), because the action — add an alias, or merge — is at that workspace and clears it. An unresolved name is a fact about the corpus, reported in aggregate, because it recurs on every claim until someone defines the particular and cannot be cleared on any one file.

### D6. Disclosure is stated; particulars stay unscoped

The worry: promoting a claim that references Jane publishes Jane. Two facts bound it. Particular files are not served in feeds, so the exposure of an author reference in a public claim is the **URI and nothing else** — no label, no aliases. And that exposure already exists: `author: jane` in a promoted claim discloses a name today. What changes is that the disclosure is now a URI the person chose, which is why the README will say that a person's particular carries the URI they are willing to be cited under at the widest scope their claims may reach — an ORCID if they publish, a `urn:dkf:` URN if they do not.

`document.author` is the sharper case: it discloses *who is being quoted*, which is as complete a disclosure of the source as `quote` is of what was said. The spec states this in the same register as the quote-disclosure rule — a statement a reviewer reads, not a gate — and leaves the judgement with whoever reviews the promotion. A scope on particulars would be the gate; it is not needed for this and belongs with the `kind` question, where particulars may grow fields anyway.

### D7. Asserter attribution generalises harness attribution

The Trust section's observation — a `defect` counts against the process that produced the claim, a `provenance-failure` against the cited document, a `supersession` against nothing — was defined for `harness` because that was the only structured identity. It now applies to any resolved author, and `provenance-failure` additionally to a resolved `document.author`. Implementations MAY report it; nothing requires the count. The signing story converges here: the identity a signature would bind is the author particular's URI, which the README will say as prose and the signing change may later make normative.

## Risks / Trade-offs

- [Write-time resolution silently changes what `author` looks like in every new claim once a person is defined] → Only on exactly one match; the URI is human-readable; and the alternative — writing ids or leaving names — forfeits the join that motivates the change.
- [Two people share a name in an organisation workspace] → D5: neither resolves, the finding names both, and an alias or a merge fixes it. The failure is loud, not wrong.
- [Author URIs minted as `urn:dkf:` URNs are workspace-local, so cross-workspace attribution needs a merge or a global URI] → The README already prefers global URIs for well-known subjects; people are the clearest case. A merge record joins a URN to an ORCID after the fact.
- [Agents put the speaker in `document.author` and also in the content, or in `author` by mistake] → Skill guidance: who told you goes in `--document-author`; `author` is you or the human you work for. Reviewers see both in the diff.
- [A `document.author` on a synthesis sharpens an existing category question] → Named in Open Questions; this change adds the field wherever `document` is permitted and does not extend where `document` is permitted.
- [Readers that predate the change] → Ignore `document.author` and read `author` as a string — which loses the join and nothing else. The index fields are covered by the existing ignore rule.

## Migration Plan

Additive. No file changes shape; no existing workspace fails validation. An index rebuild adds `author` / `document-author` to entries whose files carry them. `particulars-cli`: `claim assert` gains `--document-author` and accepts id/URI/name for `--author`; `recall --author`; `particular resolve` behaviour is already conformant; `validate` gains `author_ambiguous` and an aggregate unresolved-author line. Rollback is not needed — a reader that stops honouring the fields returns to today's results.

## Open Questions

- **Does a synthesis carry `document`?** Deferred by `verifiable-provenance` and not settled here. If it does, `document.author` applies; if it does not, this change makes the category error one field wider. Worth deciding before the signing change, since the signed payload includes `source`.
- **DID binding.** The natural rule is that a signature binds to the author particular's URI, and that a DID-signed retraction could then omit `author`. Both remain the signing change's decisions; this change only makes them nameable.
- **`defaults.source.author` as a URI.** Nothing forbids it today and the value forms make it meaningful. Whether `init` should mint the author's particular is an implementation choice.
- **Whether particulars acquire a scope** when they acquire a `kind`, which would turn D6's statement into a gate.
