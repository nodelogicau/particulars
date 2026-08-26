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
When `particular_define` is called without a `uri`, the implementation SHALL mint one as `<base-uri><slug>` if the workspace declares `workspace.base-uri`, and otherwise as `urn:dkf:<workspace-id>:<slug>`. `slug` SHALL be derived from the label by lower-casing, NFKD-folding and stripping combining marks, collapsing every run of characters outside `[a-z0-9]` to a single `-`, and trimming leading/trailing `-`. The `urn:dkf:` namespace is claimed by this specification for this purpose.

#### Scenario: Minting with a base URI
- **WHEN** the workspace has `base-uri: https://example.com/particulars/` and the label is `Project X`
- **THEN** the minted URI is `https://example.com/particulars/project-x`

#### Scenario: Minting without a base URI
- **WHEN** the workspace has no base URI, workspace id `0191…`, and label `Café Société`
- **THEN** the minted URI is `urn:dkf:0191…:cafe-societe`

#### Scenario: Same label across sessions
- **WHEN** `particular_define` is called twice with labels that produce the same slug
- **THEN** both calls resolve to the same particular and no duplicate is created

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
