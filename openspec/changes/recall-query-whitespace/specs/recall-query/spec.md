## MODIFIED Requirements

### Requirement: Each result says how it was resolved
Each particular in a recall-by-query response SHALL carry `resolution`, one of `label`, `alias`, `lexical`, or `semantic`: `label` or `alias` when the particular's label or one of its aliases, under case folding, occurs in the case-folded query such that every character of the query outside that occurrence is of Unicode general category P or has the Unicode `White_Space` property; `lexical` when the baseline matched otherwise; `semantic` when only a semantic stage proposed it. A particular resolved more than one way SHALL carry the first applicable value in that order. Particulars SHALL be ordered by `resolution` in that order. Within `label` and `alias`, particulars SHALL be ordered first by the length, in code points after case folding, of the longest label or alias that makes the particular exact, longer first. Within `label`, `alias`, and `lexical`, particulars SHALL then be ordered by whether the trimmed whole query matches the particular's label, an alias, or the `content` of an object in its response, those that match first; then by the number of distinct trimmed terms, after case folding, that match any of those, more first; then by ascending particular id, taking the lowest id of a merge class. Within `semantic` the order is implementation-defined. When `limit` truncates, the first particulars in this order SHALL be kept.

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

### Requirement: A lexical baseline is required and always runs
Every implementation SHALL resolve a query, without a model, by matching it under Unicode case folding against particular labels and aliases and against claim and synthesis `content`. The query's terms SHALL be its maximal runs of characters without the Unicode `White_Space` property. Before matching, leading and trailing characters that are of Unicode general category P or have the Unicode `White_Space` property SHALL be removed from the whole query and from each term, as written and before case folding; interior characters SHALL be kept. A term that is empty after removal SHALL be ignored. A text SHALL match when the trimmed whole query, or any one trimmed term, is a substring of it; a particular SHALL be resolved by the baseline when its label, one of its aliases, or the `content` of one of its claims or syntheses matches. A query that is empty after removal SHALL resolve no particular and SHALL NOT be an error. The baseline SHALL run on every recall by query, whether or not any other stage is available. Another stage MAY add particulars to the resolved set and SHALL NOT remove any the baseline found.

#### Scenario: No model available
- **WHEN** an implementation has no embedding model and `knowledge_recall(query: "Timeout")` is called on a workspace with a claim containing "timeout"
- **THEN** that claim's subject is resolved with `resolution: lexical`

#### Scenario: An identifier embeddings miss
- **WHEN** the query is a ticket number that appears verbatim in one claim and the semantic stage does not propose that claim's subject
- **THEN** the subject is resolved, because the baseline found it

#### Scenario: A question mark does not hide a term
- **WHEN** a claim reads "The session timeout is 30 minutes." and the query is `timeout?`
- **THEN** the claim's subject is resolved with `resolution: lexical`, and the claim is marked as matched

#### Scenario: An identifier at the end of a sentence
- **WHEN** a claim contains `PROJ-1234` and the query is `the ticket was PROJ-1234.`
- **THEN** the claim's subject is resolved

#### Scenario: Interior punctuation is kept
- **WHEN** a claim contains "v1.2" and no other text matching, and the query is `v1.2.3?`
- **THEN** the claim's subject is not resolved by the baseline

#### Scenario: Any term is enough
- **WHEN** the query is `billing outage` and the only claim about `par_B` contains "billing" but not "outage"
- **THEN** `par_B` is resolved

#### Scenario: A query of punctuation alone
- **WHEN** the query is `?!`
- **THEN** no particular is resolved, the response is empty, and no error is raised

#### Scenario: A query of whitespace alone
- **WHEN** the query is three spaces
- **THEN** no particular is resolved, the response is empty, and no error is raised

#### Scenario: A label of punctuation alone
- **WHEN** a particular has label `?` and the query is `?!`
- **THEN** that particular is not resolved, because the query is empty after removal
