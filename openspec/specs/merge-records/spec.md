# Merge Records Specification

## Purpose

Defines the merge record written by `particular_merge`: its file location and fields, the equivalence-class semantics query tools apply across merged particulars, its retractability, and its place alongside the three knowledge objects.

## Requirements

### Requirement: Merge records are a defined record type
A merge SHALL be stored as `merges/mrg_<uuidv7>.yaml` with `id`, `type: merge`, `uris` (exactly two URIs), `source` (see `source-provenance`), `timestamp`, and optional `reason`. The file SHALL be listed in `index.yaml` with `id`, `type`, and `uris`. Merge records SHALL NOT rewrite, move, or modify any claim, synthesis, or particular.

#### Scenario: Declaring a merge
- **WHEN** `particular_merge(uri_a, uri_b, source)` is called
- **THEN** a file `merges/mrg_….yaml` is created with `uris: [uri_a, uri_b]`, `source`, and `timestamp`, and no existing file other than `index.yaml` changes

#### Scenario: Malformed merge
- **WHEN** a merge record lists one URI or three URIs
- **THEN** validation fails

### Requirement: Merged particulars form an equivalence class for query tools
Non-retracted merge records SHALL be treated as symmetric and transitive. `knowledge_recall`, `conflict_detect`, and `lineage_trace`, when given any member of a class, SHALL operate over all particulars in that class. Claims keep their original `subject`.

#### Scenario: Recall across a merge
- **WHEN** `par_A` and `par_B` are merged and `knowledge_recall(par_A)` is called
- **THEN** claims whose `subject` is `par_B` are included in the result

#### Scenario: Transitive merge
- **WHEN** merges exist for (A, B) and (B, C)
- **THEN** `knowledge_recall(par_A)` includes claims about `par_C`

### Requirement: Merge records are retractable
A merge record MAY carry a `retracted` block as defined in `retraction`. A retracted merge SHALL contribute no edge to the equivalence class.

#### Scenario: Retracting a wrong merge
- **WHEN** the (A, B) merge is retracted
- **THEN** `knowledge_recall(par_A)` no longer includes claims about `par_B`, and the merge file remains on disk with its `retracted` block

### Requirement: The core is three knowledge objects plus records
The specification SHALL state that particular, claim, and synthesis are the complete set of knowledge objects, and that retraction and merge are records — events about objects rather than knowledge — which are the only other constructs the format defines.

#### Scenario: Naive consumer
- **WHEN** a consumer implements only the three knowledge objects and ignores `/merges/`
- **THEN** it still reads every claim and synthesis correctly, merely without cross-particular unification
