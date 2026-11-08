#!/usr/bin/env python3
"""Draw the policymemo.ai mark and the nine skill icons as inked SVG.

There is no mascot. The mark is a plain ink burst beside the name "policymemo.ai".
Each skill icon shows the analytical move, in ink, with one red mark for the
thing that matters.

Every shape is drawn as a clean stroke or polygon, then its outline is roughened
with smooth noise so it reads as printed ink rather than vector. The noise is
seeded, so a rebuild changes nothing unless a drawing changes.

    python3 tools/build-marks.py

Writes docs/mark.svg (the logo), docs/favicon.svg and docs/icons/<icon>.svg.
Requires shapely (pip install shapely).
"""
import math
import pathlib
import random

from shapely.geometry import LineString, MultiPolygon, Point, Polygon
from shapely.ops import unary_union

ROOT = pathlib.Path(__file__).resolve().parent.parent
RED = "#C42B2E"
INK = "#1c1b18"


# ---- drawing helpers --------------------------------------------------------

def stroke(points, w):
    return LineString(points).buffer(w / 2, cap_style="round", join_style="round", quad_segs=8)


def dot(x, y, r):
    return Point(x, y).buffer(r, quad_segs=10)


def curve(fn, n=60):
    return [fn(i / n) for i in range(n + 1)]


def bezier(p0, p1, p2, p3):
    def at(t):
        u = 1 - t
        return (u**3 * p0[0] + 3 * u * u * t * p1[0] + 3 * u * t * t * p2[0] + t**3 * p3[0],
                u**3 * p0[1] + 3 * u * u * t * p1[1] + 3 * u * t * t * p2[1] + t**3 * p3[1])
    return curve(at)


def dashes(x0, x1, y, dash, gap, w):
    out, x = [], x0
    while x < x1 - 0.1:
        out.append(stroke([(x, y), (min(x + dash, x1), y)], w))
        x += dash + gap
    return unary_union(out)


# ---- ink --------------------------------------------------------------------

class Ink:
    """Roughens outlines with smooth noise along their length."""

    def __init__(self, seed, amp, scale):
        self.rng = random.Random(seed)
        self.amp, self.scale = amp, scale

    def ring(self, coords):
        pts = list(coords)[:-1]
        dense = []
        for a, b in zip(pts, pts[1:] + pts[:1]):
            n = max(1, int(math.dist(a, b) / self.scale))
            dense += [(a[0] + (b[0] - a[0]) * i / n, a[1] + (b[1] - a[1]) * i / n) for i in range(n)]
        waves = [(self.rng.uniform(0.15, 0.6), self.rng.uniform(0, 6.3), self.rng.uniform(0.3, 1))
                 for _ in range(4)]
        out, s = [], 0.0
        for i, p in enumerate(dense):
            q = dense[(i + 1) % len(dense)]
            r = dense[i - 1]
            s += math.dist(r, p)
            tx, ty = q[0] - r[0], q[1] - r[1]
            ln = math.hypot(tx, ty) or 1
            nx, ny = -ty / ln, tx / ln
            off = sum(a * math.sin(s * f + ph) for f, ph, a in waves) / 2.2
            off += self.rng.uniform(-0.35, 0.35)
            out.append((p[0] + nx * off * self.amp, p[1] + ny * off * self.amp))
        return out

    def path(self, geom):
        polys = geom.geoms if isinstance(geom, MultiPolygon) else [geom]
        d = []
        for poly in polys:
            for ring in [poly.exterior, *poly.interiors]:
                pts = self.ring(ring.coords)
                d.append("M" + " ".join(f"{x:.1f} {y:.1f}" for x, y in pts) + "Z")
        return "".join(d)


def svg(view, layers, seed, amp=0.55, scale=1.2, title=None, extra=""):
    ink = Ink(seed, amp, scale)
    body = ""
    for fill, geom in layers:
        body += f'<path fill="{fill}" fill-rule="evenodd" d="{ink.path(geom)}"/>'
    t = f"<title>{title}</title>" if title else ""
    return f'<svg xmlns="http://www.w3.org/2000/svg" viewBox="{view}">{t}{extra}{body}</svg>\n'


# ---- the mark: an ink burst ------------------------------------------------
# Keep it jagged and inky. A smooth, rounded burst drifts toward the Claude logo.

def mark_layers(points=18, outer=46, inner=33):
    pts = []
    for i in range(2 * points):
        r = outer if i % 2 == 0 else inner
        a = math.pi * i / points - math.pi / 2
        pts.append((50 + r * math.cos(a), 50 + r * math.sin(a)))
    return [(INK, Polygon(pts))]


def write_mark():
    layers = mark_layers()
    view = "0 0 100 100"
    (ROOT / "docs" / "mark.svg").write_text(
        svg(view, layers, seed=3, amp=0.7, scale=1.0, title="policymemo.ai"), encoding="utf-8")
    # The favicon: the same drawing, ink turned to paper in dark mode.
    style = (f"<style>.i{{fill:{INK}}}@media (prefers-color-scheme:dark){{.i{{fill:#f6f4ee}}}}</style>")
    s = svg(view, layers, seed=3, amp=0.7, scale=1.0, extra=style).replace(f'fill="{INK}"', 'class="i"')
    (ROOT / "docs" / "favicon.svg").write_text(s, encoding="utf-8")


# ---- the nine skill icons ---------------------------------------------------
# All drawn in a 100 x 80 box. Ink first, then the one red mark.

W = 6  # line weight


def problem():
    # A scribbled tangle, with one straight red line pulled out of it.
    tau = 2 * math.pi
    knot = curve(lambda t: (24 + 10 * math.sin(3 * t * tau + 0.5) + 3.5 * math.sin(7 * t * tau),
                            40 + 11 * math.sin(2 * t * tau) + 3.5 * math.cos(5 * t * tau)), 240)
    x0 = max(x for x, _ in knot) - 4
    return [(INK, stroke(knot, 3.6)),
            (RED, unary_union([stroke([(x0, 40), (82, 40)], W), dot(86, 40, 5)]))]


def stakeholders():
    # Actors of different weight, tied together; one holds the deciding position.
    a, b, c, d = (30, 18), (16, 62), (58, 58), (84, 40)
    links = unary_union([stroke([a, b], 4), stroke([b, c], 4), stroke([a, c], 4), stroke([c, d], 4)])
    ink = unary_union([links, dot(*a, 8), dot(*b, 6), dot(*c, 5)])
    return [(INK, ink.difference(dot(*d, 12))), (RED, dot(*d, 10))]


def evidence():
    # Known, inferred, assumed: solid, dashed, dotted.
    solid = stroke([(14, 20), (86, 20)], W)
    dashed = dashes(14, 86, 40, 14, 7, W)
    dotted = unary_union([dot(16 + i * 11.7, 60, 3.6) for i in range(7)])
    return [(INK, unary_union([solid, dashed])), (RED, dotted)]


def options():
    # A fork with one branch taken.
    stem = stroke([(50, 76), (50, 44)], W)
    left = stroke(bezier((50, 44), (50, 30), (30, 26), (24, 12)), W)
    mid = stroke([(50, 44), (50, 10)], W)
    ink = unary_union([stem, left, mid, dot(24, 12, 5), dot(50, 10, 5)])
    right = unary_union([stroke(bezier((50, 46), (50, 30), (70, 26), (76, 12)), W), dot(76, 12, 6)])
    return [(INK, ink.difference(right.buffer(3))), (RED, right)]


def criteria():
    # A ruler, with the mark that sets the standard.
    body = Polygon([(10, 40), (90, 40), (90, 64), (10, 64)])
    hole = Polygon([(15.5, 45.5), (84.5, 45.5), (84.5, 58.5), (15.5, 58.5)])
    rim = body.difference(hole)
    ticks = unary_union([stroke([(20 + i * 10, 44), (20 + i * 10, 52 if i % 2 else 56)], 3.6)
                         for i in range(7) if i != 4])
    pointer = unary_union([Polygon([(52, 14), (68, 14), (60, 28)]).buffer(1.5), stroke([(60, 24), (60, 56)], 4)])
    return [(INK, unary_union([rim, ticks]).difference(pointer.buffer(2.5))), (RED, pointer)]


def outcomes():
    # The red line pulls away from what would have happened anyway.
    axes = stroke([(14, 10), (14, 70), (90, 70)], W)
    base = unary_union([stroke([(x, 60 - (x - 22) * 0.12), (x + 8, 60 - (x + 8 - 22) * 0.12)], 4.5)
                        for x in range(22, 86, 14)])
    effect = stroke(bezier((22, 60), (46, 58), (64, 38), (86, 14)), W)
    return [(INK, unary_union([axes, base]).difference(effect.buffer(3))), (RED, effect)]


def tradeoffs():
    # A balance tipped: what is gained against what is given up.
    from shapely import affinity
    plank = affinity.rotate(stroke([(10, 46), (90, 46)], W), -12, origin=(50, 46))
    fulcrum = Polygon([(50, 46), (38, 70), (62, 70)])
    block = affinity.rotate(Polygon([(14, 34), (30, 34), (30, 50), (14, 50)]), -12, origin=(50, 46))
    block = affinity.translate(block, 0, 1)
    ball = dot(78, 30, 8)
    return [(INK, unary_union([plank, fulcrum, block]).difference(ball.buffer(2.5))), (RED, ball)]


def decide():
    # Sign here: the line, the cross, and the signature that commits.
    line = stroke([(12, 60), (88, 60)], 4.5)
    cross = unary_union([stroke([(12, 34), (24, 46)], 4.5), stroke([(24, 34), (12, 46)], 4.5)])
    sig = curve(lambda t: (34 + 2.4 * t * 4 * math.pi - 6 * math.sin(t * 4 * math.pi),
                           48 - 9 * math.cos(t * 4 * math.pi) + 4 * t), 160)
    sig += [(70, 44), (78, 40), (88, 32)]
    signature = stroke(sig, 5.5)
    return [(INK, unary_union([line, cross]).difference(signature.buffer(2.5))), (RED, signature)]


def story():
    # A memo that leads with the answer.
    page = Polygon([(24, 6), (62, 6), (76, 20), (76, 76), (24, 76)])
    inner = Polygon([(29.5, 11.5), (59.5, 11.5), (70.5, 22.5), (70.5, 70.5), (29.5, 70.5)])
    fold = unary_union([stroke([(60, 8), (60, 22), (74, 22)], 4.5)])
    lines = unary_union([stroke([(36, 44), (64, 44)], 4.5), stroke([(36, 54), (64, 54)], 4.5),
                         stroke([(36, 63), (54, 63)], 4.5)])
    lead = stroke([(36, 32), (64, 32)], W)
    return [(INK, unary_union([page.difference(inner), fold, lines])), (RED, lead)]


ICONS = {
    "problem": problem, "stakeholders": stakeholders, "evidence": evidence,
    "options": options, "criteria": criteria, "outcomes": outcomes,
    "tradeoffs": tradeoffs, "decision": decide, "story": story,
}


def write_icons():
    out = ROOT / "docs" / "icons"
    out.mkdir(exist_ok=True)
    for i, (name, fn) in enumerate(ICONS.items()):
        layers = [(("currentColor" if f == INK else f), g) for f, g in fn()]
        s = svg("0 0 100 80", layers, seed=100 + i, amp=0.45, scale=1.0,
                title=f"policymemo.ai {name} icon")
        s = s.replace(f'fill="{RED}"', f'class="red" fill="{RED}"')
        (out / f"{name}.svg").write_text(s, encoding="utf-8")


if __name__ == "__main__":
    write_mark()
    write_icons()
    print("wrote docs/mark.svg, docs/favicon.svg and", len(ICONS), "icons")
