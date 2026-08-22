## 1. Canonical serialisation (#11)

- [x] 1.1 Add a "Field order" note under Core Object Types: the order shown per type is canonical; writers SHOULD emit it, readers MUST accept any order, extension fields go last
- [x] 1.2 Correct the merge-record prose in README.md so `reason` sits between `uris` and `source`, matching the existing example
- [x] 1.3 In Trust and Provenance, define "canonical object" as the object in canonical field order minus `retracted` and `signature`, and note the writer-SHOULD becomes a MUST for signed objects
- [x] 1.4 Update the Status section: field order is settled; the signed payload's serialisation basis remains open

## 2. Workspace discovery (#12)

- [x] 2.1 Add `.dkf` to the File Layout with the `repo/.dkf → knowledge/` example
- [x] 2.2 Document the discovery algorithm in the `dkf.yaml` section: per ancestor, `dkf.yaml` wins, else `.dkf` redirects; no chaining; target must contain `dkf.yaml`; error names both paths
- [x] 2.3 State that `.dkf` is not a workspace marker, carries no configuration, and that a workspace stays discoverable from inside without one
- [x] 2.4 State discovery precedence: explicit workspace argument, then environment variable, then walk-up

## 3. Synthesis subject (#13)

- [x] 3.1 Change the tool table to `synthesis_create(particular_id, content, inputs[], unresolved, source)` and note `particular_id` accepts id, URI, label, or alias
- [x] 3.2 In the DSYNTHESIS section, state that every claim and synthesis carries exactly one explicit `subject` and that implementations MUST NOT infer it from inputs
- [x] 3.3 Add the cross-reference from the cross-particular-inputs paragraph explaining why inference is unsafe

## 4. Scope promotion (#14)

- [x] 4.1 Add a "Promotion records" subsection after Merge records with the `publishes/pub_….yaml` example in canonical field order
- [x] 4.2 Define effective scope: widest non-retracted promotion covering the object, else its asserted `context.scope`, with `personal` < `organisation` < `public`
- [x] 4.3 State the widen-only rule and its rationale (a naive consumer under-shares rather than leaks); narrowing is retraction
- [x] 4.4 State that promotion does not cascade to a synthesis's inputs, and that implementations SHOULD warn when a promoted synthesis has narrower inputs
- [x] 4.5 State that promotions are retractable, and that retraction ends future feed eligibility but cannot recall what was already fetched
- [x] 4.6 Change the tool table to `knowledge_publish(claim_ids[], scope, source, reason?)`
- [x] 4.7 Add `/publishes/` to the File Layout and a publish entry to the `index.yaml` example
- [x] 4.8 Rewrite "Scope isolation" under Trust and Provenance in terms of effective scope
- [x] 4.9 Update the DCLAIM `context` paragraph to name the file's value the *asserted* scope

## 5. Knock-ons

- [x] 5.1 Add `pub` to the identifier prefix table and to the lenient read regex in the Identifiers section
- [x] 5.2 Reword the "Minimal spec, layered implementation" principle to "three knowledge objects plus records (retraction, merge, publish)"
- [x] 5.3 Note in the Conflict semantics section that promotion records are not knowledge and affect no conflict set
- [x] 5.4 Add `/knowledge/publishes/` to the `.well-known` feeds example if it aids crawlers, or state explicitly that promotions are not served

## 6. Review and close out

- [x] 6.1 Read README.md end-to-end: every example in canonical field order, both changed tool signatures consistent, no remaining claim that scope is decidable from the claim file alone
- [x] 6.2 Verify each scenario in `openspec/changes/resolve-v01-blockers/specs/` is answered by a normative sentence in README.md
- [x] 6.3 Confirm the MODIFIED requirement headers match the existing spec headers exactly, so archiving merges rather than duplicates
- [x] 6.4 Commit referencing #11–#14; comment on each issue with the resolving section and close it
- [x] 6.5 Open a follow-up issue on particulars-cli for `pub_` records, effective-scope filtering in the feed and Graph export, `particular_id` on MCP `synthesis_create`, and `source` on `knowledge_publish`
