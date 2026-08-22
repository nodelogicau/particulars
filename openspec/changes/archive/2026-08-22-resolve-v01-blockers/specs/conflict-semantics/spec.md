## ADDED Requirements

### Requirement: Promotion records are not knowledge
Publish records SHALL NOT affect `current`, `unsynthesised`, or `stale`, SHALL NOT be reported by `conflict_detect`, and SHALL NOT form equivalence classes as merge records do.

#### Scenario: Promoting a claim changes no conflict set
- **WHEN** a claim covered by the `current` synthesis is promoted to `public`
- **THEN** the particular's conflict sets are unchanged and it is not reported

#### Scenario: A promotion is never unsynthesised
- **WHEN** a workspace contains promotion records that no synthesis cites
- **THEN** they do not appear in any `unsynthesised` set
