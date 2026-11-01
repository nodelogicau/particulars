# okf-comparison-page Specification

## Purpose
Defines the page at particulars.fyi/okf/ that compares particulars with Google Cloud's Open Knowledge Format: its framing by update model through a worked example, how the two formats compose, its scope and provenance statements, the version and last-checked stamp, the rule that every OKF statement rests on OKF's primary sources, and the self-containment, theming and accessibility constraints it shares with the landing page. It is the only place on the site whose own prose names a competing format.
## Requirements
### Requirement: Page location and identity
The site SHALL serve a comparison page from `docs/okf/index.html`, reachable at `https://particulars.fyi/okf/`. Its first mention of OKF SHALL give the full name "Open Knowledge Format" and its publisher (Google Cloud), and SHALL link to OKF's primary source.

#### Scenario: Page reachable
- **WHEN** a visitor requests `https://particulars.fyi/okf/`
- **THEN** the comparison page is served with a valid certificate

#### Scenario: No name confusion
- **WHEN** a visitor reads the first mention of OKF
- **THEN** it names Google Cloud's Open Knowledge Format and links to Google's own spec or repository, not to the Open Knowledge Foundation

### Requirement: Version and last-checked stamp
The page SHALL display, near its top, the OKF version it describes and the date its OKF content was last checked against primary sources.

#### Scenario: Stamp present
- **WHEN** a visitor opens the page
- **THEN** a line such as "Describes OKF v0.2 · last checked 2026-11-02", linking to the spec at the commit read is visible before the first comparison section

### Requirement: Primary sourcing
Every statement the page makes about OKF SHALL be verifiable against OKF's primary sources (Google's published spec or repository) at the stamped version. A statement verifiable only from secondary write-ups SHALL be omitted.

#### Scenario: Review against the spec
- **WHEN** a reviewer checks each OKF statement on the page against the primary source at the stamped version
- **THEN** every statement is supported, and each has a corresponding claim in the knowledge workspace citing that source with a verbatim quote and hash

### Requirement: Update-model framing by worked example
The page SHALL present the difference between OKF and DKF as a difference in update model, shown through one worked example of a single fact that changes. It SHALL show OKF's scheduled staleness (`status`/`stale_after`) and refresh-by-rewrite alongside DKF's contradiction-detected staleness and synthesis with recorded reasoning. It SHALL state that both formats store vendor-neutral plain files in git. The page SHALL NOT use a feature-checklist table or scoring.

#### Scenario: Worked example shows both fates
- **WHEN** a visitor reads the comparison section
- **THEN** the same fact is traced through both formats, showing where the reason for the change lives in each (git history for OKF; a synthesis citing the claims for DKF)

#### Scenario: No checklist
- **WHEN** the page is inspected
- **THEN** it contains no feature matrix, tick/cross table, or score

### Requirement: Composition section
The page SHALL include a section showing that the formats compose. A DKF claim cites an OKF concept with a verbatim quote and a document hash or commit-pinned URL. DKF validation reports document drift as a cue to re-read. OKF's `stale_after` signals when the citing claim is due for a re-check.

#### Scenario: Citation example
- **WHEN** a visitor reads the composition section
- **THEN** they see an example DKF claim citing an OKF concept with quote and hash, and an explanation of how each format's signal prompts a re-check of the other

### Requirement: Scope statement
The page SHALL state the scope of each format as its specification does. OKF fixes no taxonomy of concept types and can carry procedural concepts such as playbooks. DKF is semantic memory with provenance that deliberately excludes episodic and procedural memory. Neither format standardises episodic memory. Where OKF's scope is broader than DKF's, the page SHALL say so.

#### Scenario: Scope is not overstated
- **WHEN** a visitor reads the scope statement
- **THEN** it does not describe OKF as limited to data catalogs, it acknowledges that OKF can hold procedures DKF excludes, and it names episodic memory as standardised by neither

### Requirement: Accurate provenance contrast
The page SHALL NOT claim that OKF lacks provenance or per-statement attribution. Any provenance contrast SHALL be framed at the unit of change: immutable DKF claims that record who asserted them, versus OKF concepts rewritten in place without a structure for recording disagreement or the reasoning for a change.

#### Scenario: Attribution acknowledged
- **WHEN** a visitor reads any provenance comparison on the page
- **THEN** it acknowledges OKF's `sources`, footnote attribution, and `generated`/`verified` fields before stating the difference

### Requirement: Shared page constraints
The comparison page SHALL meet the same constraints as the landing page: a single self-contained HTML file with embedded CSS and a system font stack, no network request other than the page itself, no JavaScript required to render, inline theme-aware SVG for any diagram, no horizontal body scroll at a 360px viewport, semantic headings, text alternatives for diagrams, and WCAG AA contrast in light and dark themes. It SHALL link back to the landing page.

#### Scenario: No external requests
- **WHEN** the page loads and its network activity is inspected
- **THEN** the only request is for the page document itself

#### Scenario: Dark mode and narrow viewport
- **WHEN** the page is viewed with a dark `prefers-color-scheme` at a 360px viewport
- **THEN** all text and diagrams are legible, nothing is clipped, and the body does not scroll horizontally

