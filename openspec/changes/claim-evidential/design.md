## Context

This came out of the same review that produced `verifiable-provenance`: a comparison against an independently-built personal knowledge graph, which types every claim by *mood* — assertion, belief, observation, intention, commitment, question — as a closed axis. Importing that list would have been the wrong move, and the first attempt to justify it here was exactly that: argument from another system's feature table.

The version that survived is derived rather than borrowed, and arrived by two corrections. The first was noticing that the *nature of a source* determines what a claim can honestly be — an unhashable source cannot back an assertion of fact the way a committed file can. The second was that this is not a binary. Between "go and check" and "that is your opinion" sits a large class of claims that are true by *derivation* — most of the interesting claims in our own workspace are of this kind — and a binary had nowhere to put them.

Three constraints from prior rounds govern what follows. Readers are lenient and writers strict. A field earns a place only if a process needs it before it can act — the test that `weight`, `method`, and `role` all currently fail. And claims are immutable, which turns out to be the binding constraint on how this can ship at all.

## Goals / Non-Goals

**Goals:**
- Let a reader tell what backs a claim, so an agent composing an answer does not present a position as a finding.
- Give `confidence` a definition, and stop it being applied where it means nothing.
- Give a synthesis a way to say that a disagreement is not the kind evidence settles.

**Non-Goals:**
- A mood or modality system. DKF is past-tense by construction and needs no `intention` or `commitment`; those exist in the comparison system because they route to detail tables and propose plans.
- Recording strength of conviction. See D4.
- Deciding whether a claim's declared evidential is honest, which no tool can do.
- Backfilling existing claims, which the format forbids.

## Decisions

### D1. The axis is what backs the claim, and it has three values

Not what kind of speech act it is, and not how certain the author feels — what would settle it:

```
  what settles it     value       already in DKF?
  ──────────────────────────────────────────────────────────────
  observation         observed    yes, as a claim with a document
  argument            inferred    yes — this is what a DSYNTHESIS is,
                                  the format just never named it
  nothing external    held        no. This is the missing row.
```

The middle row is the reason to believe this closure is right rather than invented. DKF already has an object whose warrant is argument rather than observation, and whose entire design reflects that: a synthesis is checkable against its inputs and reasoning rather than against a source, which is precisely why `unresolved` is mandatory on it and why it is the object that requires `source.harness`. The category was built before it was named.

`inferred` is preferred over `argued` because it matches the standard term in the evidentiality literature, which is the closest linguistic precedent. Worth stating plainly rather than discovering later: **`held` is not strictly an evidential.** Natural languages grammaticalise sources of information — witnessed, reported, inferred — and none of them mark "this is my opinion", because a value judgement is not information-sourced. The axis is therefore "what backs this", and `held` is the value meaning *nothing external does*. We are extending the category, not borrowing it intact.

*Why not derive it from `source`:* only the documented case is derivable. A claim carrying `{author: ben}` may be a direct observation ("I ran it and saw 8443"), an inference, or a position, and `source` cannot distinguish them. Source records who and what they read; it never records how they know.

### D2. Required, with no default

The alternative — absent means `observed` — makes the laziest path produce the most authoritative-looking output, which is the failure `context.scope` was made mandatory-on-disk to prevent.

The decisive argument is about direction, and it is specific to this format rather than general spec hygiene:

```
  forbid now → relax later     every existing workspace stays valid
  permit now → tighten later   the offending claims cannot be fixed,
                               because claims are immutable. Only
                               retracted and re-asserted, losing ids
                               and lineage.
```

In an append-only format the permissive choice is the irreversible one. The project has already paid for this lesson once: `defaults.scope: personal` was a one-way door that took issue #14 and an entire record type to escape, on a workspace of 38 claims.

### D3. `undeclared` is what readers report, and it is not a value

Required-on-every-claim collides with immutability: there is no legal way to add the field to a claim that already exists, so every workspace in existence would become permanently invalid the moment it is required.

The resolution is the discipline the format already runs on everywhere — writers strict, readers lenient. Writers MUST declare. Readers MUST accept absence and report `undeclared`, which is neither a fourth value nor a synonym for `observed`: it means the claim predates the field and its warrant cannot now be established. It does not license `confidence`; it means nobody can check whether confidence was licensed. Not valid, not invalid — unverified, in the same register the provenance change uses for unfetchable sources.

The practical consequence is that the distinction ages out rather than migrating. That is the only shape available here, and it is defensible on its own terms: backfilling would mean inventing warrants for claims nobody can now interrogate.

### D4. A held claim cannot carry confidence

`confidence` is the inverse probability that a claim is mistaken. That applies to `observed` (evidence can be misread) and to `inferred` (an inference can be invalid). A position is not mistaken in the way a probability describes, so the scale does not apply — the claim is not on it rather than scoring badly on it.

This is the decision that makes the axis structural instead of descriptive. It is the only mechanically enforceable rule anywhere in this design space: `scope_wider_than_inputs`, source drift, and retraction kind can each only warn, because judging prose is not something a machine does. Here two fields on one file settle it, with no traversal, no network, and no context. Without the gate, `evidential` would be advisory metadata — which, by this project's own test, is what `weight` and `method` already are.

*On recording conviction:* the obvious objection is that strength of feeling is real information, and a mild preference differs from a firm one. It must not become a `conviction:` field. That would be the same trap wearing a disguise, laundering social force into a number that sorts and aggregates. Where it matters it belongs in prose, which is where this format puts reasoning.

*On the permissive alternative:* allowing `held` with confidence is arguably worse than today's silence. `{harness: claude}` + `held` + `confidence: 0.9` reads as "I know this is a position and I am ninety percent sure of it", which is a more authoritative artifact than an unlabelled opinion, because the label signals the format considered the case and permitted it.

Implementations SHOULD report the condition under the name `confidence_on_held`, in the family of `scope_wider_than_inputs` and `legacy_produced_by`. A named condition makes a future relaxation a one-word change rather than a renegotiation.

### D5. Syntheses are inferred by construction

A synthesis is derived from its inputs — that is what it is — so declaring the field on it would be redundant. It is implied rather than required, mirroring `source.harness`, which is mandatory on syntheses and optional on claims.

### D6. `method` becomes a closed vocabulary

`method: reconciliation` has existed since the first draft with no definition and no consumer. It is the right shape for the synthesis-side of this axis:

- `reconciliation` — the inputs disagreed about a fact; this settles it.
- `qualification` — the inputs are both true, in different contexts.
- `positions` — no evidence settles this; the synthesis names the positions and what would move either.

`positions` is what gives `unresolved` the vocabulary it currently lacks for "considered, and this is not the kind of question evidence closes". It also defuses the obvious worry about `held` becoming a dumping ground: marking a claim `held` does not exempt it from reconciliation. Two conflicting positions still surface as unsynthesised and still want a synthesis — one of a different kind. The label changes what the work is, not whether there is work.

## Risks / Trade-offs

- [**Terminology collision**] → `synthesis-rules` already contains "A synthesis's subject is explicit and never inferred", where "inferred" means derived-from-inputs in a completely different sense. Both readings are natural and they now sit two requirements apart. One of them should be reworded before this lands.
- [A mandatory field strains a stated principle] → "Backward compatibility by design… adoption does not require full implementation" is harder to say with a required field on every claim. The reader-lenient rule preserves the letter of it — old files stay readable, and a consumer ignoring the field still gets a valid claim — but the principle's wording deserves review rather than a quiet reinterpretation.
- [`held` becomes an escape hatch for unreconciled work] → Mitigated by D6 as above. It may also want the treatment `unresolved` got: a conventional usage that means *considered*, not *escaped*.
- [Three values will not fit every case] → Likely, at the edges. The guard is that the closure is derived from what settles a claim rather than from a category list, in the same way the three retraction kinds are the three joints of `claim → source → world`. A fourth value should have to name a fourth way a claim can come to be believed.
- [Scale of the break] → Largest change since the object model was fixed. It is why the v0.1 declaration question comes with it rather than after it.

## Open Questions

- **The evaluative synthesis.** A synthesis that reconciles two positions and concludes "given both, X is the better path" has an evaluative conclusion reached by argument. `inferred` with `method: positions` is the intended answer, on the grounds that the synthesis reasons *about* positions rather than asserting one — but if that is wrong, it is wrong in the direction of letting judgements launder themselves as reasoning, which is what this change exists to prevent. Unsettled deliberately.
- **May an `undeclared` claim carry confidence?** It already does, in every existing workspace. Reporting it as unverified is proposed here; forbidding it retroactively is not possible, and ignoring it entirely loses the signal.
- **Is `held` the right name?** `judged`, `valued`, and `position` were all considered. `held` reads well against "a position someone holds" and does not imply a verdict, but it is the least standard of the three terms.
- **v0.1 or v0.2.** Not a question this change can answer alone.
