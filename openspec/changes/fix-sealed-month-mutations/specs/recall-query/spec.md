## MODIFIED Requirements

### Requirement: A semantic cache is optional, derived, and never authoritative
An implementation MAY keep a cache of embeddings of particular labels and aliases and of claim and synthesis `content`, and MAY use it to propose particulars in the resolution stage. The cache SHALL be fully regenerable from the workspace files. It SHALL record the identifier of the model that produced it and SHALL NOT be consulted when that differs from the model in use. It SHALL be stored outside the workspace directory tree, SHALL NOT be committed, and SHALL NOT be published or served to consumers. Validators and drift checks SHALL NOT read it. A missing, partial, or stale cache SHALL NOT cause an object to be returned that recall by particular would not return; it MAY cause a particular to be unresolved that a complete cache would have proposed. Because an embedding can disclose the text it was computed from, an implementation SHALL NOT consult an embedding of a field that has since been redacted, and SHALL delete it no later than the next update of the cache; content-redacted objects are identified for this from the index's `redacted` lists. Because a particular's `label` and `aliases` may be updated in place and the index does not mirror them, the cache SHALL record, for each vector of a label or alias, the text it embedded or a hash of that text. It SHALL NOT consult a vector whose recorded text is no longer the particular's label or one of its aliases, and SHALL recompute or delete that vector no later than the next update of the cache. Claim and synthesis vectors need no such record, because their `content` never changes except by redaction.

#### Scenario: Missing cache
- **WHEN** the cache has been deleted and `knowledge_recall(query)` is called
- **THEN** the response is the baseline's, every result's `resolution` is `label`, `alias`, or `lexical`, and no error is raised

#### Scenario: Model changed
- **WHEN** the cache records model `m1` and the implementation is now configured with `m2`
- **THEN** the cache is not consulted until rebuilt under `m2`

#### Scenario: Retraction after embedding
- **WHEN** a claim was embedded and has since been retracted, and recall by query is called with `include_retracted: false`
- **THEN** the claim is not in the response, and the cache did not have to be updated for this to hold

#### Scenario: Redaction after embedding
- **WHEN** a claim's `content` was embedded and has since been redacted, and the cache is next updated
- **THEN** the claim's vector is deleted from the cache, and before that update it was never consulted

#### Scenario: An alias removed after embedding
- **WHEN** a particular's alias `pX` was embedded and `particular_define` has since removed it, and recall by query is called before the cache is next updated
- **THEN** the vector for `pX` is not consulted, so no query resolves to the particular through `pX`, and the next update deletes that vector

#### Scenario: A label changed after embedding
- **WHEN** a particular's `label` has changed since its vector was computed
- **THEN** the next update of the cache recomputes that vector, although the index records no change to the particular

#### Scenario: Not in the published tree
- **WHEN** a publisher serves its workspace directory over HTTP
- **THEN** no embedding data is reachable under it

#### Scenario: Incremental update
- **WHEN** an object is added to a workspace whose cache was complete under the current model
- **THEN** bringing the cache up to date requires embedding only that object, identified from ids present in the index and absent from the cache

