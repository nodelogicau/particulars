## ADDED Requirements

### Requirement: An author value is a particular reference
The value of `source.author` SHALL be one of: a particular id, a particular URI, or a bare name. Readers SHALL resolve an id by exact match, a URI by the particular's `uri` including through non-retracted merge records, and a bare name by label or alias. A value that resolves to no particular SHALL be treated as an opaque name that satisfies the `source` minimum, and SHALL be reported as unresolved rather than invalid.

#### Scenario: Author written as a URI
- **WHEN** a claim carries `source: {author: https://orcid.org/0000-0002-1825-0097}` and a particular with that `uri` exists
- **THEN** the claim is asserted by that particular

#### Scenario: Author written as a bare name that matches an alias
- **WHEN** a claim carries `source: {author: ben}` and exactly one particular has label or alias `ben`
- **THEN** the claim is asserted by that particular

#### Scenario: Author written as a bare name with no match
- **WHEN** a claim carries `source: {author: ben}` and no particular has label or alias `ben`
- **THEN** the claim is valid, satisfies the source minimum, and is reported as having an unresolved author

#### Scenario: Existing workspace becomes attributable
- **WHEN** a particular with alias `ben` is defined in a workspace whose earlier claims carry `author: ben`
- **THEN** those claims are asserted by the new particular without any file being modified

### Requirement: Writers prefer the URI of a defined particular
When the author of an object being written is a defined particular, the writer SHALL write that particular's `uri` as the `author` value, not its id. When a writer is given a bare name, including from `defaults.source.author`, that resolves to exactly one particular, it SHALL write that particular's `uri`; on zero or several matches it SHALL write the name unchanged.

#### Scenario: Default author resolves
- **WHEN** `dkf.yaml` has `defaults.source.author: ben`, one particular has alias `ben`, and `claim_assert` is called without an author
- **THEN** the written file carries the particular's `uri` as `source.author`

#### Scenario: Default author is ambiguous
- **WHEN** two particulars carry alias `ben` and `claim_assert` is called without an author
- **THEN** the written file carries `author: ben` unchanged

#### Scenario: Author given as an id
- **WHEN** `claim_assert` is called with `author: par_01a0…` naming an existing particular
- **THEN** the written file carries that particular's `uri`, not the id

### Requirement: Asserted-by and reported-from are distinct relations over merge classes
An object SHALL be **asserted by** the particular its `source.author` resolves to, and **reported from** the particular its `source.document.author` resolves to. Both relations SHALL be computed over the merge equivalence class of the resolved particular. Implementations SHALL NOT collapse the two relations into one when reporting.

#### Scenario: Recorded testimony
- **WHEN** a claim carries `source.author` resolving to Ben and `source.document.author` resolving to Jane
- **THEN** the claim is asserted by Ben and reported from Jane, and neither is reported as the other

#### Scenario: Attribution across a merge
- **WHEN** `urn:dkf:…:jane` and `https://orcid.org/…` are merged and a claim's `document.author` is the URN
- **THEN** a query for objects reported from the ORCID includes the claim

#### Scenario: Self-report
- **WHEN** a claim's `subject` and `source.author` resolve to the same particular
- **THEN** the claim is both about and asserted by that particular, and nothing is reported as an error

### Requirement: Resolution never guesses
A bare name that matches more than one particular by label or alias SHALL resolve to none of them. `particular_resolve` SHALL report ambiguity, listing the candidates, rather than selecting one. Implementations SHALL report an ambiguous author reference as a per-object finding named `author_ambiguous`, and an unresolved author as an aggregate fact about the corpus.

#### Scenario: Ambiguous resolve
- **WHEN** `particular_resolve("ben")` is called and two particulars carry alias `ben`
- **THEN** it returns no match and reports both candidates

#### Scenario: Ambiguous author on a claim
- **WHEN** validation reads a claim whose `author: ben` matches two particulars
- **THEN** it reports `author_ambiguous` on that claim naming both candidates, and does not fail validation

#### Scenario: Unresolved authors in aggregate
- **WHEN** validation reads ninety claims whose `author: ben` matches no particular
- **THEN** it reports one aggregate line with the count, not ninety findings

### Requirement: `knowledge_recall` filters by author
`knowledge_recall` SHALL accept an `author` parameter — an id, URI, label, or alias — and SHALL return the non-retracted objects asserted by or reported from that particular's merge class, each result labelled with which relation matched. The parameter SHALL be combinable with `particular_id`, `scope`, and `include_retracted`.

#### Scenario: Everything Jane said
- **WHEN** `knowledge_recall(author: "jane")` is called
- **THEN** it returns claims asserted by Jane and claims reported from Jane, each labelled `asserted` or `reported`

#### Scenario: Jane on one subject
- **WHEN** `knowledge_recall(particular_id: par_X, author: "jane")` is called
- **THEN** it returns only objects whose subject is in X's class and which are asserted by or reported from Jane

### Requirement: Asserter attribution generalises harness attribution
The retraction-kind observation defined for `source.harness` SHALL apply to any resolved author: a `defect` counts against the asserting particular, a `provenance-failure` counts against the cited document and against the resolved `document.author` where one exists, and a `supersession` counts against nothing. Implementations MAY report these counts per particular.

#### Scenario: Defect on an asserted claim
- **WHEN** a claim asserted by Ben is retracted with `kind: defect`
- **THEN** the defect is attributable to Ben and to the harness, and not to the claim's `document.author`

#### Scenario: Provenance failure on reported testimony
- **WHEN** a claim reported from Jane is retracted with `kind: provenance-failure`
- **THEN** the failure is attributable to Jane, and other claims reported from Jane are identifiable as candidates for review

### Requirement: Attribution is disclosed with promotion
The specification SHALL state that promoting an object discloses its `source.author` URI with it, and that a `document.author` discloses who is being quoted as completely as a `quote` discloses what was said. Implementations SHALL NOT reject a promotion on that basis. A person's particular SHALL carry the URI under which they are willing to be cited at the widest scope their claims may reach.

#### Scenario: Promoting reported testimony
- **WHEN** a claim carrying `document.author` resolving to Jane is promoted to `public`
- **THEN** the specification tells the promoter that Jane's URI is published with it, and the promotion proceeds

#### Scenario: Particular files are not served
- **WHEN** a public consumer fetches a claim whose `author` is a URI
- **THEN** it learns the URI and nothing else about the particular, because particular files are not in any feed
