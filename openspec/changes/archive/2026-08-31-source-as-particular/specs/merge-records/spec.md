## MODIFIED Requirements

### Requirement: Merged particulars form an equivalence class for query tools
Non-retracted merge records SHALL be treated as symmetric and transitive. `knowledge_recall`, `conflict_detect`, and `lineage_trace`, when given any member of a class, SHALL operate over all particulars in that class. The asserted-by and reported-from relations defined in `source-attribution` SHALL likewise be computed over the class of the resolved author. Claims keep their original `subject` and their original `source` values.

#### Scenario: Recall across a merge
- **WHEN** `par_A` and `par_B` are merged and `knowledge_recall(par_A)` is called
- **THEN** claims whose `subject` is `par_B` are included in the result

#### Scenario: Transitive merge
- **WHEN** merges exist for (A, B) and (B, C)
- **THEN** `knowledge_recall(par_A)` includes claims about `par_C`

#### Scenario: Attribution across a merge
- **WHEN** a person's URN and ORCID are merged and `knowledge_recall(author: <ORCID>)` is called
- **THEN** objects whose `source.author` is the URN are included, and their files are unchanged
