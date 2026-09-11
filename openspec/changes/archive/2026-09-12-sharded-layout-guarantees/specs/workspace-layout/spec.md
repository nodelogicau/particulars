## MODIFIED Requirements

### Requirement: A validator warns on time it cannot have seen
A validator SHOULD report, as a warning naming the object, any id whose minting instant is later than the validator's own clock, and any object or retraction `timestamp` later than it; such a warning SHALL NOT fail validation, because a clock a few days fast at a month end is ordinary and the validator's clock may be the one that is wrong. A validator SHALL fail on an id whose month is two or more months later than the validator's current month. The uncertainty is the same in both cases — a validator two months slow cannot tell itself from an id two months fast — and the rule rests on the asymmetry of consequence, not of confidence: a validator whose own clock is two months slow fails a healthy workspace once, loudly, on a machine that is itself broken, and that is the better error, because the alternative is accepting an id that seals the month every correct writer is minting into, which cannot be undone. The specification SHALL state that an id can only be dated ahead by a clock, that every validator on a correctly set machine will therefore flag it, and that the place to catch it is a pull-request check before the object is merged.

#### Scenario: A future-dated retraction in a hand-edited file
- **WHEN** a claim file carries `retracted.timestamp: 2027-11-03T10:00:00Z` and the validator runs on 2026-11-04
- **THEN** validation warns naming the claim, and exits successfully if nothing else is wrong

#### Scenario: An id minted on a skewed clock
- **WHEN** an id's UUIDv7 timestamp is two days later than the validator's clock
- **THEN** validation warns naming the object, and the object's file is still expected at the month its id derives

#### Scenario: Honest time
- **WHEN** every id and timestamp in the workspace is at or before the validator's clock
- **THEN** nothing is reported

#### Scenario: An id one month ahead
- **WHEN** an id's month is the month after the validator's current month
- **THEN** validation warns and does not fail, because that month is the next open one and seals nothing

#### Scenario: A far-future id
- **WHEN** an id's month is two or more months after the validator's current month
- **THEN** validation fails naming the object, because the id would seal the month correct writers are minting into

#### Scenario: A far-future id caught at review
- **WHEN** a machine a year fast mints an object on a branch and opens a pull request, and the check runs `validate` on a correctly set machine
- **THEN** the check fails naming the object, and the object is not merged

#### Scenario: A validator two months slow
- **WHEN** a validator's own clock is two months behind and it checks a healthy workspace whose newest id is from the real current month
- **THEN** it fails naming that object, and the failure is the intended error: the machine running the validator is the one to fix
