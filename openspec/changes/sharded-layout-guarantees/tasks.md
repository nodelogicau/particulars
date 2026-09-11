## 1. Which operation guarantees what, in the README

- [x] 1.1 In *`index.yaml`*, in the drift-check paragraph, say what a matching count guarantees — no file arrived in that month, so no late mint — and that it says nothing about retractions, which change no count; name `validate` as the operation that regenerates every sealed month's `retracted` list from the files it already parses and compares it with the segment
- [x] 1.2 In *`index.yaml`*, in the cache-forever paragraph, make "a workspace that validates" carry both halves: no late mint by the count, no late retraction by validation's comparison
- [x] 1.3 In *Sharding*, replace the far-future validator sentence's reason with the asymmetry of consequence: a validator two months slow fails a healthy workspace once, on the machine that is broken, and that is the better error than accepting an id that seals the month every correct writer is using

## 2. Close out

- [x] 2.1 Verify each scenario across the two delta specs is answered by a normative sentence in README.md, including the drift check not seeing a sealed-month retraction, the late-merge retraction, and the validator two months slow
- [x] 2.2 Confirm both MODIFIED blocks copy their baseline requirement in full with every pre-existing scenario retained except the one deliberately moved to the ADDED requirement
- [x] 2.3 Commented on and closed #30 (2026-09-12, landed as ad35395): both points accepted; the first fixed by naming which operation guarantees what rather than by parsing in the drift check, and why (the regenerated retraction list needs every file, which is validation's cost and not the lag check's); the second with the proposed wording
- [x] 2.4 Commented on particulars-cli#11 (2026-09-12): `index --check` unchanged (counts plus open documents); `validate` additionally regenerates each sealed month's tombstone list and compares
- [x] 2.5 Recorded in particulars-knowledge#39 as clm_01a092e9-72fb-7864-8bdd-db567d6ed87d: a claim qualifying the fifth claim of #39 with the split of guarantees, and noting the pattern the week completes
