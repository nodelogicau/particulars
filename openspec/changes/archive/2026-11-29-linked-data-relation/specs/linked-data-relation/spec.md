## ADDED Requirements

### Requirement: The specification states its relation to linked data
The specification SHALL contain a *Relation to Linked Data* section after *Trust and Provenance* and before *Design Principles*. The section SHALL state that it is informative, SHALL contain no capitalised requirement keyword, and SHALL place no requirement on a writer, reader or validator. *Design Principles* SHALL link to it where it says that ontologies are implementation concerns.

#### Scenario: Implementing without linked data
- **WHEN** an implementor builds a conformant writer, reader and validator with no RDF support
- **THEN** nothing in *Relation to Linked Data* makes the implementation non-conformant

#### Scenario: Finding the section from the principle
- **WHEN** a reader reads "Minimal spec, layered implementation"
- **THEN** it links to *Relation to Linked Data*

### Requirement: Identity is shared through the particular's URI
The section SHALL state that a particular's `uri` is an IRI that joins DKF and RDF data, and that a non-retracted merge record means what `owl:sameAs` means. It SHALL state that a particular has no type and that a type is a claim.

#### Scenario: Typing a particular
- **WHEN** an implementation wants `rdf:type` for a particular
- **THEN** the section directs it to write a claim and derive the type from that claim, not to add a field to the particular's file

#### Scenario: Exporting a retracted merge
- **WHEN** an exporter writes merge records as `owl:sameAs`
- **THEN** the section says to write only the non-retracted ones

### Requirement: An export keeps the claim as its unit
The section SHALL state that a claim is exported as a resource whose fields are statements about it, never as the bare triple its content appears to state. It SHALL map each field with a standard counterpart to a term from RDF, RDFS, PROV-O, SKOS or DCMI Metadata Terms. It SHALL name the fields that have no standard term, and SHALL state that this specification publishes no RDF namespace.

#### Scenario: Who said it survives export
- **WHEN** a claim that Project X uses microservices is exported
- **THEN** the export still says who asserted it, from what, and when

#### Scenario: Withdrawn claims stay withdrawn
- **WHEN** an exporter drops `retracted` or `redacted`
- **THEN** the section says that a withdrawn claim has been turned back into a standing one

### Requirement: An export obeys feed scope
The section SHALL state that an RDF export serves only objects whose effective scope is `public`, and that it is linked with `describedby` under its own media type, distinguished from a manifest link by type.

#### Scenario: A private claim
- **WHEN** a claim's effective scope is `organisation`
- **THEN** no RDF export serves it

### Requirement: Derived graphs are views
The section SHALL state that a graph built from a workspace is rebuilt from the files and never written back to them, and that triples extracted from a claim go in a named graph identified by that claim. It SHALL state that an inconsistency found by a reasoner is evidence for a synthesis, not a defect in the graph. It SHALL state that a conclusion drawn by the graph becomes knowledge only when written as an `inferred` claim with a `basis`.

#### Scenario: A reasoner finds an inconsistency
- **WHEN** an OWL reasoner reports a graph built from every non-withdrawn claim as inconsistent
- **THEN** the section treats this as the conflict *Conflict semantics* already reports

### Requirement: Imports are claims
The section SHALL state that a statement read from a linked-data source is recorded as an `observed` claim citing the source in `source.document`. It SHALL state that ontology constraints may inform conflict detection but never decide validity.

#### Scenario: Wikidata disagrees
- **WHEN** an imported Wikidata statement disagrees with a local claim
- **THEN** both stand, the pair is `unsynthesised`, and neither overwrites the other

### Requirement: Rejected alternatives are recorded
The section SHALL state why RDF or JSON-LD was not adopted as the file format and why typed predicates are not required in claims. *References* SHALL list the vocabularies the section maps to as mapping targets, not as sources of the format.

#### Scenario: Asking why not JSON-LD
- **WHEN** a reader asks why object files are not JSON-LD
- **THEN** the section answers that a file must read without fetching a context, so the specification stands alone
