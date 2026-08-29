## 1. Content and diagrams

- [x] 1.1 Draft the page copy for all five sections (hero tagline + sub-headline, "one fact, two fates" labels and kicker, loop captions, proof caption, quickstart text, single MCP roadmap line), checking no competitor name and no calendar-format analogy appears
- [x] 1.2 Design the hero dialectic triad as inline SVG (thesis/antithesis → synthesis carrying reasoning and declared unresolved, feeding the next thesis), theme-aware via CSS custom properties
- [x] 1.3 Design the "one fact, two fates" panel as inline SVG: one everyday fact traced through ordinary memory (stale, silently wrong) vs particulars (challenge, synthesis with reasoning, current belief)
- [x] 1.4 Design the collaboration-loop diagram as inline SVG: agent recalls/asserts/synthesises on a branch → YAML files → PR review → human merge as acceptance
- [x] 1.5 Generate the proof graph: run `particulars export --format mermaid --subject "Dialectical Knowledge Format" --depth 1` against particulars-knowledge, render to static SVG, verify scope of every included node is organisation or public, caption with generation date and repo link

## 2. Page assembly

- [x] 2.1 Build `docs/index.html`: single file, embedded CSS, system font stack, semantic headings, light/dark via `prefers-color-scheme`, no JS, no external requests
- [x] 2.2 Make it responsive: `viewBox` + `max-width:100%` on all SVGs, wide diagrams in `overflow-x: auto` containers, verify at 360px with no body horizontal scroll
- [x] 2.3 Accessibility pass: text alternatives or captions for every diagram, heading hierarchy, WCAG AA contrast in both themes
- [x] 2.4 Add `docs/CNAME` containing `particulars.fyi` and an HTML comment in index.html noting how to regenerate the proof graph

## 3. Deployment

- [x] 3.1 Verify the page locally in light and dark themes, with JavaScript disabled, and confirm zero external network requests
- [x] 3.2 Verify quickstart commands verbatim against the released CLI (brew tap install, init, skill install, recall)
- [ ] 3.3 Commit and push `docs/`; enable GitHub Pages (source: main, folder: /docs) and set custom domain particulars.fyi
- [ ] 3.4 Confirm the page serves at the repository's github.io URL
- [ ] 3.5 Document and hand off registrar DNS records (four GitHub Pages apex A records for particulars.fyi; note that blog.particulars.fyi stays free for Cloudflare later); after DNS propagates, enable Enforce HTTPS and confirm https://particulars.fyi
