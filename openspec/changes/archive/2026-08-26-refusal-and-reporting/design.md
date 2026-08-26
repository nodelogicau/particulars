## Context

Both halves were decided on particulars-cli#4 through implementation experience rather than argument — including the implementer correcting their own earlier position twice: their `validate` half-complied with their own principle (legacy warnings listed per object), and their original "the warning is the only way anyone learns it is there" argued for the signal's existence, not its multiplicity.

Posted on #4 before applying, per the standing ordering.

## Goals / Non-Goals

**Goals:** the one enforceable rule fires where the mistake is made; actionable warnings stay visible in real workspaces.
**Non-Goals:** exit codes, JSON output shapes, severity taxonomies, or any new condition.

## Decisions

### D1. Three roles, three verbs

Writers **refuse**, validators **report and fail**, readers **read regardless**. The first rule where write-side and read-side genuinely differ, so the spec says all three rather than leaving "reject" to cover them ambiguously. The reader clause is the load-bearing one in an append-only format: a file that cannot be fixed must never be unreadable, or the rule converts a past mistake into permanent data loss.

### D2. Nature, not proportion

A proportion trigger ("aggregate when many") renders the same fact differently in different workspaces and needs an arbitrary threshold. The real division: a finding about an object has an action attached (fix the quote, review the synthesis, retract); a fact about the corpus has none per object — it is permanent, unactionable at the object level, and uncleared by construction. Six legacy lines are wallpaper too; they are just a small wall. The classification follows from language the spec already uses — a condition described as "unverified rather than invalid" or "an observation" was always a corpus fact.

### D3. Message on the aggregate line only when uniform

Fell out of the reference implementation: legacy markers say the same sentence on every file, so the aggregate line reads as a sentence; `unverified_document` varies by cause, and gluing the first message onto a count attributes one object's reason to the rest. Count always; message when uniform.

## Risks / Trade-offs

- [Classifying conditions in the spec couples it to reporting, which is arguably ergonomics] → The counterargument that won: the format's entire recent design load rests on warnings being read, which makes legibility load-bearing rather than cosmetic. The spec names the distinction once and stops; rendering mechanics beyond the one rule stay with implementations.
- [A future condition may straddle the line] → The test is whether an object-level action exists. If genuinely both, it is a finding; over-listing errs toward visibility.
