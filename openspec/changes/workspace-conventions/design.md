## Context

The spec has never said anything normative about an MCP server beyond the tool names and signatures in the README table, which the reference implementation treats as the contract ("Tool names follow the DKF specification"). #23 asks for a step further: a file the workspace owns and a server behaviour that delivers it. The precedent is `.dkf` (resolve-v01-blockers D2): an additive file convention the reference implementation had already shipped, blessed because "the alternative is each implementation inventing a different one".

The review of #23 against the reference implementation (add-workspace-conventions, knowledge-not-catalogue) found five things to settle rather than copy: the default filename, what an invalid path does, what "inside the workspace" means, whether the cap is a maximum or a minimum, and where the register that motivated the issue actually belongs.

## Goals / Non-Goals

**Goals:**
- One filename and one reader behaviour, so a workspace's rules survive a change of tool.
- The three invariants of the format untouched: every object file interpretable alone, readers never consult configuration to interpret a file, readers lenient.
- The observed failure addressed where it happens — the tool surface — not only in a document some clients never see.

**Non-Goals:**
- Constraining or validating the document's content. It is prose for a model.
- Specifying when a server reads it (startup versus per request), or delivery to harnesses that read the repository — they read the file.
- `AGENTS.md` as the default (see D1); it remains a legitimate value for the key.
- A general MCP-server capability. Two requirements about a server do not justify one; if more accrue, they can move.

## Decisions

### D1. The default is `dkf.md`, the prose sibling of `dkf.yaml`

#23's own argument for a file over keys is that `dkf.yaml` stays configuration and the conventions are prose. Naming the file as the marker's sibling makes that split literal: anyone who knows what `dkf.yaml` is knows what `dkf.md` is, the walk-up that finds one finds the other, and no tool that predates DKF claims the name. The cost — the name says nothing to a human browsing the repository — is paid by the file's first line.

The deciding argument against any generic default is silent delivery. A workspace at a repository root with an aider `CONVENTIONS.md` would have coding conventions injected into every knowledge session from the day a server first started, with nobody having asked. A DKF-specific name can only exist because someone meant it.

*Alternatives:* `CONVENTIONS.md` (aider); `AGENTS.md` — the emerging cross-tool norm for exactly this kind of document, and its nested-file rule makes `knowledge/AGENTS.md` already addressed to agents working there, so a repo-reading harness delivers it with no DKF support at all. That is the right *value* for a workspace that is its own agent scope, and the README says so; as the default it fails the root-workspace case, where the repository's `AGENTS.md` is about the code. `WORKSPACE.md` (Bazel adjacency), `KNOWLEDGE.md` (reads as the knowledge itself), `TOPICS.md` (too narrow), `PARTICULARS.md` (names the implementation, not the format).

### D2. An invalid path is unset with a warning, and the check is lexical

The reference implementation fails config validation on an absolute or escaping `workspace.conventions`. The consequence is disproportionate and, worse, inconsistent across versions: a typo makes `recall` refuse the workspace on a newer tool while an older reader — which ignores the key, as `workspace-config` requires — opens it without comment. A validity rule that only some conformant readers enforce produces exactly the "holds under one tool, evaporates under the next" outcome the issue exists to prevent.

`base-uri` is the precedent for strictness and the reason it does not apply: a malformed base URI changes what identifiers get minted. A conventions path changes nothing structural, so it joins the lenient side — ignored, reported, never fatal — alongside the missing-but-configured file the issue already treats that way.

"Resolves inside the workspace" is stated as a check on the cleaned path: no absolute path, no leading `..` segment. A relative path that is a symlink to elsewhere passes. The reference implementation checks lexically; the spec should promise no more, and should say so, so that a second implementation does not add a `realpath` check and disagree about which workspaces are valid.

### D3. Delivery is SHOULD; the cap is a floor; the resource is MAY

SHOULD rather than MAY because a MAY gives a workspace author no guarantee, and the guarantee is the point of blessing the file at all. The order — after the generic guidance, under a heading naming the file — is pinned because a model should meet the format's rules before the workspace's refinements, and because the heading is what lets a model go and read the rest when the text is truncated.

A fixed cap in the spec would be an implementation number; no cap would leave an author with no portable budget. Stating it as a minimum — deliver at least the first 16 KiB untruncated, cut on a character boundary, say so and name the file — gives the author a budget they can rely on and lets a server deliver more. 16 KiB is the reference implementation's number, kept so that its behaviour is conformant on day one. The character-boundary rule exists because the reference implementation cuts bytes and can split a UTF-8 sequence.

The resource is MAY because the reference implementation's own follow-up notes several clients never surface `instructions` at all. A resource is the MCP channel a client can attach deliberately. It is not SHOULD because the spec should not require a second delivery path before one implementation has needed it.

### D4. The document constrains nothing but the model

Two sentences guard the invariants. No reader or validator derives behaviour from the document: `defaults` already has "readers SHALL NOT consult", and this is stronger — nothing consults it, only a model reads it. And it cannot relax a requirement of the specification: a workspace whose `dkf.md` says "confidence on held claims is fine here" has written a wish, not a rule, and an implementation that refuses the claim is conformant.

### D5. The register goes in the tool table

knowledge-not-catalogue's finding is that the catalogue failure happens at one moment — a model holding a document chooses `particular_id` and `content` — and the only text guaranteed in context then is the tool and parameter descriptions. The spec owns those, via the README table. So the register is stated there, for `claim_assert` and `particular_define`, as a presence requirement: the subject is the thing in the world, never the document or feed it was read in; what was read goes in `source.document`; `particular_define`'s examples of global URIs are identities, not reading matter. Exact wording is the implementation's.

This also corrects the motivation the spec gives for the file. The file is for what only the workspace can say — vocabulary, retired tags, ingestion policy — not for the generic register, which the format can teach on every surface.

### D6. What the format models does not go in prose

#23 lists "who its authors are and which URI each one uses" as conventions content. The format already models that: authors are particulars resolved by label or alias, `defaults.source.author` supplies the default, and merge records join identities. A prose table of the same facts drifts from the structural one and cannot be reconciled by any tool. A non-normative sentence in the README steers: conventions are for what the format does not model. Not a requirement, because the spec does not constrain the content (D4).

## Risks / Trade-offs

- [The reference implementation's shipped default changes from `CONVENTIONS.md` to `dkf.md`] → Additive at v0.12.0, one minor version old, no workspace known to rely on the default (the dogfood workspace names its file). A rename in the CLI, tracked on `particulars-cli#7`.
- [Two files at the root that start with `dkf`] → Deliberate; the pairing is the point.
- [SHOULD on delivery lets a conformant server deliver nothing] → It does, and reports nothing to the author either. Accepted: a MUST on a server behaviour for a MAY file is disproportionate, and `particulars workspace`-style reporting is an implementation courtesy the spec does not need to require.
- [A floor invites authors to write exactly 16 KiB] → The README advises brevity: the text rides in every session's context.
- [Lexical path check passes a symlink to outside the workspace] → The document is prose delivered to a model, not executed; the workspace owner chose the link. Stated, not defended.

## Migration Plan

Additive. No file, key, or reader behaviour changes; workspaces without the file or key behave exactly as today. The reference implementation renames its default and relaxes its validation on its next release.

## Open Questions

- None.
