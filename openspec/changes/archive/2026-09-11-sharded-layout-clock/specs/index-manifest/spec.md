## MODIFIED Requirements

### Requirement: The index is a hot tail, sealed segments, and a tombstone list
In a `dkf/0.2` workspace, `index.yaml` SHALL carry `format`, `segments` (a list of paths, relative to `index.yaml`: `index/legacy.yaml` first if it exists, then one per sealed month in ascending order), `entries` (the entries of objects minted in the current month), and `retracted` (the ids, sorted, of objects whose `retracted.timestamp` falls in the current month or any later month, whatever month they were minted in). Each month's segment SHALL be at `index/<YYYY-MM>.yaml` and SHALL carry `format`, `entries` for objects minted in that month, and `retracted` for objects retracted in that month. `index/legacy.yaml` SHALL carry `format` and `entries` for objects whose ids derive no month, and no `retracted`. The current month SHALL be the month of the newest id in the workspace, and nothing else, so that a rebuild is a function of the files alone and sealing is driven by mints alone; a month earlier than the current month with retractions and no mints yields a segment with an empty `entries`, and a month with neither yields no segment. A sealed segment SHALL NOT change once written; `index/legacy.yaml` is not sealed and a change to it is drift. Entries SHALL NOT carry `retracted`; the per-month lists are the sole index record of retraction. Because an object cannot be retracted before it is minted, an object minted in month M is retracted if and only if its id appears in `retracted` of the root or of a segment for month M or later, a check whose cost is proportional to the months elapsed since M.

#### Scenario: Shape of the root index
- **WHEN** a workspace holds objects minted in August and September 2026, the newest id is from September, and one August object was retracted in September
- **THEN** `index.yaml` lists `index/2026-08.yaml` under `segments`, carries September's entries under `entries`, and its `retracted` names the August object

#### Scenario: Month rollover
- **WHEN** the first object of October 2026 is minted and the index is rebuilt
- **THEN** September's entries and September's retractions move into a new `index/2026-09.yaml`, `segments` gains that path, `entries` in the root holds only October, and `retracted` in the root holds retractions dated October or later

#### Scenario: A rebuild is deterministic
- **WHEN** two implementations rebuild the index of the same files on different days
- **THEN** they produce the same root document and the same segments, because the current month follows the newest id and not the clock

#### Scenario: A retraction touches only the root
- **WHEN** a claim whose entry is in `index/2026-08.yaml` is retracted in October 2026
- **THEN** its id is added to `retracted` in `index.yaml`, `index/2026-08.yaml` is byte-identical to before, and the root holds only retractions dated October or later

#### Scenario: Filtering retracted objects from the index
- **WHEN** `knowledge_recall` is called with `include_retracted: false` over objects minted in August 2026
- **THEN** retracted objects are excluded using the `retracted` lists of the root and of the segments for August and later, without opening files

#### Scenario: Filtering the current month
- **WHEN** `knowledge_recall` is called with `include_retracted: false` over objects minted in the current month
- **THEN** the root's `retracted` list alone decides

#### Scenario: A segment is a valid index document
- **WHEN** a tool that understands index entries opens `index/2026-08.yaml` on its own
- **THEN** it reads `format`, a list of entries, and a list of retracted ids in the shape defined by this specification, and nothing else

#### Scenario: A remote consumer caches sealed segments
- **WHEN** a consumer has fetched `index/2026-08.yaml` once
- **THEN** it never needs to fetch it again, and learns of every later retraction from the root and from segments newer than August

#### Scenario: A month of retractions only
- **WHEN** objects are retracted in November 2026 and none are minted, and the index is rebuilt after a December mint
- **THEN** `index/2026-11.yaml` exists with an empty `entries` and November's `retracted`

#### Scenario: The legacy segment
- **WHEN** a workspace holds a claim with id `clm_07m3zp9s2q1r4t8v`
- **THEN** its entry is in `index/legacy.yaml`, which is the first path under `segments`, and if it is retracted its id is in the `retracted` list of the month of its retraction

#### Scenario: A retraction dated ahead of the newest mint
- **WHEN** the newest id is from October 2026 and a retraction is dated in December 2026
- **THEN** the root's `retracted` carries it while October remains the current month, a November mint seals October without it, and it seals into `index/2026-12.yaml` only when a January 2027 or later id is minted

#### Scenario: A mint between the newest id and a retraction dated ahead
- **WHEN** the newest id is from October 2026, a retraction is dated in December 2026, and an object is minted in November 2026
- **THEN** the mint is legal, October seals, November becomes the current month, and no sealed segment changes
