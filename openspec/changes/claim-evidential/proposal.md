## Why

Every DKF claim is an assertion of fact, because the format never considered any alternative. "The billing service listens on 8443", read from a config file, and "the microservices split was a mistake", held as a view, are the same object with different prose. A consumer cannot tell them apart, and neither can `conflict_detect`, `knowledge_publish`, or an agent composing an answer from forty recalled claims.

This matters more for DKF than it would for a note store, for two reasons. The format is written mostly by agents, and the highest-risk artifact an agent can produce is a fluent, well-formed judgement with nothing behind it — presented, because the format has no other register, as fact. And DKF took its structure from a dialectic that operates on positions and concepts, then quietly assumed its content would be factual: every synthesis is shaped as though reconciliation converges on a truth, and `unresolved` has no vocabulary for "considered, and this is not that kind of question".

There is a second, smaller hole underneath. `confidence` has existed since the first draft and **no requirement anywhere defines it**. Its only calibration lives in the reference implementation's agent guidance, which scores it evidentially — 0.9+ for something seen directly, 0.6–0.8 for inference. So the field means "how good is my evidence" by convention and nothing else, which leaves it meaningless on a claim that has no evidence to grade.

## What Changes

- **Claims carry a required `evidential`** with one of three values — `observed` (someone or something looked), `inferred` (derived by reasoning), `held` (a position; nothing external backs it). **There is no default.** **BREAKING**.
- **Readers accept its absence and report `undeclared`.** This is not a fourth value and not a synonym for `observed`; it means the claim predates the field and its warrant cannot now be established. Writers must declare; readers stay lenient, as they already do for legacy ids, legacy `produced-by`, and field order.
- **A `held` claim MUST NOT carry `confidence`**, reported as `confidence_on_held`. Confidence measures how likely a claim is to be wrong; a position is not wrong in the way a probability describes. This is the first mechanically enforceable rule in this area — every other signal in the format can only warn, because a machine cannot judge prose.
- **`confidence` gets a definition** for the first time: the inverse probability that the claim is mistaken, applicable to `observed` and `inferred` and undefined for `held`.
- **A synthesis is `inferred` by construction** and does not declare the field, in the same way it already requires `source.harness` where a claim does not.
- **`method` gains a closed vocabulary** — `reconciliation` (the inputs disagreed on a fact), `qualification` (both true in different contexts), `positions` (no evidence settles this; the synthesis names what is at stake). The field has existed since the first draft with no definition and no consumer.

## Capabilities

### New Capabilities
- `claim-evidential`: the evidential axis, the required-on-write and lenient-on-read rule, `undeclared`, and the definition of `confidence` including its exclusion from held claims.

### Modified Capabilities
- `synthesis-rules`: a synthesis is inferred by construction; `method` becomes a closed vocabulary.

## Impact

- `README.md` — `DCLAIM` gains a required field and the confidence definition; `DSYNTHESIS` gains the method vocabulary; Design Principles may need a sentence, since "a consumer that ignores the format entirely gets readable YAML" survives but "adoption does not require full implementation" is strained by a mandatory field.
- **Existing workspaces become `undeclared` permanently.** Claims are immutable, so there is no legal way to backfill — adding a `retracted` block is the only permitted modification to an existing file. The distinction ages out as new claims are written rather than being migrated, which is the only shape available to an append-only format and is arguably correct: backfilling would mean inventing warrants for claims nobody can now interrogate.
- **This forces the v0.1 question.** Every change since the object model was set has been additive or corrective. This one makes a field mandatory on the most common object in the format, and renegotiates what a claim is rather than how it serialises. It is a reasonable v0.2 opener, or the reason to declare v0.1 first.
- Interaction with the unapplied `verifiable-provenance` change: if that lands, `held` combined with `kind: defect` is incoherent — a position has no source to have misread — and changing one's mind is `supersession` under the reading that the claim was true-of-its-holder then. That constraint is deliberately not specified here, because the requirement it would modify does not yet exist in the baseline.
- `particulars-cli` — `claim assert` gains a required `--evidential`, `validate` gains `confidence_on_held` and an `undeclared` report, and its agent skill needs the calibration guidance rewritten, since today it tells agents to score confidence on every claim.
