## Context

A review round on a change that has been applied and archived but not yet implemented. The reviewer traced the code paths the CLI would need and read the spec against its own criteria; the five findings are all in the text, none in the model. Two of them (#17, #19) alter behaviour an implementation would ship, so they are settled here rather than left to the implementer. The others are a missing sentence (#18), a type error (#20), and a compatibility gap this change opened without noticing (#21), plus one open question from the previous design that the review answered.

The same three constraints as before govern it: writers strict, readers lenient; a field earns its place only if a process needs it; claims are immutable. The third is what makes #18 decisive and #19 necessary.

## Goals / Non-Goals

**Goals:**
- Settle the two behavioural questions — what a writer refuses, and how the two author conditions are reported — so `particulars-cli#7` can proceed.
- Fix the text where it was wrong or incomplete, without reopening the decisions that were reviewed and held.
- Close the index compatibility gap for this and every future MAY field.

**Non-Goals:**
- Reopening D2 (URI over id), D3 (no reportative evidential), D6 (no scope on particulars). Reviewed and held.
- A `document.author` on syntheses, DID binding, `kind`, particular scope, the feed-inputs question. Still deferred.
- The reference implementation's own defects surfaced by the review (the MCP document mapping still says `uri`; URI resolution does not yet go through merge classes). Implementation facts, tracked on #7.

## Decisions

### D1. Both author conditions are corpus facts (#17)

The previous design's D5 split them — ambiguity a per-object finding, unresolved an aggregate fact — on the grounds that the action "add an alias, or merge" clears ambiguity. It does; so does "define the particular" clear an unresolved name. Neither action is at the object, and the spec's criterion is whether one is. D5 answered a different question (is there *an* action?) and got the classification wrong.

The corrected rule is also the more useful one. An aggregate line carries a message when it is uniform across the group, and for ambiguity it always is: the candidates are a property of the name, not the object.

```
  before   172 × "clm_…: author 'ben' is ambiguous between par_A and par_B"
  after    1   × "172 objects: author 'ben' is ambiguous between par_A and par_B"
```

The criterion's own sentence has to move with it. "Cannot be cleared, because clearing it would mean rewriting an immutable file" was true of every corpus fact until now; these two clear at the workspace. The general form is *cannot be cleared at any object*, which covers both reasons: the file is immutable, or the fix is elsewhere and clears every occurrence at once. The finding/fact test itself is unchanged.

### D2. The freeze argument goes into D2 and the README (#18)

Stated as the reviewer put it, because the argument is theirs and it is right:

> Writing the resolved reference freezes a resolution that was unambiguous when the claim was written. Define a second `ben` next year and a claim written as `https://github.com/benfortuna` is still Ben's; a claim that kept the bare name is ambiguous from that day on, and being immutable stays so until an alias is removed or a merge is written.

This is the argument that answers "why write anything at all, names resolve at read time" — and it composes with the existing one: freezing beats the name, and the URI beats the id because an id freezes only inside the workspace. No requirement changes; the *Writers prefer the URI* requirement already says what to write.

### D3. The writer is strict where it can be, and lenient only for defaults (#19)

The full table, which the README carries in prose:

```
  author given as       matches   writer
  ──────────────────────────────────────────────────────────────
  par_ id               0         REFUSE — nobody is called par_01a0…
  par_ id               1         writes the URI
  URI                   0         writes it unchanged — someone not defined
                                  here; the right identity, not an error
  URI                   1         writes it unchanged
  name, explicit        0         unchanged — a person not yet defined
  name, explicit        1         writes the URI
  name, explicit        >1        REFUSE, listing the candidates
  name, from defaults   0         unchanged
  name, from defaults   1         writes the URI
  name, from defaults   >1        unchanged; reported in aggregate (D1)
```

Two of these are new refusals and one is a case the review did not raise. The unresolved-URI row matters because it is the cross-workspace case D2 exists for: a claim authored by an ORCID this workspace has never defined is exactly right, and refusing it would make the URI form unusable until every author has a local particular.

*Why defaults fall through:* an ambiguous default fails every write in the workspace until someone edits an alias. The write is not the place to discover that, and the aggregate report (D1) is. *Why explicit names do not:* the caller chose the name and can choose a URI instead; refusing with candidates is the same behaviour subject resolution has today. One consequence to state in the skill rather than the spec: an agent that passes `author: ben` explicitly on every call, copying the default, will be refused the day a second `ben` exists. That is correct — pass the author only when it differs from the default.

### D4. `relations` is a set (#20)

An object whose `source.author` and `source.document.author` both resolve into the queried class matches both relations. A single label would either pick — the guessing forbidden everywhere else — or drop one, losing what "never collapsed" exists to keep. `relations: [asserted, reported]`; a result carries one or both, never neither.

### D5. A drift check tolerates what the committed index could not have known (#21)

Issue #16 protected an older tool from a newer workspace: unknown entry *types* survive a rebuild and do not count as drift. This change created the mirror case — a newer tool against an older index — and did not protect it: the first tool to write `author` into entries would regenerate an index that differs from every committed one and fail CI on workspaces that changed nothing.

The rule: a drift check SHALL NOT report, as a difference, a field marked MAY that is absent from the committed index. A MAY field present on both sides with different values is still drift; a missing or extra entry is still drift. This is the local form of a tolerance the README already grants remote consumers — the index is "potentially lagging the files" — and it is generic, so the next MAY field costs nothing.

*Alternatives:* require a rebuild on upgrade (honest, and every upgrade turns CI red once per workspace); compare baseline fields only (too weak — `scope` and `retracted` are MAY fields whose staleness the check exists to catch).

### D6. A person's particular is never minted as a side effect

The previous design left "whether `init` should mint the author's particular" to implementations. The review answered it: a URN-minted person gives every subsequent claim `urn:dkf:<ws>:ben` where it had `ben` — opaque, and with no cross-workspace identity, since the URN is workspace-local by construction. The value of an author URI is entirely in its being chosen. So: implementations SHALL NOT define a person's particular as a side effect of `init` or of writing an object; it is defined deliberately, with the URI the person chooses, and the writer rule's "written unchanged" path is what carries the name until then.

## Risks / Trade-offs

- [Two new write-time refusals could break an agent loop that passes `--author` reflexively] → Only the explicit-ambiguous case is reachable that way, only once a second particular shares the alias, and the error lists the candidates. The skill says when to pass an author at all.
- [Aggregating ambiguity hides which objects are affected] → The existing rule already requires that an aggregate be expandable to its object list. Nothing is hidden, it is folded.
- [MAY-field tolerance in the drift check lets a stale index pass when the only change is a new field] → By construction that index is behind, not wrong: readers never depend on a MAY field being present. A rebuild fixes it whenever someone next touches the workspace.
- [Refusing an unknown `par_` id while accepting an unknown URI looks inconsistent] → It is the same asymmetry as `subject`: an id is a promise of local existence, a URI is not.

## Migration Plan

Text only in this repository. For implementations: `author_ambiguous` and `author_unresolved` both on the aggregation whitelist; two refusals at the write call sites; `relations` as a list in recall output; the drift check gains a MAY-field allowance. No file changes shape; no existing workspace fails validation.

## Open Questions

- Whether the aggregate ambiguity line should also appear at *write* time for the default-author case, so the first person to hit it learns why their claims carry a bare name. Probably yes as a warning on the write; left to implementations.
- None of the previously deferred items moves.
