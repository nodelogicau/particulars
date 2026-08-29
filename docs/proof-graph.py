#!/usr/bin/env python3
"""Regenerate the proof-section SVG in index.html from a mermaid export.

Usage:
    particulars export --format mermaid \
        --subject "Dialectical Knowledge Format" --scope organisation > export.mmd
    python3 docs/proof-graph.py export.mmd docs/index.html

Renders the synthesis spine (oldest at the bottom, current on top) with
verbatim excerpts and full-text tooltips, each generation's claim inputs as a
counted cluster of squares (tooltips carry role + full claim text), and the
subject particular at the root. Ids are omitted by design. After running,
update the totals in the section-4 lead paragraph and the caption date.
"""
import re
import sys
from html import escape

SPINE_X, SPINE_W = 330, 310
CUR_X, CUR_W = 320, 330
ROW_PITCH, BOX_H, CUR_H = 136, 76, 104
SQ, GAP, COLS, SQ_RIGHT = 12, 6, 6, 220
ROLE_LABEL = {
    "thesis": "thesis",
    "antithesis": "antithesis",
    "thesis:qualifying": "qualifying",
    "antithesis:qualifying": "antithesis (qualifying)",
}


def wrap(text, width, lines):
    out, cur = [], ""
    for word in text.split():
        cand = f"{cur} {word}".strip()
        if len(cand) > width and cur:
            out.append(cur)
            cur = word
            if len(out) == lines:
                break
        else:
            cur = cand
    if len(out) < lines and cur:
        out.append(cur)
    return out  # truncation is marked by the emitter's closing ellipsis


def main(mmd_path, html_path):
    mmd = open(mmd_path).read()
    nodes = {}  # id -> (kind, label)
    for nid, br, label in re.findall(r'^  (n\d+)([\[(])"(.*?)"[\])]$', mmd, re.M):
        nodes[nid] = ("claim" if br == "[" else "synthesis", label)
    tips = dict(re.findall(r'^  click (n\d+) callback "(.*)"$', mmd, re.M))
    edges = re.findall(r"^  (n\d+) -->\|([a-z:]+)\| (n\d+)$", mmd, re.M)
    current = re.search(r"^  class (n\d+) current$", mmd, re.M).group(1)
    unsyn = re.findall(r"^  class (n\d+) unsynthesised$", mmd, re.M)
    if unsyn:
        sys.exit(f"unsynthesised nodes present ({unsyn}); this renderer draws a "
                 "fully reconciled graph — reconcile first or extend the script")

    # spine: follow synthesis->synthesis thesis edges back from current
    prev = {d: s for s, r, d in edges if nodes[s][0] == "synthesis"}
    spine = [current]
    while spine[-1] in prev:
        spine.append(prev[spine[-1]])
    clusters = {
        syn: [(s, r) for s, r, d in edges if d == syn and nodes[s][0] == "claim"]
        for syn in spine
    }

    total_claims = len([n for n, (k, _) in nodes.items() if k == "claim"])
    citations = sum(len(c) for c in clusters.values())
    print(f"spine: {len(spine)} generations; {total_claims} claims, "
          f"{citations} citations", file=sys.stderr)

    height = 40 + CUR_H + (len(spine) - 1) * ROW_PITCH + 92 + 54 + 20
    out = [f'<svg class="min600" viewBox="0 0 760 {height}" role="img" '
           'aria-labelledby="proof-title proof-desc">',
           '          <title id="proof-title">The workspace&rsquo;s full dialectic, '
           'at organisation scope</title>',
           f'          <desc id="proof-desc">A vertical chain of {len(spine)} '
           'syntheses, oldest at the bottom, each citing its predecessor as '
           'thesis and each reconciling a counted cluster of claims, down to the '
           'particular they are all about: the Dialectical Knowledge Format. '
           'Every node carries its full text as a tooltip.</desc>',
           '          <defs>',
           '            <marker id="ah4" viewBox="0 0 10 10" refX="9" refY="5" '
           'markerWidth="7" markerHeight="7" orient="auto-start-reverse">',
           '              <path d="M0,0 L10,5 L0,10 z" class="head"/>',
           '            </marker>',
           '          </defs>']

    def emit(s):
        out.append("          " + s)

    y = 40
    for i, syn in enumerate(spine):
        is_cur = syn == current
        bx, bw, bh = (CUR_X, CUR_W, CUR_H) if is_cur else (SPINE_X, SPINE_W, BOX_H)
        tip = escape(("synthesis · CURRENT — " if is_cur else
                      "synthesis — ") + tips[syn], quote=False)
        if not is_cur:
            emit(f'<path d="M485,{y} L485,{y - 54}" class="edge" marker-end="url(#ah4)"/>')
            emit(f'<text x="500" y="{y - 22}" class="lbl">thesis</text>')
        emit(f'<rect x="{bx}" y="{y}" width="{bw}" height="{bh}" rx="14" '
             f'class="{"box-accent" if is_cur else "box"}"><title>{tip}</title></rect>')
        head = ('<tspan class="accent-t">synthesis &middot; CURRENT</tspan>'
                if is_cur else "synthesis")
        emit(f'<text x="{bx + 22}" y="{y + 28}" class="lbl">{head}</text>')
        excerpt = tips[syn] if is_cur else nodes[syn][1].split("<br>", 1)[-1]
        excerpt = excerpt.rstrip("…").rstrip()
        lines = wrap(excerpt, 38, 3 if is_cur else 2)
        for j, line in enumerate(lines):
            q1 = "&ldquo;" if j == 0 else ""
            q2 = "&hellip;&rdquo;" if j == len(lines) - 1 else ""
            emit(f'<text x="{bx + 22}" y="{y + 50 + j * 18}" class="small">'
                 f'{q1}{escape(line, quote=False)}{q2}</text>')

        claims = clusters[syn]
        mid = y + bh // 2
        rows = [claims[k:k + COLS] for k in range(0, len(claims), COLS)]
        top = mid - (len(rows) * (SQ + GAP) - GAP) // 2
        for ri, r in enumerate(rows):
            x0 = SQ_RIGHT - (len(r) * (SQ + GAP) - GAP)
            for ci, (cn, role) in enumerate(r):
                ctip = escape(f"claim · {ROLE_LABEL[role]} — {tips[cn]}",
                              quote=False)
                emit(f'<rect x="{x0 + ci * (SQ + GAP)}" y="{top + ri * (SQ + GAP)}" '
                     f'width="{SQ}" height="{SQ}" class="clm"><title>{ctip}</title></rect>')
        emit(f'<text x="166" y="{top + len(rows) * (SQ + GAP) + 14}" '
             f'text-anchor="middle" class="lbl">{len(claims)} '
             f'claim{"s" if len(claims) != 1 else ""} cited</text>')
        emit(f'<path d="M232,{mid} L{bx - 5},{mid}" class="edge" marker-end="url(#ah4)"/>')
        y += (CUR_H if is_cur else BOX_H) + (ROW_PITCH - BOX_H)

    py = y
    emit(f'<path d="M485,{py} L485,{py - 46}" class="edge-dot" marker-end="url(#ah4)"/>')
    emit(f'<text x="500" y="{py - 18}" class="lbl">the subject of every claim above</text>')
    emit(f'<rect x="320" y="{py}" width="330" height="54" rx="27" class="box-par">'
         '<title>particular — Dialectical Knowledge Format '
         '(https://github.com/nodelogicau/particulars): the subject of every claim '
         'and synthesis in this graph.</title></rect>')
    emit(f'<text x="342" y="{py + 22}" class="lbl">particular</text>')
    emit(f'<text x="342" y="{py + 42}" class="small" font-weight="600">'
         'Dialectical Knowledge Format</text>')
    out.append("        </svg>")
    svg = "\n".join(out)

    html = open(html_path).read()
    new, n = re.subn(
        r'<svg class="min600" viewBox="0 0 760 \d+" role="img" '
        r'aria-labelledby="proof-title proof-desc">[\s\S]*?</svg>',
        svg.replace("\\", "\\\\"), html, count=1)
    assert n == 1, "proof svg not found"
    open(html_path, "w").write(new)
    print(f"wrote proof graph: {len(spine)} generations, {total_claims} claims, "
          f"{citations} citations, viewBox height {height}", file=sys.stderr)


if __name__ == "__main__":
    main(sys.argv[1], sys.argv[2])
