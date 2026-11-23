## MODIFIED Requirements

### Requirement: The specification states its relationship to intentions
The *Purpose* section SHALL state, before it describes any other format, that DKF is complete on its own and can be adopted without any other format. It SHALL then state that DKF is one of a family of formats each of which stands alone, that DKF is the retrospective layer, what is known, and that intentions is the prospective layer, what a person means to do. It SHALL state that the two are coupled only through the URIs of the particulars they share, that either may cite the other informally, and that neither validates the other. The *References* entry for intentions SHALL point to *Purpose* rather than restate the relationship.

#### Scenario: The relationship in one place
- **WHEN** a reader looks for how DKF relates to intentions
- **THEN** *Purpose* states it, and the *References* entry links there

#### Scenario: No resolved link implied
- **WHEN** a reader reads *Purpose*'s account of the coupling
- **THEN** nothing in it implies that a DKF validator resolves an intentions reference, or the reverse

#### Scenario: Standing alone comes first
- **WHEN** a reader reads *Purpose* from the top
- **THEN** they learn that DKF is complete on its own before any other format is named
