## Why

DKF v0.1 is declared and released, but the project has no public web presence: particulars.fyi has no DNS records, and the only entry point is a 1100-line spec README written for implementers. Practitioners — people who would use the CLI with an AI harness today, and remote MCP later — need a digestible, visual introduction to what particulars is and why its knowledge doesn't go stale.

## What Changes

- Add a static, single-page landing site served from `docs/` in this repository via GitHub Pages, with the custom domain `particulars.fyi`.
- The page introduces dialectical knowledge management for a practitioner audience: staleness-led hook ("Knowledge that doesn't go stale"), the dialectic as the mechanism, the human/agent collaboration loop, proof via the real public workspace, and a CLI quickstart.
- Visuals-first: hand-authored inline SVG diagrams (theme-aware), no JS frameworks, no build step, no external assets.
- Differentiation is by category (notes/wikis, vector memory, docs with expiry dates), never by competitor name.
- GitHub Pages configuration: `CNAME` file, apex-domain DNS documented (A records to GitHub Pages IPs), leaving `blog.particulars.fyi` free for the separate `particulars-website` repo on Cloudflare later.
- Remote MCP appears only as a single roadmap line ("in design") — no promised features.

## Capabilities

### New Capabilities

- `landing-page`: the public single-page website — its content narrative, visual requirements, accessibility/theme behaviour, and GitHub Pages hosting/domain requirements.

### Modified Capabilities

None — no DKF format capability changes; this is a publishing surface for the existing spec.

## Impact

- New files under `docs/` (index.html, CNAME); no changes to the spec text or any format capability.
- Repository settings: GitHub Pages must be enabled (deploy from `main` / `docs/`); custom domain set to particulars.fyi.
- External: DNS records for particulars.fyi must be created at the registrar (manual step, documented in tasks).
- No dependencies, no build tooling, no CI required.
