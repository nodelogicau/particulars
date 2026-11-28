## Why

People comparing DKF with an ontology-based approach (OWL/RDF, schema.org, SKOS) find nothing in the text about how the two relate. *Design Principles* says that entity types and ontologies are implementation concerns but doesn't say how an implementation that uses one should meet the format. Without that, exporters will each invent a mapping. The likely default, turning a claim's content into a bare triple, would drop the provenance and dialectic that set DKF apart. The two approaches answer different questions and complement each other, and the text should say where they meet.

## What Changes

- **A *Relation to Linked Data* section** after *Trust and Provenance*. It is informative throughout and covers:
  - **Shared identity:**
    - a particular's `uri` is already a linked-data node;
    - a non-retracted merge means what `owl:sameAs` means;
    - a particular has no type, because a type is a claim.
  - **Exporting claims as RDF:**
    - export the claim, not the triple it seems to state;
    - a table maps fields onto RDF, PROV-O, SKOS and `dcterms:subject`;
    - the dialectical fields have no standard term;
    - an export serves only what a feed would serve, and is linked with `describedby` under its own media type.
  - **Derived graphs:**
    - a graph built from a workspace is a view, with one named graph per claim;
    - reasoner inconsistency is the conflict the format already reports;
    - new conclusions become knowledge only as `inferred` claims with a `basis`.
  - **Importing from linked data:**
    - external statements become `observed` claims;
    - ontology constraints may inform conflict detection but never decide validity.
  - **Not adopted:** RDF or JSON-LD as the file format, and typed predicates in claims.
- ***Design Principles*:** "Minimal spec, layered implementation" links to the new section.
- ***References*:** a new group, *Vocabularies an export maps to*, lists RDF 1.1, PROV-O, SKOS, OWL 2, DCMI Metadata Terms and JSON-LD 1.1 as mapping targets, not sources of the format.
- **No format version.** No file is read differently and no file stops validating.

## Capabilities

### New Capabilities
- `linked-data-relation`: the specification states, informatively, how DKF relates to linked data and ontologies: shared identity, export, derived graphs, import, and what was not adopted.

### Modified Capabilities
None.

## Impact

- `README.md`: a new informative section, one sentence in *Design Principles*, and one group in *References*.
- `openspec/specs`: one capability added.
- Implementations: none. The mapping is guidance for exporters; nothing is required.

## Open question

DKF's own fields (`evidential`, `confidence`, `method`, `unresolved`, `context.scope`, `retracted`, `redacted`) have no standard RDF terms, and this change publishes no namespace. So that part of an export doesn't interoperate between exporters. Reserving a namespace would be a normative addition, and is left to a separate change.
