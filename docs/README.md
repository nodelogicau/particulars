# particulars.fyi

The landing page for Particulars: one hand-written HTML file, no build step, no
JavaScript, no external requests. Served by GitHub Pages from this `docs/`
directory on `main`, with the custom domain in `CNAME`.

## Deployment

Repository settings → Pages: source **Deploy from a branch**, branch `main`,
folder `/docs`, custom domain `particulars.fyi`, **Enforce HTTPS** once the
certificate is issued.

## DNS (at the registrar for particulars.fyi)

Apex `A` records, all four GitHub Pages addresses:

```
particulars.fyi.  A  185.199.108.153
particulars.fyi.  A  185.199.109.153
particulars.fyi.  A  185.199.110.153
particulars.fyi.  A  185.199.111.153
```

Optional: `www` as a `CNAME` to `nodelogicau.github.io` (GitHub redirects it to
the apex once the custom domain is set).

`blog.particulars.fyi` is deliberately left free — the separate
`particulars-website` repo (Cloudflare Pages) can claim it later without
touching these records.

## Updating the proof graph

Section 4 of `index.html` is a static SVG rendering of real output from
`particulars export --format mermaid --subject "Dialectical Knowledge Format"
--depth 1` against the (private) `particulars-knowledge` workspace. To refresh
it: re-run the export, redraw the SVG nodes/edges to match, confirm every
included node is organisation- or public-scoped, and update the generation date
in the caption.
