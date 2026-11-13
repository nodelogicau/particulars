## 1. Spec

- [x] 1.1 Add `recall-entry-limit`: `entry_limit` for both modes, the four-tier selection order with recency within tiers, lineage-order output, `omitted` excluding filtered entries, and refusal of a non-positive cap
- [x] 1.2 Modify *Recall by query resolves to particulars, then recalls structurally* in `recall-query`: pass `entry_limit` through, keep matched entries ahead of the rest, and state that `limit` bounds particulars and `entry_limit` entries
- [x] 1.3 Modify *Each result says how it was resolved* in `recall-query`: ranking counts against the response before `entry_limit`, so the cap never changes which particulars appear or their order

## 2. README

- [x] 2.1 Update the `knowledge_recall` row in *MCP Server Tools*: add `entry_limit` to the signature and describe it and `omitted`
- [x] 2.2 In *Recall by query*, add a paragraph on the cap: what it keeps and why (`current`, then unsynthesised, then matched), why kept entries stay in lineage order, why `omitted` ignores filtered entries, and why there is no default
- [x] 2.3 In *Recall by query*, where `limit` and the order are described, say that the order is computed before `entry_limit` applies
- [x] 2.4 Add a Status entry: #38 point 1 is closed by `entry_limit`, tool behaviour with no format version, and point 2 (order and the flood of matches) stays open

## 3. Verify and follow up

- [x] 3.1 Run `openspec validate recall-entry-limit --strict` and fix any findings
- [ ] 3.2 Comment on #38 linking the change, and say that point 2 is still open
- [ ] 3.3 Open a particulars-cli issue for `entry_limit`, the selection order, `omitted`, and `limit` on recall by particular as a deprecated synonym, citing `internal/query/recall.go:166`
