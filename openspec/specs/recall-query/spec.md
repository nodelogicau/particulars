# Recall Query Specification

## Purpose

Defines `knowledge_recall` called with a free-text `query`: resolution to particulars followed by structural recall, the required model-free lexical baseline, the `resolution` marker on results, the optional semantic cache and its rules (derived, model-tagged, outside the workspace, never committed or published, never authoritative), the scope ceiling on remote embedding, and that `particular_resolve` stays exact.

## Requirements

### Requirement: Recall by query resolves to particulars, then recalls structurally
`knowledge_recall` called with `query` SHALL first resolve the query to a set of particulars, each taken with its merge equivalence class, and SHALL then return, for each, exactly what `knowledge_recall` called with that particular's id and the same `author`, `scope`, and `include_retracted` would return. Every object in the response SHALL come from this second stage. Within a particular the order SHALL be lineage order with `current` identified, as for recall by particular; resolution SHALL NOT reorder it. Objects whose `content` matches the query, as the baseline defines a match — the trimmed whole query or any one trimmed term occurring in it — SHALL be marked as matched within their particular's results.

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

### Requirement: Each result says how it was resolved
Each particular in a recall-by-query response SHALL carry `resolution`, one of `label`, `alias`, `lexical`, or `semantic`: `label` or `alias` when the particular's label or one of its aliases, under case folding, occurs in the case-folded query such that every character of the query outside that occurrence is of Unicode general category P; `lexical` when the baseline matched otherwise; `semantic` when only a semantic stage proposed it. A particular resolved more than one way SHALL carry the first applicable value in that order. Particulars SHALL be ordered by `resolution` in that order. Within `label`, `alias`, and `lexical`, particulars SHALL be ordered first by whether the trimmed whole query matches the particular's label, an alias, or the `content` of an object in its response, those that match first; then by the number of distinct trimmed terms, after case folding, that match any of those, more first; then by ascending particular id, taking the lowest id of a merge class. Within `semantic` the order is implementation-defined. When `limit` truncates, the first particulars in this order SHALL be kept.

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

### Requirement: A lexical baseline is required and always runs
Every implementation SHALL resolve a query, without a model, by matching it under Unicode case folding against particular labels and aliases and against claim and synthesis `content`. The query's terms SHALL be its maximal runs of characters without the Unicode `White_Space` property. Before matching, leading and trailing characters of Unicode general category P SHALL be removed from the whole query and from each term, as written and before case folding; interior characters SHALL be kept. A term that is empty after removal SHALL be ignored. A text SHALL match when the trimmed whole query, or any one trimmed term, is a substring of it; a particular SHALL be resolved by the baseline when its label, one of its aliases, or the `content` of one of its claims or syntheses matches. A query that is empty after removal SHALL resolve no particular and SHALL NOT be an error. The baseline SHALL run on every recall by query, whether or not any other stage is available. Another stage MAY add particulars to the resolved set and SHALL NOT remove any the baseline found.

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

### Requirement: A semantic cache is optional, derived, and never authoritative
An implementation MAY keep a cache of embeddings of particular labels and aliases and of claim and synthesis `content`, and MAY use it to propose particulars in the resolution stage. The cache SHALL be fully regenerable from the workspace files. It SHALL record the identifier of the model that produced it and SHALL NOT be consulted when that differs from the model in use. It SHALL be stored outside the workspace directory tree, SHALL NOT be committed, and SHALL NOT be published or served to consumers. Validators and drift checks SHALL NOT read it. A missing, partial, or stale cache SHALL NOT cause an object to be returned that recall by particular would not return; it MAY cause a particular to be unresolved that a complete cache would have proposed.

#### Scenario: Missing cache
- **WHEN** the cache has been deleted and `knowledge_recall(query)` is called
- **THEN** the response is the baseline's, every result's `resolution` is `label`, `alias`, or `lexical`, and no error is raised

#### Scenario: Model changed
- **WHEN** the cache records model `m1` and the implementation is now configured with `m2`
- **THEN** the cache is not consulted until rebuilt under `m2`

#### Scenario: Retraction after embedding
- **WHEN** a claim was embedded and has since been retracted, and recall by query is called with `include_retracted: false`
- **THEN** the claim is not in the response, and the cache did not have to be updated for this to hold

#### Scenario: Not in the published tree
- **WHEN** a publisher serves its workspace directory over HTTP
- **THEN** no embedding data is reachable under it

#### Scenario: Incremental update
- **WHEN** an object is added to a workspace whose cache was complete under the current model
- **THEN** bringing the cache up to date requires embedding only that object, identified from ids present in the index and absent from the cache

### Requirement: Content is sent to a remote embedding service only by configuration and under a scope ceiling
An implementation SHALL NOT send object content, labels, or aliases to an embedding service on another host unless explicitly configured to. Such configuration SHALL name a scope ceiling, defaulting to `public`, and the implementation SHALL NOT send an object whose effective scope — including promotion records — is narrower than the ceiling. Objects not embedded for this reason SHALL remain resolvable through the baseline. This configuration SHALL NOT be read from `dkf.yaml`.

#### Scenario: Default ceiling
- **WHEN** remote embedding is configured without a ceiling and the workspace holds a `personal` claim and a `public` claim
- **THEN** only the `public` claim's content is sent

#### Scenario: Promotion widens eligibility
- **WHEN** a `personal` claim is promoted to `public` by a promotion record under a `public` ceiling
- **THEN** the claim becomes eligible to be embedded

#### Scenario: Not configured
- **WHEN** no remote embedding is configured and no local model is available
- **THEN** no content leaves the machine and recall by query uses the baseline alone

### Requirement: Particular resolution stays exact
`particular_resolve(query)` SHALL NOT use a semantic stage. It SHALL continue to match by id, URI, label, or alias, and to return null rather than a nearest candidate.

#### Scenario: No exact match
- **WHEN** `particular_resolve("auth timeout")` is called and no particular has that label or alias, though a semantic cache would rank one highly
- **THEN** it returns null
