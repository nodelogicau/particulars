## MODIFIED Requirements

### Requirement: Page narrative
The landing page SHALL present, in order: (1) a hero with the tagline "Knowledge that doesn't go stale" and the dialectic triad as its graphic, (2) a "one fact, two fates" panel contrasting how ordinary memory and particulars handle a fact that changes, (3) the human/agent collaboration loop in which everything an agent writes is a proposal until a human merges it, (4) proof drawn from the project's real workspace, and (5) a quickstart with links to the spec, the CLI, and the v0.1 release. The site MAY include separate pages besides the landing page (such as the OKF comparison page). The landing page's narrative SHALL NOT depend on them.

#### Scenario: Visitor absorbs the pitch from visuals alone
- **WHEN** a visitor scrolls the page reading only headlines, diagrams, and captions
- **THEN** they encounter the staleness promise, the contradiction-to-synthesis mechanism, the propose-review-merge loop, real workspace evidence, and how to install — in that order

#### Scenario: Dialectic is explained without jargon dependency
- **WHEN** the hero and section 2 introduce thesis, antithesis, and synthesis
- **THEN** each term is grounded by the concrete example in the diagrams, and no section assumes prior knowledge of Hegelian dialectic or of any file format

## ADDED Requirements

### Requirement: Category-worded link to the comparison page
The landing page SHALL contain exactly one link to the OKF comparison page, placed with the "Docs with expiry dates" category card. The link text SHALL name the category, not a product, so that it complies with the Category-based differentiation requirement.

#### Scenario: Link present and name-free
- **WHEN** the landing page is searched for links to `/okf/`
- **THEN** exactly one is found, beside the expiry-dates card, and neither its text nor its accessible name contains "OKF" or any other product name
