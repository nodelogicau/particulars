## MODIFIED Requirements

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
