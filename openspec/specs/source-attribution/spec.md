# Source Attribution Specification

## Purpose

Defines `source.author` and `source.document.author` as references to particulars — id, URI, or bare name, resolved leniently at read time and written as the URI by writers — the asserted-by and reported-from relations computed over merge classes, the rule that resolution never guesses, the generalisation of harness attribution to any resolved author, the `knowledge_recall` author filter, and the statement that attribution is disclosed with promotion rather than gated.

## Requirements

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
When the author of an object being written is a defined particular, the writer SHALL write that particular's `uri` as the `author` value, not its id. A writer SHALL resolve the value it is given as follows: an id that resolves to a particular is written as that particular's `uri`; an id that resolves to no particular SHALL be refused; a URI is written unchanged whether or not a local particular carries it; a bare name that resolves to exactly one particular is written as that particular's `uri`; a bare name that resolves to no particular is written unchanged; a bare name given explicitly by the caller that resolves to more than one particular SHALL be refused, listing the candidates; and a bare name taken from `defaults.source.author` or its equivalent that resolves to more than one particular SHALL be written unchanged. Writing the resolved `uri` freezes a resolution that was unambiguous at write time, so that a later particular sharing the alias does not make the object ambiguous retroactively.

#### Scenario: Default author resolves
- **WHEN** `dkf.yaml` has `defaults.source.author: ben`, one particular has alias `ben`, and `claim_assert` is called without an author
- **THEN** the written file carries the particular's `uri` as `source.author`

#### Scenario: Default author is ambiguous
- **WHEN** two particulars carry alias `ben` and `claim_assert` is called without an author
- **THEN** the written file carries `author: ben` unchanged

#### Scenario: Explicit author is ambiguous
- **WHEN** two particulars carry alias `ben` and `claim_assert` is called with `author: ben`
- **THEN** the call is refused and both candidates are reported, and no file is written

#### Scenario: Author given as an id
- **WHEN** `claim_assert` is called with `author: par_01a0…` naming an existing particular
- **THEN** the written file carries that particular's `uri`, not the id

#### Scenario: Author given as an unknown id
- **WHEN** `claim_assert` is called with `author: par_01a0…` naming no particular
- **THEN** the call is refused as not found, and no file is written

#### Scenario: Author given as a URI with no local particular
- **WHEN** `claim_assert` is called with `author: https://orcid.org/0000-0002-1825-0097` and no particular carries that `uri`
- **THEN** the written file carries the URI unchanged, and the object's author is reported as unresolved, not invalid

#### Scenario: A later alias does not reach back
- **WHEN** a claim was written with `author: https://github.com/benfortuna` and a second particular later gains alias `ben`
- **THEN** the claim is still asserted by the first particular, unambiguously

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
A bare name that matches more than one particular by label or alias SHALL resolve to none of them. `particular_resolve` SHALL report ambiguity, listing the candidates, rather than selecting one. Implementations SHALL report an ambiguous author reference as a fact about the corpus named `author_ambiguous`, in aggregate with its count and the candidates, and an unresolved author as a fact about the corpus named `author_unresolved`, in aggregate with its count; neither SHALL be reported per object, because the action that clears each is at the workspace and clears every occurrence at once.

#### Scenario: Ambiguous resolve
- **WHEN** `particular_resolve("ben")` is called and two particulars carry alias `ben`
- **THEN** it returns no match and reports both candidates

#### Scenario: Ambiguous authors in aggregate
- **WHEN** validation reads one hundred and seventy-two claims whose `author: ben` matches two particulars
- **THEN** it reports one `author_ambiguous` line carrying the count and both candidates, not one line per claim, and does not fail validation

#### Scenario: Unresolved authors in aggregate
- **WHEN** validation reads ninety claims whose `author: ben` matches no particular
- **THEN** it reports one `author_unresolved` line with the count, not ninety findings

#### Scenario: Aggregate is expandable
- **WHEN** a consumer asks which objects an `author_ambiguous` line covers
- **THEN** the implementation can list them, as for any aggregated condition

### Requirement: `knowledge_recall` filters by author
`knowledge_recall` SHALL accept an `author` parameter — an id, URI, label, or alias — and SHALL return the non-retracted objects asserted by or reported from that particular's merge class. Each result SHALL carry `relations`, a set containing `asserted`, `reported`, or both, according to which of the object's `source.author` and `source.document.author` resolved into the class; a result SHALL never carry an empty set. The parameter SHALL be combinable with `particular_id`, `scope`, and `include_retracted`.

#### Scenario: Everything Jane said
- **WHEN** `knowledge_recall(author: "jane")` is called
- **THEN** it returns claims asserted by Jane with `relations: [asserted]` and claims reported from Jane with `relations: [reported]`

#### Scenario: Both relations on one object
- **WHEN** Ben records a claim whose document is his own earlier remark, so that `source.author` and `source.document.author` both resolve to Ben's class, and `knowledge_recall(author: "ben")` is called
- **THEN** that result carries `relations: [asserted, reported]`

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

### Requirement: A person's particular is defined deliberately
Implementations SHALL NOT define a particular for a person as a side effect of `init`, of applying `defaults.source.author`, or of writing any object. A person's particular is created by an explicit `particular_define` with the URI the person chooses; until then their name is written unchanged and reported as unresolved.

#### Scenario: Initialising a workspace
- **WHEN** `init` is run with `--author ben`
- **THEN** `dkf.yaml` records the default and no `par_` file is created

#### Scenario: First claim with an undefined default author
- **WHEN** `claim_assert` is called in a workspace whose default author `ben` matches no particular
- **THEN** the file carries `author: ben`, and no particular is minted for it
