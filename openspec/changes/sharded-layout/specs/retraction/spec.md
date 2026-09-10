## MODIFIED Requirements

### Requirement: The index mirrors retraction
When an object is retracted, the index SHALL record it: in a `dkf/0.1` index, its entry SHALL carry `retracted: true`; in a `dkf/0.2` index, its id SHALL appear in the root index's `retracted` list and its entry SHALL be unchanged, so that the segment holding the entry is not rewritten.

#### Scenario: Filtering without opening files
- **WHEN** `knowledge_recall` is called with `include_retracted: false`
- **THEN** retracted objects are excluded using the index alone — the entry flag in a `dkf/0.1` index, the `retracted` list in a `dkf/0.2` index

#### Scenario: Retracting into a sealed month
- **WHEN** a claim whose entry sits in `index/2026-08.yaml` is retracted in a `dkf/0.2` workspace
- **THEN** `index.yaml`'s `retracted` list gains the id and `index/2026-08.yaml` does not change
