## Why

Reviewing the applied `verifiable-provenance` round, the reference implementation identified a defect in it and declined to ship one requirement ([particulars-cli#3](https://github.com/nodelogicau/particulars-cli/issues/3)). The objection is correct.

The spec asks implementations to cross-check a declared retraction `kind` against observed source drift, and in particular to warn when `supersession` is declared against a document whose hash is unchanged, "since nothing moved to supersede the claim". But drift is a signal about the **source** joint of `claim → source → world`, while supersession is a declaration about the **world** joint. The check silently assumes the cited document is a *living* description of current state, and nothing in the format distinguishes a living document from a dated one.

The counter-example is the ordinary case rather than a corner. A claim sourced from an architecture decision record, an incident report, a dated release note, or a commit-pinned URL cites a document that is *supposed* to remain byte-identical while the world moves on. Retracting such a claim as `supersession` is exactly right, and the hash cannot have changed. Both the reference implementation's workspace and this repository's own contain many such claims — every claim written during the last week cites a commit-pinned blob URL — so the rule as written would warn on every honest supersession, forever. That is the cries-wolf failure the quote design was introduced to avoid.

Two smaller items from the same review are folded in, because they touch the same requirements and leaving them would mean two changes to one paragraph.

## What Changes

- **The supersession cross-check is removed.** Implementations report the observed drift state alongside the declared `kind` as fact, and leave the judgement to the reader — the line this specification takes for `scope_wider_than_inputs` and for conflict detection generally.
- **The sound inverse replaces it**: a `defect` declared against a document that *has* drifted is **unverifiable**, because the text the author is said to have misread is no longer the text a reviewer can read. That is a statement about what can be checked rather than an inference about intent, and it is the version that earns its noise.
- **Hash normalisation is pinned**: a document hash is taken over the document with CRLF sequences normalised to LF, and nothing else normalised. Trailing whitespace, Unicode form, and final newlines are left alone. Normalising the transport artefact prevents a Windows checkout reporting drift on every claim in a workspace; normalising anything further would blind the check to a class of real edit. This closes the question the previous round recorded in Status as open. **BREAKING** for any implementation that has already hashed raw bytes.
- **`document.uri` is renamed `document.ref`**, and may hold a URI or a path resolved against the workspace root. The dominant case for an agent is a repository-relative path, which is not a URI, and refusing one would push agents back to bare strings — worse provenance than the field exists to provide. **BREAKING**, and free today: the mapping form shipped on 2026-08-25 and no implementation has written one yet.

## Capabilities

### New Capabilities
<!-- none -->

### Modified Capabilities
- `retraction`: the cross-check requirement is replaced by one that reports drift as fact and names the unverifiable-defect case.
- `source-verification`: the structured reference takes `ref` in place of `uri` and admits workspace-relative paths; the hash gains its normalisation rule.

## Impact

- `README.md` — the retraction cross-check paragraph, the `document` mapping example and its field list, the drift section, and the Status entry that recorded normalisation as open.
- `openspec/specs/` — two capabilities modified, none added.
- `particulars-cli` — has stated it will implement `kind` and both drift signals regardless, and will not ship the cross-check as specified. This change makes the specification match that judgement. `ref` and the LF rule both land before it writes its first mapping.
- The specification's own examples all use remote URLs, which is why the repository-relative case went unnoticed when the mapping was designed. A repository-relative example is added so the pattern that gets copied is the one that is cheap to verify.
- **Deliberately out of scope**: two suggestions from the same review that improve `claim-evidential` rather than this round — that a writer should refuse `--confidence` alongside `evidential: held` rather than leaving it to a validator, and that findings appearing on nearly every object should be reported in summary rather than per object. Both are worth adopting; neither belongs in a change about drift.
