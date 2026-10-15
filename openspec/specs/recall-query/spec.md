# Recall Query Specification

## Purpose

Defines `knowledge_recall` called with a free-text `query`: resolution to particulars followed by structural recall, the required model-free lexical baseline, the `resolution` marker on results, the optional semantic cache and its rules (derived, model-tagged, outside the workspace, never committed or published, never authoritative), the scope ceiling on remote embedding, and that `particular_resolve` stays exact.

## Requirements

### Requirement: Recall by query resolves to particulars, then recalls structurally
`knowledge_recall` called with `query` SHALL first resolve the query to a set of particulars, each taken with its merge equivalence class, and SHALL then return, for each, exactly what `knowledge_recall` called with that particular's id and the same `author`, `scope`, and `include_retracted` would return. Every object in the response SHALL come from this second stage. Within a particular the order SHALL be lineage order with `current` identified, as for recall by particular; resolution SHALL NOT reorder it. Objects whose `content` matched the query SHALL be marked as matched within their particular's results.

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

### Requirement: Each result says how it was resolved
Each particular in a recall-by-query response SHALL carry `resolution`, one of `label`, `alias`, `lexical`, or `semantic`: `label` or `alias` when the whole query equals the particular's label or one of its aliases under case folding; `lexical` when the baseline matched otherwise; `semantic` when only a semantic stage proposed it. A particular resolved more than one way SHALL carry the first applicable value in that order. When `limit` truncates, particulars SHALL be kept in that order of `resolution` before any other ordering.

#### Scenario: Exact alias
- **WHEN** a particular has alias `DKF` and the query is `dkf`
- **THEN** its `resolution` is `alias`

#### Scenario: Found both ways
- **WHEN** the baseline matches a particular's claim content and the semantic stage also proposes it
- **THEN** its `resolution` is `lexical`

#### Scenario: Limit keeps exact matches
- **WHEN** a query resolves one particular by `label` and five by `semantic`, and `limit` is 3
- **THEN** the `label` particular is in the response

### Requirement: A lexical baseline is required and always runs
Every implementation SHALL resolve a query, without a model, by matching it under Unicode case folding against particular labels and aliases and against claim and synthesis `content`, matching both the whole query and each whitespace-separated term as a substring. The baseline SHALL run on every recall by query, whether or not any other stage is available. Another stage MAY add particulars to the resolved set and SHALL NOT remove any the baseline found.

#### Scenario: No model available
- **WHEN** an implementation has no embedding model and `knowledge_recall(query: "Timeout")` is called on a workspace with a claim containing "timeout"
- **THEN** that claim's subject is resolved with `resolution: lexical`

#### Scenario: An identifier embeddings miss
- **WHEN** the query is a ticket number that appears verbatim in one claim and the semantic stage does not propose that claim's subject
- **THEN** the subject is resolved, because the baseline found it

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
