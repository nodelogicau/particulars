## Why

Google Cloud's Open Knowledge Format (OKF) and DKF are both vendor-neutral, plain-file knowledge formats kept in git and maintained by humans and agents. OKF's canonical home is `GoogleCloudPlatform/open-knowledge-format` (v0.2, Apache-2.0). Practitioners who meet one will ask how it differs from the other. Today particulars.fyi answers that only by category (the "Docs with expiry dates" card) and names no competitor, which is right for the landing page. The question that leaves open is recorded in the `particulars-knowledge` workspace's positioning synthesis: whether "a comparison or FAQ page" should name OKF. A separate page answers it in the project's own voice, so other people's write-ups don't answer it for us, and it keeps the landing page evergreen.

## What Changes

- Add a second static page, `docs/okf/index.html`, served at `particulars.fyi/okf/`. It explains how DKF and OKF differ in their **update model**: OKF schedules staleness in advance (`status`/`stale_after`) and refreshes by rewriting. DKF detects staleness when a contradicting claim arrives and reconciles it with a synthesis that keeps the reasoning.
- Show how the two **compose**: a DKF claim cites an OKF concept with a verbatim quote and a document hash (or a URL pinned to a commit), and OKF's `stale_after` signals when that claim is due for a re-check.
- Show the **scope difference** honestly. OKF fixes no taxonomy of concept types: it covers knowledge surrounding data and systems, and its own examples include tables, metrics, attested computations and playbooks (procedures). DKF is semantic memory with provenance, and it leaves procedural and episodic memory out of scope on purpose. Neither format standardises episodic memory.
- Stamp the page with the OKF version it describes and a "last checked" date. The page links to OKF's primary sources and makes no claim from secondary write-ups alone.
- Argue through one worked example (a single fact that changes, shown in both formats), not through a feature-checklist table.
- Add one link from the landing page to the comparison page. The link text names a category, not a product, so the landing page's own voice stays name-free.
- **Modified requirement**: the landing-page capability currently requires the site to be a single page. That requirement is relaxed so the site can include one comparison page alongside the landing page.

## Capabilities

### New Capabilities
- `okf-comparison-page`: the public page comparing DKF and OKF: its framing (update model, not a feature table), the composition pattern, the scope statement, version and last-checked stamping, sourcing rules, and the same self-containment, theming and accessibility constraints as the landing page.

### Modified Capabilities
- `landing-page`: the "Page narrative" requirement no longer means the whole site is a single page, and a requirement is added for a single, name-free link to the comparison page. "Category-based differentiation" still governs the landing page's own voice, unchanged.

## Impact

- `docs/okf/index.html` (new). `docs/index.html` gets one added link. `docs/README.md` notes the second page.
- No change to the format spec, the CLI or the hosting setup. GitHub Pages already serves everything under `docs/`.
- Ongoing upkeep: the page names an external spec that is still changing (v0.1 → v0.2 within about a month), so it needs a re-check whenever OKF publishes a new version.
- Knowledge workspace: once this is merged, record a claim that resolves the "comparison or FAQ page" item listed as unresolved in the positioning synthesis.
