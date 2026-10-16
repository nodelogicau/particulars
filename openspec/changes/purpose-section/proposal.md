## Why

The README says how DKF works and never says what it is for. *The Problem* describes siloed memory and contradiction treated as error. *The Approach* describes the dialectic. The one sentence that places the format, "intentions is the prospective layer, what a person means to do, and this is the retrospective one, what is known", sits in *References*, about eighteen hundred lines in. A reader comparing DKF with an agent-memory system has to infer the scope, and the obvious inference is wrong. Most readers will guess "a memory format" and expect it to hold conversation logs, events and skills.

The scope is narrower, and the narrowness is a strength. DKF is semantic memory: claims about things in the world, reconciled into a current belief. What no other memory system does is keep, on every claim, who asserted it, through which harness, from what, and how it is backed. Psychology calls the usual loss of that information source amnesia. Provenance is the format's distinguishing value, and the dialectic is what provenance makes possible: a contradiction can only be reconciled if both sides still say where they came from. The README presents these the other way round, with dialectic first and provenance as a consequence, which undersells what is unique.

## What Changes

- **A *Purpose* section** between *The Problem* and *The Approach*, of two or three short paragraphs:
  - DKF is **semantic memory that keeps its provenance**. Provenance is named as what sets the format apart, and the dialectic as what provenance makes possible.
  - DKF is the **retrospective** layer, what is known, beside intentions as the **prospective** layer, what a person means to do. The two are coupled loosely, through the URIs of the particulars they share. Each may cite the other informally, and neither validates the other.
  - **Episodic and procedural memory are out of scope.** An event can be a particular and have claims made about it, but a log of episodes is not the format's job. How an agent does things belongs to skills and prompts; a workspace's conventions document addresses an agent but constrains nothing. Either may be addressed by a separate specification later.
- ***The Approach* opens by connecting to *Purpose***, so the dialectic reads as what provenance makes possible. Its text otherwise stays as it is.
- ***References* keeps its intentions entry**, shortened to the citation, since *Purpose* now states the relationship.

Not **BREAKING**: prose only, with no normative change to any object, field, tool or rule.

## Capabilities

### New Capabilities

- `format-purpose`: what the specification states about its own purpose and scope. It says DKF is semantic memory that keeps its provenance, that it is the retrospective layer beside intentions with coupling through shared URIs only, and that episodic and procedural memory are outside the format.

### Modified Capabilities

None.

## Impact

- `README.md`: new *Purpose* section; an opening sentence in *The Approach*; the intentions entry in *References* shortened.
- particulars.fyi: the landing page leads with "Knowledge that doesn't go stale" and the dialectic triad (`landing-page`). This change doesn't alter it. Whether the site should lead with provenance is a separate decision.
- intentions: no change needed. Its README already says a retrospective account of what happened "is not this format's job", and that a DKF claim may cite its objects, which is the relationship *Purpose* describes from this side.
- The memory-types whitepaper discussed alongside this change is not part of it. *Purpose* is written so the whitepaper can extend it without contradicting it.
- Dogfood: a claim in particulars-knowledge recording DKF's purpose as stated, and that provenance, not the dialectic, was identified as the distinguishing value.
