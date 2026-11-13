## MODIFIED Requirements

### Requirement: Recall by query resolves to particulars, then recalls structurally
`knowledge_recall` called with `query` SHALL first resolve the query to a set of particulars, each taken with its merge equivalence class, and SHALL then return, for each, exactly what `knowledge_recall` called with that particular's id and the same `author`, `scope`, `include_retracted`, and `entry_limit` would return, except that when `entry_limit` removes entries, entries marked as matched SHALL be kept ahead of the remaining ones as *Recall can cap the entries each particular returns* specifies. Every object in the response SHALL come from this second stage. Within a particular the order SHALL be lineage order with `current` identified, as for recall by particular; resolution SHALL NOT reorder it. Objects whose `content` matches the query, as the baseline defines a match — the trimmed whole query or any one trimmed term occurring in it — SHALL be marked as matched within their particular's results. `limit` SHALL bound the number of particulars and `entry_limit` the number of entries each returns.

#### Scenario: A query that matches a superseded claim
- **WHEN** `clm_1` about `par_T` contains "auth timeout", `syn_1` about `par_T` synthesises `clm_1` and does not contain the phrase, and `knowledge_recall(query: "auth timeout")` is called
- **THEN** the response contains `par_T`'s lineage with `syn_1` identified as `current` and `clm_1` marked as matched

#### Scenario: Filters apply after resolution
- **WHEN** the query matches a retracted claim about `par_A` and `knowledge_recall(query, include_retracted: false)` is called
- **THEN** `par_A` may be resolved, but the retracted claim is not in the response

#### Scenario: Resolution across a merge
- **WHEN** the query matches the label of `par_A`, and `par_A` and `par_B` are merged
- **THEN** the response includes claims whose `subject` is `par_B`

#### Scenario: A resolved particular with nothing in scope
- **WHEN** the query resolves to `par_P`, all of whose objects are `personal`, and the call has `scope: public`
- **THEN** `par_P` does not appear in the response

#### Scenario: One term is enough to mark an object
- **WHEN** the query is `billing outage` and a claim's content contains "billing" but not "outage"
- **THEN** the claim is marked as matched

#### Scenario: Limit alone does not bound entries
- **WHEN** a query resolves one particular whose response has 140 entries, and `knowledge_recall(query, limit: 1)` is called without `entry_limit`
- **THEN** the response contains that particular with all 140 entries

#### Scenario: Both bounds together
- **WHEN** a query resolves five particulars, each with more than 10 entries in its response, and `knowledge_recall(query, limit: 3, entry_limit: 10)` is called
- **THEN** the response contains three particulars, each with exactly 10 entries and an `omitted` count

#### Scenario: A matched entry is kept ahead of an unmatched one
- **WHEN** `par_T` has `current` `syn_2`, which synthesises `clm_1` and `clm_2`, only the older `clm_1` contains "timeout", nothing is unsynthesised, and `knowledge_recall(query: "timeout", entry_limit: 2)` is called
- **THEN** `par_T`'s results are `syn_2` and `clm_1`, with `clm_1` marked as matched, and `omitted` is 1

#### Scenario: Unsynthesised entries are kept ahead of matched ones
- **WHEN** `par_T` has `current` `syn_2`, a synthesised claim containing "timeout", and an unsynthesised claim that does not contain it, and `knowledge_recall(query: "timeout", entry_limit: 2)` is called
- **THEN** `par_T`'s results are `syn_2` and the unsynthesised claim

### Requirement: Each result says how it was resolved
Each particular in a recall-by-query response SHALL carry `resolution`, one of `label`, `alias`, `lexical`, or `semantic`: `label` or `alias` when the particular's label or one of its aliases, under case folding, occurs in the case-folded query such that every character of the query outside that occurrence is of Unicode general category P or has the Unicode `White_Space` property; `lexical` when the baseline matched otherwise; `semantic` when only a semantic stage proposed it. A particular resolved more than one way SHALL carry the first applicable value in that order. Particulars SHALL be ordered by `resolution` in that order. Within `label` and `alias`, particulars SHALL be ordered first by the length, in code points after case folding, of the longest label or alias that makes the particular exact, longer first. Within `label`, `alias`, and `lexical`, particulars SHALL then be ordered by whether the trimmed whole query matches the particular's label, an alias, or the `content` of an object in its response, those that match first; then by the number of distinct trimmed terms, after case folding, that match any of those, more first; then by ascending particular id, taking the lowest id of a merge class. A particular's response for this ordering SHALL be taken after `author`, `scope`, and `include_retracted` are applied and before `entry_limit` is, so that `entry_limit` SHALL NOT change which particulars are returned or their order. Within `semantic` the order is implementation-defined. When `limit` truncates, the first particulars in this order SHALL be kept.

#### Scenario: Exact alias
- **WHEN** a particular has alias `DKF` and the query is `dkf`
- **THEN** its `resolution` is `alias`

#### Scenario: Found both ways
- **WHEN** the baseline matches a particular's claim content and the semantic stage also proposes it
- **THEN** its `resolution` is `lexical`

#### Scenario: Limit keeps exact matches
- **WHEN** a query resolves one particular by `label` and five by `semantic`, and `limit` is 3
- **THEN** the `label` particular is in the response

#### Scenario: A name asked about with a question mark is still exact
- **WHEN** a particular has label `Project X` and the query is `Project X?`
- **THEN** its `resolution` is `label`

#### Scenario: A quoted name is still exact
- **WHEN** a particular has label `Project X` and the query is `"Project X"`
- **THEN** its `resolution` is `label`

#### Scenario: A name ending in punctuation is still exact
- **WHEN** a particular has label `C#` and the query is `C#?`
- **THEN** its `resolution` is `label`

#### Scenario: A prefix is not exact
- **WHEN** a particular has label `C#` and the query is `C`
- **THEN** its `resolution` is not `label`

#### Scenario: More terms matched ranks first
- **WHEN** the query is `auth timeout`, `par_A`'s response contains a claim with "auth" and a claim with "timeout" but neither contains "auth timeout", `par_B`'s contains only "auth", both are `lexical`, and `limit` is 1
- **THEN** `par_A` is in the response and `par_B` is not

#### Scenario: The whole query ranks before scattered terms
- **WHEN** the query is `auth timeout`, `par_A`'s response contains "auth timeout", `par_B`'s contains "auth" and "timeout" separately, and both are `lexical`
- **THEN** `par_A` is ordered before `par_B`

#### Scenario: Ties break by id
- **WHEN** two `lexical` particulars match the same number of distinct terms and neither matches the whole query
- **THEN** the one with the lower particular id is ordered first

#### Scenario: What the caller cannot see does not rank
- **WHEN** `par_A`'s only claim containing "timeout" is retracted and the call has `include_retracted: false`
- **THEN** "timeout" does not count toward `par_A`'s distinct terms

#### Scenario: What the cap removes still ranks
- **WHEN** the query is `auth timeout`, `par_A`'s only claim containing "timeout" is removed by `entry_limit`, `par_A` also has a claim containing "auth", `par_B`'s response contains only "auth", both are `lexical`, and `limit` is 1
- **THEN** `par_A` is in the response and `par_B` is not, as they would be without `entry_limit`

#### Scenario: Whitespace beside a name is still exact
- **WHEN** a particular has label `Project X` and the query is `Project X ?`
- **THEN** its `resolution` is `label`

#### Scenario: A line of input is still exact
- **WHEN** a particular has label `Project X` and the query is a space, `Project X`, and a line feed
- **THEN** its `resolution` is `label`

#### Scenario: Interior whitespace is kept
- **WHEN** a particular has label `Project X` and the query is `Project  X` with two spaces
- **THEN** its `resolution` is not `label`

#### Scenario: Edge whitespace does not change the order
- **WHEN** the query is `auth timeout ` with a trailing space, and `par_A`'s response contains "auth timeout" only at the end of a claim's content
- **THEN** `par_A` counts as matching the whole query

#### Scenario: The longer exact name ranks first
- **WHEN** `par_C` has label `C`, `par_S` has label `C#`, `par_C` has the lower id, the query is `C#`, and `limit` is 1
- **THEN** both are exact, `par_S` is in the response, and `par_C` is not
