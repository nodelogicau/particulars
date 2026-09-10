## MODIFIED Requirements

### Requirement: The index mirrors retraction
When an object is retracted, the index SHALL record it: in a `dkf/0.1` index, its entry SHALL carry `retracted: true`; in a `dkf/0.2` index, its id SHALL appear in the `retracted` list of the root index for the current month, and later, when that month seals, in the `retracted` list of that month's segment. Its entry SHALL be unchanged wherever it sits, so that no sealed segment is rewritten. A retraction's `timestamp` SHALL NOT fall in a month earlier than the workspace's current month.

#### Scenario: Filtering without opening files
- **WHEN** `knowledge_recall` is called with `include_retracted: false`
- **THEN** retracted objects are excluded using the index alone — the entry flag in a `dkf/0.1` index, the `retracted` lists of the root and of the segments from the object's minting month onward in a `dkf/0.2` index

#### Scenario: Retracting into a sealed month
- **WHEN** a claim whose entry sits in `index/2026-08.yaml` is retracted in October 2026 in a `dkf/0.2` workspace
- **THEN** `index.yaml`'s `retracted` list gains the id and `index/2026-08.yaml` does not change

#### Scenario: The retraction seals with its month
- **WHEN** that retraction's month, October 2026, later seals
- **THEN** the id moves from the root's `retracted` into `index/2026-10.yaml`'s `retracted`, and the root's list holds only the new current month
