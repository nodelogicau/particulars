## MODIFIED Requirements

### Requirement: A sealed month gains no files
A month directory SHALL be sealed once any id in the workspace was minted in a later month. A sealed directory SHALL gain no files. A file within it MAY change only by the single modification the format permits to any object file, the appending of a `retracted` block. A writer SHALL write at the workspace's present when its own clock is behind it: an implementation SHALL NOT mint an id earlier than the newest id in the workspace, and when its clock is earlier than that id's instant it SHALL mint at an instant just after the newest id rather than refuse; and it SHALL NOT write a retraction whose `timestamp` is earlier than the start of the newest id's month, nor later than the later of its own clock and that instant. No write SHALL be refused because another writer's clock disagreed with this one. The `legacy` directory is not a month: it is never sealed, no conformant writer adds to it, and a rebuild that finds it changed reports the difference as drift.

#### Scenario: Retracting into a sealed month
- **WHEN** a claim under `claims/2026-08/` is retracted in October 2026
- **THEN** its file gains a `retracted` block and nothing else in `claims/2026-08/` changes

#### Scenario: A sealed directory in git
- **WHEN** objects are appended for a year after August 2026
- **THEN** no commit in that year rewrites the tree object for `claims/2026-08/` unless a file in it is retracted

#### Scenario: A retraction dated into a sealed month
- **WHEN** an implementation is asked in October 2026 to write a retraction with `timestamp` in September 2026, and the newest id is from October
- **THEN** it refuses, and the writer records the retraction with a current timestamp and a `reason` that says when it was decided

#### Scenario: The legacy directory is not sealed
- **WHEN** a file is copied into `claims/legacy/` after the workspace has objects minted in later months
- **THEN** no sealed-month rule is violated, and the next drift check reports the index as lagging

#### Scenario: A retraction dated into the future
- **WHEN** an implementation whose clock reads 2026-11-03 is asked to write a retraction with `timestamp: 2027-11-03T10:00:00Z`, and no id in the workspace is later than November 2026
- **THEN** it refuses, naming the timestamp and its own clock

#### Scenario: A mint after a retraction dated ahead
- **WHEN** the newest id is from October 2026, a retraction has been dated in December 2026, and an implementation mints in November 2026
- **THEN** the mint is permitted, because the bound is the newest id's month and not the retraction's

#### Scenario: A retraction from a writer behind the workspace
- **WHEN** the newest id was minted on 2 December 2026 by a machine two days fast, and a machine whose clock reads 30 November 2026 retracts an object
- **THEN** it writes the retraction with `timestamp` at the start of December 2026, the workspace's present, and records in `reason` when it was decided if that matters

#### Scenario: A mint from a writer behind the workspace
- **WHEN** the newest id was minted on 2 December 2026 by a machine two days fast, and a machine whose clock reads 30 November 2026 asserts a claim
- **THEN** it mints an id whose instant is just after the newest id, the file lands under `claims/2026-12/`, and the claim's `timestamp` carries the writer's own clock

#### Scenario: A writer ahead of the workspace
- **WHEN** a writer's clock is later than every id in the workspace
- **THEN** it mints and dates retractions at its own clock, as before

### Requirement: A validator warns on time it cannot have seen
A validator SHOULD report, as a warning naming the object, any id whose minting instant is later than the validator's own clock, and any object or retraction `timestamp` later than it. The warning SHALL NOT fail validation: the validator's clock may be the one that is wrong, and under the single sealing clock a future-dated object still has exactly one derived home. The specification SHALL state that an id can only be dated ahead by a clock, that every validator on a correctly set machine will therefore flag it, and that the place to catch it is a pull-request check before the object is merged, since once merged it is the workspace's present until the calendar reaches it.

#### Scenario: A future-dated retraction in a hand-edited file
- **WHEN** a claim file carries `retracted.timestamp: 2027-11-03T10:00:00Z` and the validator runs on 2026-11-04
- **THEN** validation warns naming the claim, and exits successfully if nothing else is wrong

#### Scenario: An id minted on a skewed clock
- **WHEN** an id's UUIDv7 timestamp is two days later than the validator's clock
- **THEN** validation warns naming the object, and the object's file is still expected at the month its id derives

#### Scenario: Honest time
- **WHEN** every id and timestamp in the workspace is at or before the validator's clock
- **THEN** nothing is reported

#### Scenario: A clamped id seen from the behind machine
- **WHEN** a writer behind the workspace mints an id clamped to just after the newest id, and then validates on the same machine
- **THEN** validation warns naming the new object, because from that machine's clock the id is in the future, and does not fail

#### Scenario: A far-future id caught at review
- **WHEN** a machine a year fast mints an object on a branch and opens a pull request, and the check runs `validate` on a correctly set machine
- **THEN** the check surfaces the warning naming the object, and a reviewer declines to merge it
