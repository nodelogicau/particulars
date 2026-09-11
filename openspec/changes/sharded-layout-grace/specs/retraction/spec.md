## MODIFIED Requirements

### Requirement: The index mirrors retraction
When an object is retracted, the index SHALL record it: in a `dkf/0.1` index, its entry SHALL carry `retracted: true`; in a `dkf/0.2` index, its id SHALL appear in the `retracted` list of the root index, which holds every retraction dated in either open month or later, and later, when the month of its `timestamp` seals, in the `retracted` list of that month's segment. Its entry SHALL be unchanged wherever it sits, so that no sealed segment is rewritten. A retraction's `timestamp` is the writer's clock; it SHALL NOT fall in a sealed month.

#### Scenario: Filtering without opening files
- **WHEN** `knowledge_recall` is called with `include_retracted: false`
- **THEN** retracted objects are excluded using the index alone — the entry flag in a `dkf/0.1` index, the `retracted` lists of the root and of the segments from the object's minting month onward in a `dkf/0.2` index

#### Scenario: Retracting into a sealed month
- **WHEN** a claim whose entry sits in `index/2026-08.yaml` is retracted in November 2026 in a `dkf/0.2` workspace
- **THEN** `index.yaml`'s `retracted` list gains the id and `index/2026-08.yaml` does not change

#### Scenario: The retraction seals with its month
- **WHEN** that retraction's month, November 2026, later seals because an id is minted in January 2027 or later
- **THEN** the id moves from the root's `retracted` into `index/2026-11.yaml`'s `retracted`, and the root's list holds only retractions dated in an open month or later

#### Scenario: A retraction dated ahead waits in the root
- **WHEN** a retraction is dated in December 2026 by a writer whose clock is ahead while the newest id is from October 2026
- **THEN** its id sits in the root's `retracted` and seals into `index/2026-12.yaml` when an id is minted in February 2027 or later

#### Scenario: A retraction on a branch merged across one boundary
- **WHEN** a claim is retracted on a branch on 28 November 2026 and the branch merges on 5 December after main has minted in December
- **THEN** November is open, the id is in the root's `retracted`, and no segment changes
