## MODIFIED Requirements

### Requirement: A sealed month gains no files
A month SHALL be sealed once any id in the workspace was minted two or more months after it; the current month and the month before it are open. An implementation SHALL NOT mint an id whose month is sealed, and SHALL NOT write a retraction whose `timestamp` falls in a sealed month; it mints and dates retractions at its own clock, and with a month of grace only a clock more than a month out can trip either guard. A file within a sealed month MAY change only by the single modification the format permits to any object file, the appending of a `retracted` block. A file arriving in a sealed month's directory by a merge — a branch open across two or more month boundaries — is a late merge: validation SHALL fail naming the file, and the remedy is to re-mint the branch's objects before merging. The specification SHALL state the git consequence as the benefit delivered rather than as a rule: an old month's tree object is rewritten only by a late merge or a retraction, never by an ordinary append. The `legacy` directory is not a month: it is never sealed, no conformant writer adds to it, and a rebuild that finds it changed reports the difference as drift.

#### Scenario: Retracting into a sealed month
- **WHEN** a claim under `claims/2026-08/` is retracted in November 2026
- **THEN** its file gains a `retracted` block and nothing else in `claims/2026-08/` changes

#### Scenario: A sealed directory in git
- **WHEN** objects are appended for a year after August 2026
- **THEN** no commit in that year rewrites the tree object for `claims/2026-08/` unless a file in it is retracted or a late merge adds one

#### Scenario: A retraction dated into a sealed month
- **WHEN** an implementation is asked in November 2026 to write a retraction with `timestamp` in August 2026, and the newest id is from November
- **THEN** it refuses, and the writer records the retraction with a current timestamp and a `reason` that says when it was decided

#### Scenario: The legacy directory is not sealed
- **WHEN** a file is copied into `claims/legacy/` after the workspace has objects minted in later months
- **THEN** no sealed-month rule is violated, and the next drift check reports the index as lagging

#### Scenario: A retraction dated into the future
- **WHEN** an implementation whose clock reads 2026-11-03 writes a retraction
- **THEN** it dates it 2026-11-03, its own clock, and the timestamp lands in an open month

#### Scenario: A branch open across one boundary
- **WHEN** a claim is minted on a branch on 28 November 2026 and merged on 5 December after main has minted in December
- **THEN** the file lands under `claims/2026-11/`, November is open, and validation passes

#### Scenario: A branch open across two boundaries
- **WHEN** a claim minted on a branch in August 2026 is merged in November 2026 after main has minted in October or later
- **THEN** the file lands under `claims/2026-08/`, which is sealed, and validation fails naming it as a late merge

#### Scenario: Clock skew at a month boundary
- **WHEN** a machine two days slow mints on what it believes is 30 November 2026 while the newest id is from 2 December
- **THEN** the id lands under `claims/2026-11/`, which is open, and nothing is refused

#### Scenario: A writer more than a month behind
- **WHEN** the newest id in the workspace is from December 2026 and a machine whose clock reads September 2026 tries to mint
- **THEN** it refuses, because September is sealed, and names the sealed month

### Requirement: A validator warns on time it cannot have seen
A validator SHOULD report, as a warning naming the object, any id whose minting instant is later than the validator's own clock, and any object or retraction `timestamp` later than it; such a warning SHALL NOT fail validation, because a clock a few days fast at a month end is ordinary and the validator's clock may be the one that is wrong. A validator SHALL fail on an id whose month is two or more months later than the validator's current month, because such an id seals the month every correct writer is minting into. The specification SHALL state that an id can only be dated ahead by a clock, that every validator on a correctly set machine will therefore flag it, and that the place to catch it is a pull-request check before the object is merged.

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
