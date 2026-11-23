# standalone-conformance Specification

## Purpose

DKF is implementable from its own specification (README.md) alone: no field's value must be another format's identifier, no rule constrains another format, and a Conformance section states which text is normative, including that plain-prose rules in normative sections bind. Introduced by change `standalone-spec`.

## Requirements
### Requirement: No field requires another format's identifier
The specification SHALL define no field whose value must be an identifier of an object defined by another format. Where a field may hold such an identifier, as `source.document.ref` may hold an episode id or a claim may cite an intention, the field SHALL be defined in this format's own terms, and validation SHALL NOT resolve the identifier against another format.

#### Scenario: Validating with no sibling workspace
- **WHEN** a validator checks a DKF workspace with no intentions or episodes workspace present
- **THEN** it can decide whether every object is valid without resolving any reference to another format

#### Scenario: A document that is an episode
- **WHEN** a claim's `source.document.ref` is an episode id and no episodes workspace is available
- **THEN** the claim is valid, as for any document its reader cannot fetch

### Requirement: No rule constrains another format
The specification SHALL state no requirement on how another format is written, read or used. Where it describes how another format relates to DKF, the description SHALL be informative.

#### Scenario: What DKF requires of intentions
- **WHEN** a reader looks for what this specification requires of an intentions or episodes workspace
- **THEN** they find no requirement, only informative description

### Requirement: The Conformance section states what is normative
The specification SHALL contain a Conformance section after *The Approach*. The section SHALL:
- interpret capitalised key words per BCP 14;
- state that rules in plain prose in normative sections bind equally;
- list the normative sections, and those normative only for a stated kind of implementation;
- state that every other section is informative;
- state that the specification is complete on its own.

All text describing intentions, episodes or the family of formats SHALL be informative and SHALL place no requirement on a DKF implementation.

#### Scenario: Implementing DKF alone
- **WHEN** an implementor builds a writer, reader and validator from the normative sections only
- **THEN** the implementation conforms, with no intentions or episodes code, data or workspace

#### Scenario: A rule in lower case
- **WHEN** a normative section says a reader "must" accept a legacy alias
- **THEN** the rule binds, although the word is not capitalised

#### Scenario: Tools an implementation does not expose
- **WHEN** an implementation exposes no MCP tools
- **THEN** it can conform, and MCP Server Tools places no requirement on it

