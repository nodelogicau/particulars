## Context

The README's opening runs *The Problem*, then *The Approach*, then *Core Object Types*. *The Problem* ends on contradiction ("current formats treat contradiction as an error to eliminate rather than signal to preserve"). *The Approach* gives the dialectic and closes on "records the process by which knowledge was formed — making it portable, inspectable, and trustworthy". Scope and relationship to intentions appear only in *References*. intentions' README states its side: what actually happened "is not this format's job", and "a DKF claim may cite any object here by id and version, and that is the whole of the relationship". Its `reference` field is an informal pointer to a DKF claim that validation never resolves.

## Goals / Non-Goals

**Goals:**
- A reader learns, before any mechanism, what DKF is for and what it is not for.
- Provenance is presented as the distinguishing value, with the dialectic as what it makes possible.
- The intentions relationship is stated accurately: coupled through shared URIs, with informal citation either way and nothing resolved.
- Episodic and procedural memory are named as out of scope without ruling out a later specification.

**Non-Goals:**
- The memory-types whitepaper, and any treatment of BDI, consolidation or source monitoring beyond a phrase.
- The landing page's tagline or hero.
- Any normative change. *Purpose* adds no MUST, and no implementation or validator behaviour depends on it.

## Decisions

### D1. Placement: its own section between *The Problem* and *The Approach*

*The Problem* says what is wrong, *Purpose* says what DKF is for, and *The Approach* says how. *Purpose* comes before *The Approach* so the mechanism arrives already justified.

*Alternative considered:* rewrite the last paragraph of *The Problem* to lead with provenance. Rejected for this change. *The Problem* is accurate as written; missing provenance is one of the gaps it lists. Changing it would widen the change from adding a section to rewriting the pitch.

### D2. Draft text

The wording will be refined on apply. This draft fixes the claims each paragraph makes:

> ## Purpose
>
> DKF is **semantic memory that keeps its provenance**: what is believed about things in the world, where every claim still says who asserted it, through which harness, from what, and how it is backed. That is what sets it apart. Memory usually forgets where it learned something, and a belief whose source is gone can only be overwritten, not weighed. Because DKF keeps the source, a contradiction is evidence on both sides, and the dialectic below is how it is reconciled.
>
> It is the **retrospective** layer, what is known. [intentions](https://github.com/nodelogicau/intentions) is the **prospective** one, what a person means to do. The two are coupled only loosely, through the URIs of the particulars they share. A claim may cite an intention and an intention may point at a claim, but neither format validates the other.
>
> **Episodic** and **procedural** memory are outside the format. An event can be a particular and have claims made about it, but a log of what happened is not DKF's job. Neither is how an agent does things: that lives in skills and prompts, and a workspace's [conventions document](#dkfmd) addresses an agent without constraining anything. Either may get a specification of its own.

*Why "semantic memory" by name.* It is the term readers from agent memory and from psychology share, and it says at once what is excluded.

*Why name source amnesia only implicitly* ("memory usually forgets where it learned something"). The term is precise but sends readers to a glossary. The whitepaper can name it.

### D3. *The Approach* gets one bridging clause, not a rewrite

Its first sentence becomes: "Keeping provenance is what lets DKF draw on the structure of Hegelian dialectic: …". Everything after stays as it is.

### D4. *References* keeps the link, not the explanation

The intentions entry becomes "the format that composes with this one for the prospective layer — see [Purpose](#purpose)". The References section exists to name sources and what they back, and *Purpose* now carries the explanation.

### D5. A `format-purpose` capability, stated as what the specification says

Like the requirement in `agent-guidance` that the specification "SHALL note" where structural facts belong, the requirements say what the README states, with scenarios a reviewer can check against the text. This gives the scope a spec home that a later episodic or procedural specification can modify.

## Risks / Trade-offs

- [Naming episodic memory out of scope looks like it contradicts intentions, which sends "what actually happened" to DKF claims] → It doesn't. A claim about an event-particular, citing the intention it fulfilled, is a semantic fact about that event. *Purpose* says so ("an event can be a particular"). What is out of scope is a log of episodes, and the whitepaper is where that boundary gets argued in full.
- [Provenance-first framing on the README and dialectic-first framing on particulars.fyi diverge] → Accepted for now and listed under Impact. The site is a separate decision.
- [*Purpose* grows into a manifesto] → Capped at three short paragraphs. Anything more belongs in the whitepaper.

## Open Questions

- Should particulars.fyi follow with a provenance-led section? This is deferred to a decision about the site.
