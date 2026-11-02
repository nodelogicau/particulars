## MODIFIED Requirements

### Requirement: The index is a hot tail, sealed segments, and a tombstone list
In a `dkf/0.2` or later workspace, `index.yaml` SHALL carry `format`, `segments` (a list of mappings, each with `path` relative to `index.yaml` and `count`, the number of entries in that segment: `index/legacy.yaml` first if it exists, then one per sealed month in ascending order), `entries` (the entries of objects minted in either open month), and `retracted` (the ids, sorted, of objects whose `retracted.timestamp` falls in either open month or any later month, whatever month they were minted in), and, in a `dkf/0.3` workspace, `redacted` (the ids, sorted, of objects whose `redacted.fields` includes `content` and whose `redacted.timestamp` falls in either open month or any later month). The current month SHALL be the month of the newest id in the workspace; the open months SHALL be the current month and the month before it; a month SHALL be sealed once any id in the workspace was minted two or more months after it. Each sealed month's segment SHALL be at `index/<YYYY-MM>.yaml` and SHALL carry `format`, `entries` for objects minted in that month, `retracted` for objects retracted in that month, and, in `dkf/0.3`, `redacted` for objects content-redacted in that month; its `count` in the root SHALL equal the number of its entries, which SHALL equal the number of files in that month's directories across every type. `index/legacy.yaml` SHALL carry `format` and `entries` for objects whose ids derive no month, and no `retracted` or `redacted`. A rebuild SHALL be a function of the files alone; a sealed month with retractions or redactions and no mints yields a segment with an empty `entries`, and a month with none of these yields no segment. A sealed segment SHALL NOT change once written; `index/legacy.yaml` is not sealed and a change to it is drift. Entries SHALL NOT carry `retracted` or `redacted`; the per-month lists are the sole index record of retraction and of withdrawal by redaction, and no redaction changes an entry, because no redactable field is mirrored by one. Because an object cannot be retracted before it is minted, an object minted in month M is retracted if and only if its id appears in `retracted` of the root or of a segment for month M or later, a check whose cost is proportional to the months elapsed since M; the same holds for `redacted`, so an object minted in month M is withdrawn if and only if its id appears in `retracted` or `redacted` of the root or of a segment for month M or later.

#### Scenario: Shape of the root index
- **WHEN** a workspace holds objects minted in August, September and October 2026, the newest id is from October, and one August object was retracted in September
- **THEN** `index.yaml` lists `index/2026-08.yaml` with its count under `segments`, carries September's and October's entries under `entries`, and its `retracted` names the August object

#### Scenario: Month rollover
- **WHEN** the first object of November 2026 is minted and the index is rebuilt
- **THEN** September's entries and September's retractions move into a new `index/2026-09.yaml`, `segments` gains its path and count, and the root holds October and November

#### Scenario: A rebuild is deterministic
- **WHEN** two implementations rebuild the index of the same files on different days
- **THEN** they produce the same root document and the same segments, because the open months follow the newest id and not the clock

#### Scenario: A retraction touches only the root
- **WHEN** a claim whose entry is in `index/2026-08.yaml` is retracted in October 2026
- **THEN** its id is added to `retracted` in `index.yaml`, `index/2026-08.yaml` is byte-identical to before, and the root holds only retractions dated in an open month or later

#### Scenario: Filtering retracted objects from the index
- **WHEN** `knowledge_recall` is called with `include_retracted: false` over objects minted in August 2026
- **THEN** retracted objects are excluded using the `retracted` lists of the root and of the segments for August and later, without opening files

#### Scenario: Filtering the current month
- **WHEN** `knowledge_recall` is called with `include_retracted: false` over objects minted in the current month
- **THEN** the root's `retracted` list alone decides

#### Scenario: A segment is a valid index document
- **WHEN** a tool that understands index entries opens `index/2026-08.yaml` on its own
- **THEN** it reads `format`, a list of entries, a list of retracted ids, and, in `dkf/0.3`, a list of redacted ids, in the shape defined by this specification, and nothing else

#### Scenario: A remote consumer caches sealed segments
- **WHEN** a consumer has fetched `index/2026-08.yaml` once and the workspace validates
- **THEN** it never needs to fetch it again, and learns of every later retraction from the root and from segments newer than August

#### Scenario: A month of retractions only
- **WHEN** objects are retracted in November 2026 and none are minted, and the index is rebuilt after a January 2027 mint
- **THEN** `index/2026-11.yaml` exists with an empty `entries` and November's `retracted`

#### Scenario: The legacy segment
- **WHEN** a workspace holds a claim with id `clm_07m3zp9s2q1r4t8v`
- **THEN** its entry is in `index/legacy.yaml`, which is the first path under `segments`, and if it is retracted its id is in the `retracted` list of the month of its retraction

#### Scenario: A branch merged across one month boundary
- **WHEN** a claim minted on a branch on 28 November 2026 is merged on 5 December, after main has minted in December
- **THEN** November is still open, the claim's entry goes into the root, and no segment changes

#### Scenario: A retraction dated ahead of the newest mint
- **WHEN** the newest id is from October 2026 and a retraction is dated in December 2026 by a writer whose clock is ahead
- **THEN** the root's `retracted` carries it, and it seals into `index/2026-12.yaml` only when an id is minted in February 2027 or later

#### Scenario: A redaction touches only the root
- **WHEN** a claim whose entry is in `index/2026-08.yaml` has its `content` redacted in October 2026 in a `dkf/0.3` workspace
- **THEN** its id is added to `redacted` in `index.yaml`, its entry and `index/2026-08.yaml` are byte-identical to before, and the id seals into `index/2026-10.yaml`'s `redacted` with October

#### Scenario: Filtering withdrawn objects from the index
- **WHEN** `knowledge_recall` is called with `include_retracted: false` over objects minted in August 2026 in a `dkf/0.3` workspace
- **THEN** retracted and content-redacted objects are both excluded using the `retracted` and `redacted` lists of the root and of the segments for August and later, without opening files
