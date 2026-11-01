## Context

particulars.fyi is one self-contained page (`docs/index.html`) served by GitHub Pages from `docs/`. The add-landing-page design (D3) chose to differentiate by category and never by name, and listed "named competitor comparisons" as a non-goal for *that page*. The workspace's positioning synthesis keeps that decision. It records the 2026-08-29 qualification that verbatim workspace knowledge may name OKF, and it lists as unresolved "whether the page's own prose ever names OKF (a comparison or FAQ page was mooted as the place)". This change settles that item: yes, on a separate page, and only there.

The primary source is `SPEC.md` in `GoogleCloudPlatform/open-knowledge-format`, read at commit `ad30107` (v0.2, sha256 `26aa5da0…`). It is byte-identical to the frozen copy in `GoogleCloudPlatform/knowledge-catalog/okf/`. v0.1 was published 2026-06-12 and v0.2 on 2026-07-24. Reading it first-hand corrected two beliefs drawn from secondary sources: OKF is not limited to data catalogs (it fixes no taxonomy, and its own example includes a `Playbook`), and it does attribute individual statements to sources (footnotes keyed to `sources[].id`).

## Goals / Non-Goals

**Goals:**

- Answer "how is this different from OKF?" in the project's own voice, accurately and generously.
- Lead with the update model, the one difference that holds at the document level, and show that the formats **compose** at the claim level.
- Make the page's own staleness visible: OKF version described and last-checked date.
- Leave the landing page's voice name-free and its narrative unchanged.

**Non-Goals:**

- Comparison pages for any other product, or a general "alternatives" hub.
- A feature-checklist table or scoring.
- Restating OKF's spec, beyond what the contrast needs.
- Arguing which format is "better". The page explains a difference and a composition.

## Decisions

**D1 — Separate page at `docs/okf/index.html` (served at `/okf/`).**
A directory index gives a clean URL without relying on GitHub Pages' extensionless `.html` resolution. Alternatives considered: a FAQ section on the landing page (breaks D3 and dates the evergreen page); a section in the spec README (the spec should describe DKF, not its neighbours); `particulars-website` blog post (dormant repo, and a post reads as a dated opinion, not reference).

**D2 — Argue by worked example, not by table.**
One fact traced through both formats, reusing the landing page's billing-ownership example (Priya → Ada) for continuity: in OKF the concept carries `stale_after`, someone rewrites it after the date passes, and the why survives only in git history. In DKF a contradicting claim arrives on the day the fact changes, and a synthesis cites both claims and records the reasoning and what remains unresolved. Tables invite feature-by-feature rebuttal and go stale with every version bump. A worked example argues the mechanism, which changes slowly.

**D3 — Composition is a full section, not a footnote.**
The workspace already holds the argument: OKF documents are mutable by design yet make sound DKF sources, because DKF never required immutable sources, only that mutation be detectable. Show a DKF claim citing an OKF concept with a verbatim quote plus a document hash (or a URL pinned to a commit), `validate` reporting drift as a cue to re-read, and OKF's `stale_after` acting as the cue to re-check the citing claim. This turns a competitor page into an interoperability page, and it is the most durable thing the page can say.

**D4 — Honest scope statement.**
A short section states each format's scope as its spec does. OKF covers "the metadata, context, and curated insight that surrounds data and systems" and fixes no taxonomy, so a bundle can hold tables, metrics, attested computations and playbooks (procedures). Its `log.md` is a prose history of edits to the bundle, not a record of world events. DKF is semantic memory with provenance and deliberately excludes episodic and procedural memory. Neither format standardises episodic memory. Where OKF is broader, the page says so. Being visibly fair builds trust with readers arriving from OKF.

**D4a — Provenance contrast is about assertion, not attribution.**
OKF attributes statements to sources (`sources` with credibility signals; per-statement footnotes keyed to `sources[].id`) and records who generated and verified each concept. The page does not claim OKF lacks provenance. The contrast is at the unit of change: a DKF claim is immutable, records who asserted it and how it is backed, and is never edited. An OKF concept is a document that agents rewrite in place ("agents constantly rewrite these documents", §5.1), and the spec defines no structure for recording a disagreement or the reasoning for a change.

**D5 — Version stamp and primary sourcing.**
A visible header line, "Describes OKF v0.2 · last checked YYYY-MM-DD", links to OKF's primary sources. Every statement about OKF must be verifiable against Google's spec or repository. Secondary write-ups may inform the page but are never its only basis. If a fact can't be confirmed first-hand, it is cut, not hedged.

**D6 — Reuse the landing page's visual system by copy, not by shared stylesheet.**
The landing-page spec requires self-contained pages with no external requests. The comparison page copies the needed CSS custom properties and components inline. That duplicates about a hundred lines of CSS but keeps both pages single-file and independently reviewable. Alternative considered: a shared `docs/site.css` (one extra request per page, and it changes the landing page's no-external-requests guarantee). Revisit if a third page appears.

**D7 — Landing page links by category.**
One link, worded by category (for example "How particulars compares to freshness-metadata formats →"), placed under the "Docs with expiry dates" card. The landing page's own voice still names no product. The OKF name first appears on the destination page.

**D8 — Back the page with workspace claims.**
Every OKF assertion on the page corresponds to a claim in `particulars-knowledge` that cites the primary source with quote and hash. Once merged, a new synthesis resolves the "comparison or FAQ page" item. The page dogfoods the composition it describes.

## Risks / Trade-offs

- [OKF changes and the page misdescribes it] → Version and last-checked stamp. A re-check task on each OKF release. Claims cite with quote and hash, so `validate` surfaces drift.
- [OKF converges toward updates that keep their reasoning, blunting the difference] → Already listed as unresolved in the synthesis. If it happens, the page is rewritten around composition alone, which holds either way.
- [Naming invites rebuttal from OKF's backers] → Generous tone, no scoring, composition-first. Factual errors are corrected publicly via a dated change note on the page.
- [Readers confuse Google's OKF with the Open Knowledge Foundation] → The first mention gives the full name and publisher, and links to Google's own page.
- [Duplicated CSS drifts from the landing page] → Accepted for two pages. D6 sets a third page as the trigger to revisit.

## Open Questions

- Exact wording of the landing page's link text. To settle at review.
