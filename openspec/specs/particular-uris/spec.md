# Particular URIs Specification

## Purpose

Defines what a particular's `uri` must guarantee (global uniqueness; resolvability only once published), the minting convention for unpublished particulars including the `urn:dkf:` namespace, and when a URI may change.
## Requirements
### Requirement: A particular's URI is globally unique and resolvable once published
The `uri` of a particular SHALL be globally unique. It is NOT required to be resolvable until the particular is published to `public` scope. Where a well-known global URI for the subject exists (e.g. Wikidata, ORCID, DOI, a GitHub URL), implementations SHALL prefer it over minting a new one.

#### Scenario: Defining an internal module
- **WHEN** an agent defines a particular for an internal service with no public URL
- **THEN** the particular is valid with a non-resolvable URI

### Requirement: URI minting convention
When `particular_define` is called without a `uri`, the implementation SHALL mint one as `<base-uri><slug>` if the workspace declares `workspace.base-uri`, and otherwise as `urn:dkf:<workspace-id>:<slug>`. `slug` SHALL be derived from the label by lower-casing, NFKD-folding and stripping combining marks, collapsing every run of characters outside `[a-z0-9]` to a single `-`, and trimming leading/trailing `-`. The `urn:dkf:` namespace is claimed by this specification for this purpose. A slug SHALL NOT by itself decide that two labels name the same particular; that is decided as *A minted URI resolves only to the particular it was minted for* requires.

If the slug is empty, the implementation SHALL NOT mint a URI. It SHALL refuse the call without creating or changing any file, and the refusal SHALL say that the label yields no slug and that an explicit `uri` is required. This check SHALL precede any lookup of the minted URI.

#### Scenario: Minting with a base URI
- **WHEN** the workspace has `base-uri: https://example.com/particulars/` and the label is `Project X`
- **THEN** the minted URI is `https://example.com/particulars/project-x`

#### Scenario: Minting without a base URI
- **WHEN** the workspace has no base URI, workspace id `0191…`, and label `Café Société`
- **THEN** the minted URI is `urn:dkf:0191…:cafe-societe`

#### Scenario: Same label across sessions
- **WHEN** `particular_define` is called without a `uri` with label `Project X`, and later called again without a `uri` with label `project x`
- **THEN** both calls resolve to the same particular and no duplicate is created

#### Scenario: A label of symbols only
- **WHEN** `particular_define` is called without a `uri` with label `#`
- **THEN** the call is refused, the refusal says an explicit `uri` is required, and no file is written

#### Scenario: A label in a script the slug drops
- **WHEN** `particular_define` is called without a `uri` with label `東京`
- **THEN** the call is refused and no file is written

#### Scenario: An explicit URI for such a label
- **WHEN** `particular_define` is called with label `東京` and `uri: https://www.wikidata.org/entity/Q1490`
- **THEN** the particular is created with that URI

#### Scenario: A label with some characters the slug keeps
- **WHEN** the workspace has no base URI, workspace id `0191…`, and `particular_define` is called without a `uri` with label `C 東京`
- **THEN** the minted URI is `urn:dkf:0191…:c`, and the call is subject to *A minted URI resolves only to the particular it was minted for*

### Requirement: URIs are immutable once published
A particular's `uri` MAY be changed only while the particular has never been published to `public` scope. After publication, two URIs SHALL be joined only by a merge record (see `merge-records`).

#### Scenario: Renaming an unpublished particular
- **WHEN** a particular with no published claims is redefined with a new URI
- **THEN** the change is permitted

#### Scenario: Renaming a published particular
- **WHEN** a particular that has been published is asked to change URI
- **THEN** the implementation refuses and directs the caller to `particular_merge`

### Requirement: The urn:dkf: namespace is deliberately unregistered at v0.1
The specification SHALL state that `urn:dkf:` is used as an unregistered URN namespace: its NID syntax conforms to RFC 8141, every minted URN embeds the workspace UUID so collision with any other use of the NID requires a UUID collision, and formal registration — which would change no identifier — MAY be pursued after v0.1. `base-uri` remains the recommended form for publishers.

#### Scenario: An implementer checks the namespace status
- **WHEN** an implementer looks up whether `urn:dkf:` is IANA-registered
- **THEN** the specification says it is not, that this is deliberate, and why it is safe

#### Scenario: Registration changes nothing
- **WHEN** the namespace is later registered
- **THEN** every existing URN remains valid unchanged

### Requirement: A minted URI resolves only to the particular it was minted for
When `particular_define` is called without a `uri` and the minted URI already names a particular, directly or through a merge record, the call SHALL resolve to that particular only if the supplied `label` equals, under Unicode case folding, the `label` or one of the `aliases` of a particular in that particular's merge class. The supplied `aliases` SHALL NOT count towards the match. Otherwise the implementation SHALL refuse the call without creating or changing any file. The refusal SHALL name the existing particular's `id`, `uri` and `label`, and SHALL say that a different thing requires an explicit `uri` and that the same thing can be referred to by its URI or id.

When such a call resolves to an existing particular, the implementation SHALL NOT change its `label`. It SHALL add each supplied alias the particular does not already carry and SHALL NOT remove any alias.

When `particular_define` is called with a `uri`, this requirement SHALL NOT apply: the call is idempotent on that URI and MAY change the particular's `label` and `aliases`.

#### Scenario: Same slug, different thing
- **WHEN** a particular with label `C` and minted URI `…:c` exists, and `particular_define` is called without a `uri` with label `C#`
- **THEN** the call is refused, the refusal names the particular labelled `C`, and no file is written

#### Scenario: A label differing only in diacritics
- **WHEN** a particular with label `Café` exists, and `particular_define` is called without a `uri` with label `Cafe`
- **THEN** the call is refused, naming the particular labelled `Café`

#### Scenario: Matching an existing alias
- **WHEN** a particular with label `C`, alias `C-lang` and URI `…:c-lang` exists, and `particular_define` is called without a `uri` with label `c-lang`
- **THEN** the call resolves to that particular and its label remains `C`

#### Scenario: An alias does not redirect a minted URI
- **WHEN** a particular with label `C`, alias `C-lang` and URI `…:c` exists, no particular is named by `…:c-lang`, and `particular_define` is called without a `uri` with label `C-lang`
- **THEN** a new particular is created at `…:c-lang`, since the minted URI names no particular and this requirement does not apply

#### Scenario: Supplied aliases do not steer the match
- **WHEN** a particular with label `C` exists, and `particular_define` is called without a `uri` with label `C#` and aliases `[C]`
- **THEN** the call is refused and no file is written

#### Scenario: Aliases are added, never removed
- **WHEN** a particular with label `Project X` and alias `ProjectX` exists, and `particular_define` is called without a `uri` with label `project x` and aliases `[project_x]`
- **THEN** the particular's label remains `Project X` and its aliases are `ProjectX` and `project_x`

#### Scenario: Explicit URI beside a minted one
- **WHEN** a particular with label `C` and minted URI `…:c` exists, and `particular_define` is called with label `C#` and `uri: https://www.wikidata.org/entity/Q2370`
- **THEN** a second particular is created, and the particular labelled `C` is unchanged

#### Scenario: Renaming through an explicit URI
- **WHEN** a particular with label `C` and minted URI `…:c` exists, and `particular_define` is called with that URI and label `C (language)`
- **THEN** the call resolves to that particular and MAY change its label to `C (language)`

