## Context

The slug is `[a-z0-9-]` by construction. Lower-casing, NFKD and stripping combining marks turn most Latin-script labels into ASCII, but anything in another script, and anything made only of symbols, is removed entirely:

| label | slug | minted URI, read literally |
|---|---|---|
| `#` | (empty) | `<base-uri>` or `urn:dkf:<id>:` |
| `東京` | (empty) | same |
| `Ωμέγα` | (empty) | same |
| `C 東京` | `c` | `<base-uri>c` |

`fix-slug-collisions` (#62) made a minted URI resolve only on a label or alias match. That stops the empty-slug labels merging into one particular, but leaves the first one owning a degenerate URI and every later one refused as a collision with it, which reads as a defect in the caller's label rather than in the minting rule.

## Goals / Non-Goals

**Goals:**
- No minted URI is the bare `base-uri` or ends in an empty URN segment.
- No URI already minted changes.
- The caller learns, in one refusal, what to do instead.

**Non-Goals:**
- Readable minted URIs for non-Latin labels. That needs a different slug (see D2) and its own change.
- Finding an existing particular by label when the slug is empty (see Open Questions).

## Decisions

### D1. Refuse a define whose label slugs to nothing

When `uri` is omitted and the slug is empty, the call is refused and nothing is written. The refusal says the label yields no slug and that an explicit `uri` is required. A global URI is often available for exactly these labels (`東京` has a Wikidata entity), and the spec already prefers one.

This is checked before the minted URI is looked up, so the refusal is the same whether or not a particular already holds the degenerate URI.

### D2. Alternatives rejected

- **Fall back to the particular's id** (`urn:dkf:<ws>:par_…`). Always unique, but a fresh id is minted on every call, so the same label defined in two sessions creates two particulars. Avoiding that needs a lookup by label first, which is the matching #62 already does, plus a URI that tells a reader nothing.
- **Keep letters from other scripts, as IRI characters (RFC 3987).** `東京` would mint `…:東京` and stay readable. But it changes the minted URI of every label that mixes scripts and slugs non-empty today (`Café 東京` is `cafe` now and would become `cafe-東京`), so an existing workspace's next define of such a label would mint a new URI and create a duplicate. It also means choosing which characters count as letters, normalising them, and saying how they percent-encode where only URIs are accepted. It is worth doing, as its own versioned change with an idempotency story.
- **Hash the label** (`…:x-3f2a…`). Deterministic and unique enough, but opaque, and the hash input would need its own normalisation rule — a second notion of "same label" beside case folding.

Refusal changes no URI that can be minted today and costs the caller one retry with a `uri`.

### D3. No format version

The change narrows when one write operation succeeds. Nothing in a file is read differently. A particular already carrying `urn:dkf:<id>:` or the bare `base-uri` stays valid.

## Risks / Trade-offs

- **[A whole script needs explicit URIs]** An agent working in Japanese or Greek can't mint at all. → The refusal says so directly, a global URI usually exists, and D2's IRI slug is the route to fixing it properly.
- **[An agent re-defines an empty-slug particular each session]** Having given `東京` a Wikidata URI, a later define of `東京` without a `uri` is refused rather than found. → The agent recalls it by query, which matches on label, and uses its URI.

## Open Questions

- Should the refusal name an existing particular whose label or alias matches under case folding, as the collision refusal does, so the retry is one call? It needs a label lookup that minting otherwise doesn't do.
