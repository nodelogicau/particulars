## 1. Verify OKF against primary sources

- [x] 1.1 Locate Google's canonical OKF spec and repository. Record the URLs, the current version, and the v0.1/v0.2 release dates
- [x] 1.2 Confirm against the spec text: `status`/`stale_after` semantics, `generated`/`verified` trust tiers, refresh-by-rewrite, concept types, `log.md`, Attested Computation, and any stated scope or non-goals
- [x] 1.3 Record each confirmed OKF fact as a claim in `particulars-knowledge`, citing the primary source with a verbatim quote and hash. Retract or qualify any existing OKF claim the spec contradicts

## 2. Draft the comparison page

- [x] 2.1 Create `docs/okf/index.html`: copy the landing page's CSS tokens and base components inline, set the title, and add a header with a link back to `/`
- [x] 2.2 Add an intro with the full name, publisher and primary-source link, the version and last-checked stamp, and the "what both share" paragraph (plain files, git, humans and agents)
- [x] 2.3 Add the worked example (billing ownership, Priya → Ada, matching the landing page) traced through OKF and DKF as an inline, theme-aware SVG with a caption
- [x] 2.4 Add the composition section: an example DKF claim citing an OKF concept with quote and hash, drift reported by `validate`, and `stale_after` as the re-check cue
- [x] 2.5 Add the scope section: data catalog vs general semantic memory, and the memory kinds neither format standardises
- [x] 2.6 Cross-check every OKF statement on the page against the claims from 1.3. Cut anything without one

## 3. Link from the landing page

- [x] 3.1 Add one category-worded link to `/okf/` under the "Docs with expiry dates" card in `docs/index.html`
- [x] 3.2 Confirm the landing page's own prose and the link text still name no product (grep outside the proof-graph tooltips)
- [x] 3.3 Note the second page in `docs/README.md`, with the re-check-on-OKF-release upkeep

## 4. Verify

- [x] 4.1 Check the comparison page with network inspection (only the document request), with JavaScript disabled, at a 360px viewport, and in dark mode
- [x] 4.2 Run an accessibility pass: heading order, diagram captions or labels, AA contrast in both themes
- [x] 4.3 After merge, confirm `https://particulars.fyi/okf/` is served over HTTPS

## 5. Record the outcome

- [x] 5.1 Assert a claim in `particulars-knowledge` that the comparison page exists and names OKF only on `/okf/`, then write a synthesis that resolves the positioning synthesis's "comparison or FAQ page" unresolved item
