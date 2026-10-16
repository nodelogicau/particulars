# Format Purpose Specification

## Purpose

Defines what the specification states about its own purpose and scope: that DKF is semantic memory that keeps its provenance, with provenance as its distinguishing value and the dialectic as what provenance makes possible; that it is the retrospective layer beside intentions, coupled through shared particular URIs only; and that episodic and procedural memory are outside the format.

## Requirements

### Requirement: The specification states its purpose before its mechanism
The specification SHALL include a *Purpose* section after *The Problem* and before *The Approach*, stating that DKF is semantic memory that keeps its provenance: beliefs about things in the world, each claim recording who asserted it, through which harness, from what, and how it is backed. The section SHALL identify provenance as the format's distinguishing value and SHALL present the dialectic as what provenance makes possible. The section SHALL be non-normative: it SHALL contain no requirement keyword, and no reader, writer, or validator behaviour SHALL depend on it.

#### Scenario: A reader meets the purpose first
- **WHEN** a reader reads the README from the top
- **THEN** they learn that DKF is semantic memory that keeps its provenance before any section describes the dialectic or an object type

#### Scenario: Provenance leads
- **WHEN** a reader asks what sets DKF apart from other agent memory
- **THEN** *Purpose* answers provenance, and *The Approach* connects the dialectic to it

#### Scenario: Purpose is not normative
- **WHEN** the *Purpose* section is searched for MUST, SHALL, SHOULD, or MAY
- **THEN** none is found

### Requirement: The specification states its relationship to intentions
The *Purpose* section SHALL state that DKF is the retrospective layer, what is known, and that intentions is the prospective layer, what a person means to do. It SHALL state that the two are coupled only through the URIs of the particulars they share, that either may cite the other informally, and that neither validates the other. The *References* entry for intentions SHALL point to *Purpose* rather than restate the relationship.

#### Scenario: The relationship in one place
- **WHEN** a reader looks for how DKF relates to intentions
- **THEN** *Purpose* states it, and the *References* entry links there

#### Scenario: No resolved link implied
- **WHEN** a reader reads *Purpose*'s account of the coupling
- **THEN** nothing in it implies that a DKF validator resolves an intentions reference, or the reverse

### Requirement: The specification states what is outside its scope
The *Purpose* section SHALL state that episodic memory and procedural memory are outside the format: that an event may be a particular with claims made about it while a log of episodes is not the format's job, and that how an agent does things belongs to skills and prompts, the conventions document addressing an agent without constraining anything. It SHALL leave open that either may be addressed by a separate specification.

#### Scenario: An event recorded as knowledge
- **WHEN** a reader wants to record that a certificate was renewed on a given day
- **THEN** *Purpose* tells them the event may be a particular with a claim about it, and that DKF is not a log of episodes

#### Scenario: A procedure
- **WHEN** a reader asks whether DKF stores how an agent should perform a task
- **THEN** *Purpose* tells them that belongs to skills and prompts, outside the format

#### Scenario: Future specifications not foreclosed
- **WHEN** a reader reads the scope statement
- **THEN** it does not say episodic or procedural memory will never be specified
