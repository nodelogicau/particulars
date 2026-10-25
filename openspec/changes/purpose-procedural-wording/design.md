## Context

*Purpose*'s third paragraph currently reads:

> **Episodic** and **procedural** memory are outside the format. An event can be a particular and have claims made about it, but a log of what happened is not DKF's job. Neither is how an agent does things: that lives in skills and prompts, and a workspace's [conventions document](#dkfmd) addresses an agent without constraining anything. Either could get a specification of its own.

The `format-purpose` requirement that governs it says "how an agent does things belongs to skills and prompts", and its procedure scenario asks whether DKF stores "how an agent should perform a task". So the spec, not only the prose, defines procedural memory as the agent's.

The [Forgetting](https://github.com/nodelogicau/forgetting) whitepaper (section 8) now treats procedural memory from the person's side: habit as where an intention ends up, a habit's breakdown as outliving its reason, rare procedures as mostly episodic, and agent skills as delegation, the harness's own procedural memory.

## Goals / Non-Goals

**Goals:**
- Procedural memory is described by what it is for a person, as every other memory type in *Purpose* already is.
- A reader who asks where an agent's know-how lives still gets an answer: skill files, prompts, and the conventions document.
- *Purpose* points to the whitepaper for the fuller argument, and nothing in it contradicts the whitepaper.

**Non-Goals:**
- Any change to the episodic sentence, the intentions paragraph, or the first paragraph.
- Arguing the whitepaper's case in the README. *Purpose* stays at three short paragraphs.
- Deciding whether a procedural or episodic specification should exist. The scope statement still leaves both open.
- intentions#30, on representing a recurring intention that has become habit.

## Decisions

### D1. Draft text

The wording will be refined on apply. This draft fixes what the paragraph claims:

> **Episodic** and **procedural** memory are outside the format. An event can be a particular and have claims made about it, but a log of what happened is not DKF's job. Neither is know-how, the habits and practised skills a person exercises rather than recalls. A harness's own know-how lives in skill files and prompts, and a workspace's [conventions document](#dkfmd) addresses an agent without constraining anything. Either memory could get a specification of its own. Why the family models memory as several kinds, and what each is for, is argued in [Forgetting](https://github.com/nodelogicau/forgetting).

*Why "know-how".* It is the plain-language name for procedural memory, it is about a person by default, and it lets the next sentence say "a harness's own know-how" without redefining anything.

*Why "skill files" rather than "skills".* "Skills" is ambiguous here: a person's practised skills and an agent's `SKILL.md` are the two things the paragraph now separates.

*Why keep the harness sentence at all.* Readers from agent memory will ask where an agent's procedures go, and the conventions document is the one thing in this specification that addresses procedure. Dropping it would leave that question unanswered.

### D2. The whitepaper link goes in *Purpose* and in *References*

*Purpose* links it in one closing sentence, because it is the fuller version of exactly this section. *References* gets an entry under **Ecosystem**, beside intentions, since it belongs to the family rather than to either format.

*Alternative considered:* link from *References* only. Rejected, because a reader who wants the argument behind the scope statement is reading *Purpose*, not *References*.

### D3. The spec changes by MODIFIED, not ADDED

The existing requirement already owns the scope statement and its procedure scenario. Rewording it in place keeps one requirement for scope, rather than a second requirement that partly contradicts the first.

## Risks / Trade-offs

- [The whitepaper is a draft, and *Purpose* would link to an evolving document] → The link is to the repository, not to a section, and the sentence claims only that the argument is made there.
- [Describing human know-how in a format for agents reads as scope creep] → The paragraph still says know-how is outside the format. It changes what is excluded, not what is included.
- [*Purpose* grows past three short paragraphs] → One sentence is replaced and one added; the paragraph count is unchanged.
