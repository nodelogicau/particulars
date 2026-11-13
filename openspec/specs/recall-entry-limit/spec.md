# Recall Entry Limit Specification

## Purpose
Defines `entry_limit` on `knowledge_recall`, by particular or by query: the cap on the entries each particular returns, the fixed order that decides which entries a cap keeps (`current`, then unsynthesised, then, by query, matched, then the rest, most recent first within each), the lineage-order output, the `omitted` count that ignores entries the filters removed, the absence of a default, and the refusal of a non-positive cap.
## Requirements
### Requirement: Recall can cap the entries each particular returns
`knowledge_recall` SHALL accept an optional `entry_limit`, called with `particular_id` or with `query`. When `entry_limit` is omitted, a particular's part of the response SHALL be unchanged. When it is supplied and a particular's part of the response, after `author`, `scope` and `include_retracted` are applied, has more entries than `entry_limit`, the implementation SHALL keep exactly `entry_limit` of them. It SHALL take them in this order, each entry at the first tier it belongs to:

1. the entry identified as `current`, if it is in the response;
2. entries in the particular's `unsynthesised` set, as *Conflict semantics* defines it for the merge class;
3. in recall by query only, entries marked as matched;
4. every other entry.

Within each tier, entries SHALL be taken most recent first: by descending `timestamp`, ties broken by descending id. The kept entries SHALL be returned in lineage order with `current` identified, as without the cap. The cap SHALL NOT change which entry is `current`, which entries are unsynthesised, or which are marked as matched.

When `entry_limit` is supplied, each particular in the response SHALL carry `omitted`: the number of entries the cap removed from its part of the response, `0` when it removed none. `omitted` SHALL NOT count entries removed by `author`, `scope` or `include_retracted`.

#### Scenario: The belief survives the cap
- **WHEN** `par_T` has `syn_1` as `current`, followed in lineage order by ten later claims, and `knowledge_recall(particular_id: par_T, entry_limit: 1)` is called
- **THEN** the response contains `syn_1`, identified as `current`, and `omitted` is 10

#### Scenario: Disagreement is kept before history
- **WHEN** `par_T` has `current` `syn_2`, which synthesises `clm_1` to `clm_5`, and later claims `clm_6` and `clm_7` are unsynthesised, and `knowledge_recall(particular_id: par_T, entry_limit: 3)` is called
- **THEN** the response contains `syn_2`, `clm_6` and `clm_7`, and `omitted` is 5

#### Scenario: Most recent first within a tier
- **WHEN** `par_T` has no synthesis and claims `clm_1`, `clm_2` and `clm_3` with ascending timestamps, and `knowledge_recall(particular_id: par_T, entry_limit: 2)` is called
- **THEN** the response contains `clm_2` and `clm_3`, in lineage order, and `omitted` is 1

#### Scenario: Equal timestamps break by id
- **WHEN** two unsynthesised claims about `par_T` have the same `timestamp`, the cap has room for only one of them, and recall by particular is called
- **THEN** the one with the higher id is kept

#### Scenario: Kept entries keep their order
- **WHEN** a cap keeps `current` and two unsynthesised claims, one of which precedes `current` in lineage order
- **THEN** the three are returned in lineage order, not in the order they were selected

#### Scenario: A cap larger than the lineage
- **WHEN** `par_T`'s response has four entries and `entry_limit` is 10
- **THEN** all four are returned and `omitted` is 0

#### Scenario: No cap, no count
- **WHEN** `knowledge_recall(particular_id: par_T)` is called without `entry_limit`
- **THEN** the response is `par_T`'s whole lineage and does not carry `omitted`

#### Scenario: Filtered entries are not counted as omitted
- **WHEN** `par_T` has three `public` entries and five `personal` ones, and `knowledge_recall(particular_id: par_T, scope: public, entry_limit: 2)` is called
- **THEN** two `public` entries are returned and `omitted` is 1

#### Scenario: Withdrawn entries come last
- **WHEN** `knowledge_recall(particular_id: par_T, include_retracted: true, entry_limit: 2)` is called, `par_T` has a `current` synthesis and an unsynthesised claim, and its most recent entry is a retracted claim
- **THEN** the synthesis and the unsynthesised claim are kept and the retracted claim is not, because a withdrawn object is in no `unsynthesised` set

#### Scenario: The cap applies across a merge class
- **WHEN** `par_A` and `par_B` are merged, unsynthesised claims about each exist, and `knowledge_recall(particular_id: par_A, entry_limit: 2)` is called
- **THEN** the two most recent unsynthesised claims across both are kept, whichever particular they are about

### Requirement: `entry_limit` is a positive integer
`entry_limit` SHALL be an integer of at least 1. A call with any other value SHALL be refused with an error, and SHALL NOT return an empty or uncapped response.

#### Scenario: Zero is refused
- **WHEN** `knowledge_recall(particular_id: par_T, entry_limit: 0)` is called
- **THEN** the call is refused with an error

#### Scenario: A negative cap is refused
- **WHEN** `knowledge_recall(query: "timeout", entry_limit: -1)` is called
- **THEN** the call is refused with an error

