## 1. Specification text

- [x] 1.1 Replace the closing sentence of the no-cascade paragraph in README.md so the warning is stated over effective scope on both sides rather than conditioned on promotion
- [x] 1.2 State in the same place that a synthesis MAY be wider than its inputs, with the reason (reconciling private evidence into a shareable conclusion is legitimate; no tool can judge whether prose discloses its sources)
- [x] 1.3 Name the condition `scope_wider_than_inputs` and say it is reported, not enforced
- [x] 1.4 State that the condition is computed from workspace state — evaluated by validation, by `synthesis_create`, and by `knowledge_publish` — because promotion can create or clear it without either file changing

## 2. Review and close out

- [x] 2.1 Verify each scenario in `specs/scope-promotion/spec.md` is answered by a normative sentence in README.md
- [x] 2.2 Confirm the MODIFIED requirement header matches the baseline exactly so archiving merges rather than duplicates
- [x] 2.3 Commit referencing #15
- [x] 2.4 Comment on #15 with the resolving text and close it
- [ ] 2.5 Note on particulars-cli#2 that the spec ratified `scope_wider_than_inputs` and that the effective-scope comparison is now specified
