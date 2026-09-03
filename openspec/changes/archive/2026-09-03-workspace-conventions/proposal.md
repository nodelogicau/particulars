## Why

`workspace-config` defines what `dkf.yaml` carries — identity, base URI, writer defaults — and nothing else in a workspace speaks to an agent. The generic discipline (recall before you assert, one falsifiable statement per claim, the subject is the world) travels with the tool; a workspace's **own** register — which topic facets exist, which tags were retired, that this workspace reads feeds and never makes a feed a subject — has no defined home and no defined route to a model. The reference implementation shipped one in v0.12.0 (`CONVENTIONS.md`, or the file named by `workspace.conventions`, appended to the MCP `initialize` instructions) and raised #23 asking the spec to bless it, on the argument that settled `.dkf`: the filename is the contract, and the alternative is each implementation inventing a different one, so a workspace's rules hold under one tool and evaporate under the next with no visible difference in the files.

The observed failure behind #23 — one model extracting knowledge from a feed, another recording the *catalogue* — is a register failure at the moment of choosing a subject. The reference implementation's follow-up found the reliable lever for that is the tool descriptions, the one text guaranteed in context at that moment, and demoted the conventions file to the per-workspace escalation. The spec should do both: pin the register in the tool table, since tool descriptions follow the spec, and bless the file for what only a workspace can say.

## What Changes

- **A workspace MAY carry a conventions document for agents**: `dkf.md` at the workspace root by default, or the file named by `workspace.conventions` in `dkf.yaml`, a relative path inside the workspace. It is prose addressed to agents; the specification does not constrain its content, no reader or validator derives behaviour from it, and it cannot relax any requirement of the specification. The default is `dkf.md` rather than the reference implementation's `CONVENTIONS.md`: a DKF-specific name can only exist because someone meant it, where a generic name (`CONVENTIONS.md` is aider's coding-conventions file) gets a pre-existing file delivered silently the day a server first starts.
- **An invalid `workspace.conventions` is treated as unset, with a warning.** The reference implementation fails config validation on an absolute or escaping path, which makes the workspace unopenable for a newer tool while an older reader that ignores the key opens it — precisely the one-tool/next-tool inconsistency #23 is trying to prevent. `base-uri` is strict because it affects identity; conventions affect nothing structural. The path check is lexical, on the cleaned path, so implementations agree and the spec promises no more than they deliver.
- **An MCP server bound to the workspace SHOULD deliver the document** in its `initialize` instructions after its generic guidance, under a heading naming the file; any prompt it offers carrying its discipline SHOULD carry the same text; it MAY also expose the file as a resource, since some clients never surface instructions. A configured file that cannot be read is a warning, never a startup failure. The cap is a **floor, not a ceiling**: an implementation that truncates SHALL deliver at least the first 16 KiB, SHALL cut on a character boundary, and SHALL say it truncated and name the file — a portable budget for the author without fixing an implementation number as the maximum.
- **The tool table pins the register.** `claim_assert` and `particular_define` state that the subject is the thing in the world the fact is about, never the document or feed it was read in, and that what was read belongs in `source.document`. Presence, not wording, is the requirement.
- **A non-normative steer on content**: what the format models structurally — authors as particulars, topics on the index — does not belong in prose that would drift from it; conventions are for what the format does not model.

Not **BREAKING**: no file, key, or reader behaviour changes; readers that predate the key ignore it, as `workspace-config` already requires.

## Capabilities

### New Capabilities
- `agent-guidance`: what a workspace and the tool surface say to an agent — the optional conventions document (name, key, path rule, non-effect on readers), its delivery by an MCP server (instructions, prompt, resource, the floor and the truncation note, failure as warning), and the register the tool table teaches.

### Modified Capabilities
- `workspace-config`: `workspace.conventions` joins the MAY keys of `dkf.yaml`, with its validity rule and the unset-with-warning behaviour for an invalid value.

## Impact

- `README.md` — File Layout: `dkf.md` in the tree and a `### dkf.md` subsection after `dkf.yaml`; the `dkf.yaml` example gains `conventions:`. MCP Server Tools: a delivery paragraph, and the `claim_assert` and `particular_define` rows carry the register.
- **Closes #23**, choosing a different filename than proposed and answering its three explicit openings (filename, cap, MAY vs SHOULD).
- `particulars-cli` — default renamed to `dkf.md`; invalid `workspace.conventions` becomes a warning rather than a config error; truncation on a character boundary; optionally the file as an MCP resource. To be added to `particulars-cli#7`'s list. The dogfood news workspace names its file explicitly and is unaffected.
