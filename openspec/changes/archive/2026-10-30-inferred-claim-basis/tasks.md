## 1. README

- [x] 1.1 In `DCLAIM`, add an `inferred` example claim carrying `basis`, placed after `evidential` and before `confidence` so the canonical order is shown.
- [x] 1.2 In *What backs a claim*, say that an inferred claim's basis is its evidence, the way `source.document` is an observed claim's. Cover:
  - only `inferred` claims carry a basis, and `basis_not_inferred` is read but fails validation;
  - basis ids must exist, and may be retracted;
  - other formats are reached through an `observed` claim about them;
  - a basis-less inferred claim is valid and reported as `inferred_without_basis`.
- [x] 1.3 Add a short passage on induction: a rule of thumb is an inferred claim whose basis is its instances, a counterexample is a `qualification` synthesis, and instance counts and dates are derived. Say why induction isn't a synthesis method: it would become `current`.
- [x] 1.4 In *Conflict semantics*, update `unsynthesised` (transitive inputs follow `inputs` only) and `stale` (claims too, through `inputs` and `basis`). Add the consequence that citing in a basis is not synthesis, and how a stale inferred claim leaves the set.
- [x] 1.5 In the tool tables:
  - `claim_assert` takes `basis`, refuses it unless `evidential` is `inferred`, and warns on an inferred claim without one;
  - `lineage_trace` follows `basis` and labels those edges `basis`.
- [x] 1.6 In *Findings and facts* and the scope and derived-disclosure text, add `basis_not_inferred` and dangling basis ids as findings about an object, and `inferred_without_basis` as a fact about the corpus. Say that `scope_wider_than_inputs` and no-cascade cover a basis.
- [x] 1.7 In the index section, say that claim entries carrying a basis carry `basis`.

## 2. Delta specs

- [x] 2.1 Confirm each MODIFIED block is the main-spec requirement verbatim apart from the intended edits and added scenarios, by diffing against `openspec/specs/<capability>/spec.md`.
- [x] 2.2 Run `openspec validate inferred-claim-basis --strict` and fix anything it reports.

## 3. Close out

- [x] 3.1 Verify each scenario in the delta specs is answered by a normative sentence in README.md.
- [x] 3.2 Open an issue on particulars-cli for the implementation:
  - `claim assert --basis` and the MCP parameter;
  - write-time refusal and warning;
  - `basis_not_inferred`, dangling basis ids and `inferred_without_basis` in validate;
  - conflict sets and lineage following `basis`;
  - index entries carrying `basis`;
  - the skill text.
- [x] 3.3 Comment on #42 linking the change, and close it when the change is archived. Commented 2026-10-30; closing happens at archive.
- [x] 3.4 Update Forgetting §9 when the change is archived: the rule-to-episodes link becomes a basis, and the draft note on induction is settled. Done 2026-10-30 in nodelogicau/forgetting 634ff1c.
- [x] 3.5 Record in particulars-knowledge when the change is merged: an inferred claim can now name its basis, and staleness reaches inferred claims through it (#42). Recorded 2026-10-30 as clm_01a18c55-dbc2-70bb-b261-1df6d26a46b2, merged in particulars-knowledge#46.
