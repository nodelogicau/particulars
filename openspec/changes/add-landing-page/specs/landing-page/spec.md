## ADDED Requirements

### Requirement: Page narrative
The site SHALL consist of a single page presenting, in order: (1) a hero with the tagline "Knowledge that doesn't go stale" and the dialectic triad as its graphic, (2) a "one fact, two fates" panel contrasting how ordinary memory and particulars handle a fact that changes, (3) the human/agent collaboration loop in which everything an agent writes is a proposal until a human merges it, (4) proof drawn from the real public workspace, and (5) a quickstart with links to the spec, the CLI, and the live workspace.

#### Scenario: Visitor absorbs the pitch from visuals alone
- **WHEN** a visitor scrolls the page reading only headlines, diagrams, and captions
- **THEN** they encounter the staleness promise, the contradiction-to-synthesis mechanism, the propose-review-merge loop, real workspace evidence, and how to install — in that order

#### Scenario: Dialectic is explained without jargon dependency
- **WHEN** the hero and section 2 introduce thesis, antithesis, and synthesis
- **THEN** each term is grounded by the concrete example in the diagrams, and no section assumes prior knowledge of Hegelian dialectic or of any file format

### Requirement: Category-based differentiation
The page SHALL differentiate particulars against categories of knowledge tooling — current-state notes/wikis, vector memory, and documents with freshness/expiry metadata — and SHALL NOT name any competing product, project, or vendor.

#### Scenario: No competitor names appear
- **WHEN** the page text and diagram labels are searched
- **THEN** no competing product, format, or vendor name is present

#### Scenario: Expiry-date contrast is made
- **WHEN** the differentiation content is read
- **THEN** it states that scheduled freshness (expiry dates, refresh-by-overwrite) tells you when to doubt a document but not what is now true or why it changed, whereas particulars records the challenge and its reconciliation

### Requirement: Diagrams are inline, theme-aware SVG
All diagrams SHALL be hand-authored inline SVG styled via the page's CSS custom properties, rendering legibly in both light and dark themes, with diagram text as real SVG text elements. Wide diagrams SHALL scroll within their own container; the page body SHALL NOT scroll horizontally.

#### Scenario: Dark mode renders legibly
- **WHEN** the page is viewed with a dark `prefers-color-scheme`
- **THEN** every diagram and all text meet legible contrast against the dark background with no hard-coded light-theme colors bleeding through

#### Scenario: Narrow viewport
- **WHEN** the page is viewed at a 360px-wide viewport
- **THEN** no content is clipped, the body does not scroll horizontally, and any wide diagram scrolls inside its own container

### Requirement: Self-contained page
The page SHALL be a single HTML file with embedded CSS, using a system font stack, making no network request other than fetching the page itself, and requiring no build step or JavaScript to render.

#### Scenario: No external requests
- **WHEN** the page loads and its network activity is inspected
- **THEN** the only request is for the page document itself

#### Scenario: JavaScript disabled
- **WHEN** the page is loaded with JavaScript disabled
- **THEN** all content and diagrams render fully

### Requirement: Proof section uses genuine workspace output
Section 4 SHALL present a graph generated from the actual `particulars-knowledge` workspace via `particulars export --format mermaid`, rendered to static SVG, captioned with its generation date. Because that workspace is private, the caption SHALL link to the v0.1 release rather than the workspace repository, and every node shown SHALL be organisation- or public-scoped.

#### Scenario: Provenance of the proof graph
- **WHEN** a visitor inspects the proof section
- **THEN** the caption states the date the graph was generated, identifies it as the project's own workspace, and links to the v0.1 release — with no link that resolves to a 404 for a signed-out visitor

### Requirement: Quickstart matches the released install path
The quickstart SHALL list copy-pasteable commands that match the currently released installation method and CLI verbs (Homebrew tap install, workspace init, skill install, recall), and SHALL link to the spec repository, the CLI repository, and the live workspace.

#### Scenario: Commands work as printed
- **WHEN** a practitioner runs the quickstart commands verbatim on a machine with Homebrew
- **THEN** each command succeeds against the released CLI without modification

### Requirement: Remote MCP is a single roadmap line
The page SHALL mention remote MCP exactly once, as a roadmap status line (e.g. "Remote MCP: in design"), and SHALL NOT describe or promise MCP features.

#### Scenario: MCP mention is bounded
- **WHEN** the page is searched for MCP references
- **THEN** exactly one roadmap line appears, with no feature descriptions attached

### Requirement: Hosting on GitHub Pages with custom domain
The site SHALL be served by GitHub Pages from the `docs/` directory of the repository's default branch, with a `CNAME` file containing `particulars.fyi` and HTTPS enforced once DNS resolves. Required registrar records (four GitHub Pages apex A records) SHALL be documented in the repository.

#### Scenario: Page reachable at the custom domain
- **WHEN** DNS is configured and GitHub Pages is enabled with source main/docs and custom domain particulars.fyi
- **THEN** https://particulars.fyi serves the landing page with a valid certificate

#### Scenario: Page reachable before DNS lands
- **WHEN** GitHub Pages is enabled but registrar DNS is not yet configured
- **THEN** the page is served at the repository's github.io URL, so deployment does not block on the registrar

### Requirement: Accessibility
The page SHALL use semantic HTML with a heading hierarchy, provide text alternatives for every diagram (visible captions or accessible labels), and meet WCAG AA contrast in both themes.

#### Scenario: Screen reader pass
- **WHEN** the page is traversed with a screen reader
- **THEN** each section is announced via its heading and each diagram conveys its meaning through an accessible name or adjacent caption
