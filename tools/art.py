# -*- coding: utf-8 -*-
"""art.py: the flat pictures. NaN and Beer come from the Facebook avatar scripts in tools/cast/.
    python3 tools/art.py      # writes docs/img/*.svg and build/card.svg
"""
import math
import os
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, os.path.join(HERE, "cast"))
import draw  # noqa: E402
import nan  # noqa: E402

ROOT = os.path.dirname(HERE)
IMG = os.path.join(ROOT, "docs", "img")
GOLD, CREAM, RED, IND = draw.GOLD, draw.CREAM, draw.RED, draw.IND
ROSE, ROSE2, ROSE3, WINE = "#C9485A", "#EE9496", "#F4B3B0", "#7A1A2C"
FONT = "font-family=\"'Avenir Next',Avenir,'Sukhumvit Set',Thonburi,'Segoe UI',system-ui,sans-serif\""

# Sauces: id, colour, bits colour(s), en, th, what
SAUCES = [
    ("namplaprik", "#C98A2B", ("#D62828", "#F1E3B4"), "Prik nam pla", "น้ำปลาพริก", "Fish sauce, sliced bird's-eye chilies, lime, sometimes garlic. Goes on krapow, fried rice, everything.", "น้ำปลา พริกขี้หนูซอย มะนาว บางร้านใส่กระเทียม ราดกะเพรา ข้าวผัด ได้ทุกอย่าง"),
    ("prikname", "#E9E0B8", ("#4E9A2E", "#D62828"), "Prik nam som", "พริกน้ำส้ม", "Chilies in vinegar, for noodle soup.", "พริกดองน้ำส้มสายชู ใส่ก๋วยเตี๋ยว"),
    ("namjimkai", "#E2552B", ("#B3121F",), "Nam jim kai", "น้ำจิ้มไก่", "Sweet chili sauce, for grilled chicken.", "น้ำจิ้มรสหวาน กินกับไก่ย่าง"),
    ("jaew", "#6B2E1E", ("#C1272D", "#D9B26F"), "Jaew", "น้ำจิ้มแจ่ว", "Dried chili, fish sauce, lime or tamarind, toasted rice powder. For grilled pork.", "พริกป่น น้ำปลา มะนาวหรือมะขาม ข้าวคั่ว กินกับหมูย่าง"),
    ("seafood", "#A7C957", ("#2D6A1F", "#F4F1DE"), "Nam jim seafood", "น้ำจิ้มซีฟู้ด", "Green chilies, garlic, lime, fish sauce. For anything from the sea.", "พริกเขียว กระเทียม มะนาว น้ำปลา กินกับอาหารทะเล"),
    ("suki", "#C0392B", ("#F4D35E",), "Nam jim suki", "น้ำจิ้มสุกี้", "Chili, fermented bean curd, sesame. For suki.", "พริก เต้าหู้ยี้ งา กินกับสุกี้"),
    ("sriracha", "#D7263D", (), "Sriracha", "ซอสพริกศรีราชา", "Chili sauce from Si Racha, for omelettes and fried things.", "ซอสพริกจากศรีราชา กินกับไข่เจียว ของทอด"),
]


def P(pts):
    return " ".join(f"{x:.1f},{y:.1f}" for x, y in pts)


def svg(w, h, body, extra=""):
    return (f'<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 {w} {h}" width="{w}" height="{h}" {FONT}{extra}>'
            + body + "</svg>")


def ease(t):
    t = max(0.0, min(1.0, t))
    return 0.5 - 0.5 * math.cos(math.pi * t)


def bag_width(u, puff=1.0):
    """Width of a tied balloon bag at height u (0 = top of the tip, 325 = bottom), unscaled."""
    if u < 38:
        return 18 + (38 - u) * 1.65
    if u < 88:
        return 18
    if u < 150:
        return 18 + 182 * ease((u - 88) / 62) + 14 * puff * ease((u - 88) / 62)
    return 200 + 14 * puff * math.sin(min(1, (u - 150) / 170) * math.pi * 0.9)


def bag_outline(cx, top, s, puff=1.0):
    ys = [u for u in range(0, 292, 3)]
    left = [(cx - s * bag_width(u, puff) / 2, top + s * u) for u in ys]
    right = [(cx + s * bag_width(u, puff) / 2, top + s * u) for u in ys]
    w = s * bag_width(290, puff) / 2
    bottom = [(cx + w * math.cos(a), top + s * 290 + s * 34 * math.sin(a)) for a in [math.pi * i / 24 for i in range(25)]]
    ruff = [(cx - s * bag_width(0) / 2 + s * bag_width(0) * i / 8, top + s * (0 if i % 2 else 5)) for i in range(9)]
    return left + sorted(bottom, key=lambda p: p[0]) + right[::-1] + ruff[1:-1][::-1]


def bag(cx, top, s, fill, bits=(), level=150, band="#E07A1F", wraps=4, uid="b", puff=1.0, lock=True, seed=1):
    """A tied curry bag: plastic, contents up to `level` (unscaled from the top), rubber band on the neck."""
    out = bag_outline(cx, top, s, puff)
    o = []
    o.append(f'<clipPath id="{uid}"><polygon points="{P(out)}"/></clipPath>')
    o.append(f'<polygon points="{P(out)}" fill="#FFFFFF" fill-opacity=".38"/>')
    o.append(f'<g clip-path="url(#{uid})"><rect x="{cx - 200 * s:.1f}" y="{top + level * s:.1f}" width="{400 * s:.1f}" height="{400 * s:.1f}" fill="{fill}"/>')
    o.append(f'<path d="M{cx - 200 * s:.1f} {top + level * s:.1f} Q{cx:.1f} {top + (level + 10) * s:.1f} {cx + 200 * s:.1f} {top + level * s:.1f}" fill="none" stroke="#fff" stroke-opacity=".35" stroke-width="{3 * s:.1f}"/>')
    import random
    rnd = random.Random(seed)
    for i in range(int(len(bits) and 16)):
        col = bits[i % len(bits)]
        x = cx + rnd.uniform(-85, 85) * s
        y = top + rnd.uniform(level + 18, 315) * s
        if i % 3 == 0:
            o.append(f'<ellipse cx="{x:.1f}" cy="{y:.1f}" rx="{9 * s:.1f}" ry="{4 * s:.1f}" fill="{col}" transform="rotate({rnd.uniform(-60, 60):.0f} {x:.1f} {y:.1f})"/>')
        else:
            o.append(f'<circle cx="{x:.1f}" cy="{y:.1f}" r="{rnd.uniform(2.5, 5) * s:.1f}" fill="{col}"/>')
    o.append('</g>')
    o.append(f'<polygon points="{P(out)}" fill="none" stroke="#5B5F66" stroke-opacity=".55" stroke-width="{max(1.2, 2.2 * s):.1f}" stroke-linejoin="round"/>')
    # shine
    o.append(f'<path d="M{cx - 70 * s:.1f} {top + 175 * s:.1f} Q{cx - 92 * s:.1f} {top + 230 * s:.1f} {cx - 72 * s:.1f} {top + 280 * s:.1f}" fill="none" stroke="#fff" stroke-opacity=".75" stroke-width="{7 * s:.1f}" stroke-linecap="round"/>')
    # twist lines on the neck
    for k in range(7):
        y = top + (44 + k * 6.5) * s
        o.append(f'<path d="M{cx - 9 * s:.1f} {y + 3 * s:.1f} L{cx + 9 * s:.1f} {y - 3 * s:.1f}" stroke="#5B5F66" stroke-opacity=".35" stroke-width="{1.4 * s:.1f}"/>')
    # rubber band: wraps from the bottom of the neck up, last turn over the tip
    for i in range(wraps):
        y = top + (82 - i * 8) * s
        o.append(f'<ellipse cx="{cx:.1f}" cy="{y:.1f}" rx="{12.5 * s:.1f}" ry="{3.6 * s:.1f}" fill="none" stroke="{band}" stroke-width="{3.4 * s:.1f}"/>')
    if lock:
        y = top + 40 * s
        o.append(f'<path d="M{cx - 12 * s:.1f} {top + (82 - (wraps - 1) * 8) * s:.1f} L{cx - 11 * s:.1f} {y:.1f} M{cx + 12 * s:.1f} {top + (82 - (wraps - 1) * 8) * s:.1f} L{cx + 11 * s:.1f} {y:.1f}" stroke="{band}" stroke-width="{3 * s:.1f}" stroke-linecap="round"/>')
        o.append(f'<ellipse cx="{cx:.1f}" cy="{y:.1f}" rx="{12 * s:.1f}" ry="{3.4 * s:.1f}" fill="none" stroke="{band}" stroke-width="{3.4 * s:.1f}"/>')
    return "".join(o)


def baggie_svg(sid, colour, bits, w=120, h=150):
    """A small sauce baggie for the parade, its own little svg."""
    s = 0.36
    cx, top = w / 2, 14
    body = bag(cx, top, s, colour, bits, level=120, band="#E07A1F", wraps=5, uid="sg" + sid, puff=1, seed=len(sid))
    return svg(w, h, body, f' role="img" aria-hidden="true" class="baggie"')


def scissors(x, y, ang, L=360, open_deg=16, gold=True):
    """Ribbon-cutting scissors: pivot at (x, y), blades toward +x before rotating."""
    blade = "#DDE2E8"
    edge = "#9AA3AD"
    h = GOLD if gold else "#2F6FB0"
    o = [f'<g transform="translate({x:.1f} {y:.1f}) rotate({ang:.1f})">']
    for sgn in (-1, 1):
        a = sgn * open_deg / 2
        o.append(f'<g transform="rotate({a:.1f})">'
                 f'<path d="M-10 {-sgn * 10} L{L:.0f} {sgn * 2} L{L * .1:.0f} {sgn * 22} Z" fill="{blade}"/>'
                 f'<path d="M-10 {-sgn * 10} L{L:.0f} {sgn * 2}" stroke="{edge}" stroke-width="3"/>'
                 f'<path d="M0 0 L{-L * .28:.0f} {sgn * 40}" stroke="{h}" stroke-width="20" stroke-linecap="round"/>'
                 f'<ellipse cx="{-L * .38:.0f}" cy="{sgn * 58}" rx="{L * .13:.0f}" ry="{L * .1:.0f}" fill="none" stroke="{h}" stroke-width="20"/>'
                 f'<ellipse cx="{-L * .38:.0f}" cy="{sgn * 58}" rx="{L * .13:.0f}" ry="{L * .1:.0f}" fill="none" stroke="#F3D27A" stroke-width="4" stroke-dasharray="40 30"/>'
                 '</g>')
    o.append(f'<circle r="13" fill="{h}"/><circle r="5" fill="{WINE}"/></g>')
    return "".join(o)


def ribbon(x0, x1, y, sag=30, w=26):
    pts_top = [(x0 + (x1 - x0) * t, y + sag * math.sin(math.pi * t) + 6 * math.sin(t * 18)) for t in [i / 40 for i in range(41)]]
    pts_bot = [(px, py + w) for px, py in pts_top]
    return (f'<polygon points="{P(pts_top + pts_bot[::-1])}" fill="#C8102E"/>'
            f'<polyline points="{P([(px, py + 5) for px, py in pts_top])}" fill="none" stroke="#F26B6B" stroke-width="3" opacity=".7"/>')


def bow(cx, cy, s=1.0):
    r = "#C8102E"
    return (f'<path d="M{cx} {cy} C{cx - 90 * s} {cy - 70 * s} {cx - 120 * s} {cy + 40 * s} {cx} {cy}Z" fill="{r}"/>'
            f'<path d="M{cx} {cy} C{cx + 90 * s} {cy - 70 * s} {cx + 120 * s} {cy + 40 * s} {cx} {cy}Z" fill="{r}"/>'
            f'<path d="M{cx} {cy} L{cx - 50 * s} {cy + 110 * s} L{cx - 26 * s} {cy + 100 * s} L{cx - 14 * s} {cy + 118 * s}Z" fill="#A00D25"/>'
            f'<path d="M{cx} {cy} L{cx + 46 * s} {cy + 108 * s} L{cx + 24 * s} {cy + 100 * s} L{cx + 12 * s} {cy + 118 * s}Z" fill="#A00D25"/>'
            f'<ellipse cx="{cx}" cy="{cy}" rx="{16 * s:.1f}" ry="{13 * s:.1f}" fill="#E0233F"/>')


def onsen_egg(cx, cy, s=1.0):
    """A bowl with an onsen egg: loose white, round set yolk, a line of sauce."""
    o = [f'<ellipse cx="{cx}" cy="{cy}" rx="{78 * s:.1f}" ry="{20 * s:.1f}" fill="#F7F3EA"/>',
         f'<path d="M{cx - 78 * s:.1f} {cy} Q{cx - 70 * s:.1f} {cy + 70 * s:.1f} {cx} {cy + 72 * s:.1f} Q{cx + 70 * s:.1f} {cy + 70 * s:.1f} {cx + 78 * s:.1f} {cy}Z" fill="#FFFFFF"/>',
         f'<path d="M{cx - 74 * s:.1f} {cy + 18 * s:.1f} Q{cx} {cy + 34 * s:.1f} {cx + 74 * s:.1f} {cy + 18 * s:.1f}" fill="none" stroke="{IND}" stroke-width="{5 * s:.1f}"/>',
         f'<ellipse cx="{cx}" cy="{cy}" rx="{70 * s:.1f}" ry="{15 * s:.1f}" fill="#7A4A1E" opacity=".55"/>',
         f'<path d="M{cx - 52 * s:.1f} {cy - 2 * s:.1f} C{cx - 40 * s:.1f} {cy - 26 * s:.1f} {cx + 44 * s:.1f} {cy - 30 * s:.1f} {cx + 56 * s:.1f} {cy - 2 * s:.1f} C{cx + 30 * s:.1f} {cy + 10 * s:.1f} {cx - 30 * s:.1f} {cy + 10 * s:.1f} {cx - 52 * s:.1f} {cy - 2 * s:.1f}Z" fill="#FBF6EC" opacity=".93"/>',
         f'<circle cx="{cx + 4 * s:.1f}" cy="{cy - 12 * s:.1f}" r="{20 * s:.1f}" fill="#F2A21B"/>',
         f'<circle cx="{cx - 3 * s:.1f}" cy="{cy - 19 * s:.1f}" r="{6 * s:.1f}" fill="#FFD27A"/>',
         f'<path d="M{cx - 28 * s:.1f} {cy - 6 * s:.1f} q8 {6 * s:.1f} 18 0" stroke="#3A9A3A" stroke-width="{4 * s:.1f}" fill="none" stroke-linecap="round"/>']
    for i in range(3):
        a = -1.2 + i * 0.9
        o.append(f'<path d="M{cx + 30 * math.cos(a) * s:.1f} {cy - 40 * s - i * 6:.1f} q{-8 * s:.1f} {-16 * s:.1f} 0 {-32 * s:.1f} q{8 * s:.1f} {-16 * s:.1f} 0 {-32 * s:.1f}" stroke="#fff" stroke-width="{4 * s:.1f}" fill="none" opacity=".6" stroke-linecap="round"/>')
    return "".join(o)


def krapow_box(cx, cy, s=1.0, egg=True):
    """Kraft take-away box: rice, pork krapow, basil, an onsen egg on top."""
    o = [f'<path d="M{cx - 110 * s:.1f} {cy - 40 * s:.1f} L{cx + 110 * s:.1f} {cy - 40 * s:.1f} L{cx + 92 * s:.1f} {cy + 60 * s:.1f} L{cx - 92 * s:.1f} {cy + 60 * s:.1f}Z" fill="#B98A55"/>',
         f'<path d="M{cx - 110 * s:.1f} {cy - 40 * s:.1f} L{cx + 110 * s:.1f} {cy - 40 * s:.1f} L{cx + 106 * s:.1f} {cy - 22 * s:.1f} L{cx - 106 * s:.1f} {cy - 22 * s:.1f}Z" fill="#9C7040"/>',
         f'<ellipse cx="{cx - 30 * s:.1f}" cy="{cy - 44 * s:.1f}" rx="{70 * s:.1f}" ry="{26 * s:.1f}" fill="#FBF8F0"/>',
         f'<ellipse cx="{cx + 40 * s:.1f}" cy="{cy - 46 * s:.1f}" rx="{64 * s:.1f}" ry="{22 * s:.1f}" fill="#6B3A22"/>']
    import random
    rnd = random.Random(7)
    for i in range(26):
        x = cx + 40 * s + rnd.uniform(-55, 55) * s
        y = cy - 46 * s + rnd.uniform(-16, 14) * s
        if i % 3 == 0:
            o.append(f'<ellipse cx="{x:.1f}" cy="{y:.1f}" rx="{10 * s:.1f}" ry="{5 * s:.1f}" fill="#2E7D32" transform="rotate({rnd.uniform(-50, 50):.0f} {x:.1f} {y:.1f})"/>')
        elif i % 3 == 1:
            o.append(f'<circle cx="{x:.1f}" cy="{y:.1f}" r="{3.2 * s:.1f}" fill="#D62828"/>')
        else:
            o.append(f'<circle cx="{x:.1f}" cy="{y:.1f}" r="{4 * s:.1f}" fill="#8B4A2B"/>')
    if egg:
        ex, ey = cx - 20 * s, cy - 58 * s
        o.append(f'<path d="M{ex - 48 * s:.1f} {ey + 6 * s:.1f} C{ex - 40 * s:.1f} {ey - 22 * s:.1f} {ex + 40 * s:.1f} {ey - 24 * s:.1f} {ex + 50 * s:.1f} {ey + 6 * s:.1f} C{ex + 20 * s:.1f} {ey + 18 * s:.1f} {ex - 20 * s:.1f} {ey + 18 * s:.1f} {ex - 48 * s:.1f} {ey + 6 * s:.1f}Z" fill="#FBF6EC" opacity=".95"/>')
        o.append(f'<circle cx="{ex + 2 * s:.1f}" cy="{ey - 6 * s:.1f}" r="{17 * s:.1f}" fill="#F2A21B"/><circle cx="{ex - 4 * s:.1f}" cy="{ey - 12 * s:.1f}" r="{5 * s:.1f}" fill="#FFD27A"/>')
    return "".join(o)


def bust(who, x, y, s):
    body = nan.nan() if who == "nan" else draw.beer("hb")
    return f'<g transform="translate({x:.1f} {y:.1f}) scale({s:.3f})">{body}</g>'


def bunting(W, y, n, s=0.3, start=0):
    o = [f'<path d="M0 {y} Q{W / 2} {y + 40} {W} {y}" fill="none" stroke="#7A1A2C" stroke-width="4"/>']
    for i in range(n):
        t = (i + 0.5) / n
        x = W * t
        yy = y + 40 * 4 * t * (1 - t) * 0.5 * 2 - 6
        sid, col, bits = SAUCES[(i + start) % len(SAUCES)][:3]
        o.append(bag(x, yy, s, col, bits, level=118, wraps=4, uid=f"bt{i}{start}", seed=i))
    return "".join(o)


def scene(W=1600, H=900, title=False):
    o = [f'<defs><linearGradient id="sky" x1="0" y1="0" x2="0" y2="1"><stop offset="0" stop-color="#F6B8B4"/>'
         f'<stop offset=".7" stop-color="#E97C80"/><stop offset="1" stop-color="{ROSE}"/></linearGradient></defs>',
         f'<rect width="{W}" height="{H}" fill="url(#sky)"/>']
    for (x, y, r) in ((W * .06, 210, 16), (W * .3, 250, 11), (W * .7, 240, 13), (W * .94, 200, 18), (W * .5, 205, 9)):
        o.append(nan.sparkle(x, y, r, GOLD, 1))
    for i in range(10):
        o.append(nan.moon(W * (0.05 + 0.1 * i), H * .3 + 18 * math.sin(i), 9, 2 * math.pi * i / 10 + .01, CREAM, CREAM, .3))
    o.append(bunting(W, 30, 9 if W > 1300 else 7, 0.3))
    bs = 0.62 * H / 900
    o.append(bust("nan", -40 * W / 1600, H - 1024 * bs + 20, bs))
    o.append(bust("beer", W - 1024 * bs + 40 * W / 1600, H - 1024 * bs + 20, bs))
    # counter
    cy = H - 100 * H / 900
    o.append(f'<rect x="0" y="{cy:.0f}" width="{W}" height="{H - cy:.0f}" fill="#C9CED6"/>')
    o.append(f'<rect x="0" y="{cy:.0f}" width="{W}" height="10" fill="#EEF1F4"/>')
    o.append(draw.tinchok(0, H - 40, W, 40, 56))
    s = 1.55 * H / 900
    top = cy - 322 * s
    cx = W / 2
    o.append(bag(cx, top, s, "#E0601F", ("#B3121F", "#2E7D32", "#F4E3B5"), level=150, uid="hero", seed=3))
    # the ribbon, tied on the neck with a bow
    ny = top + 62 * s
    o.append(ribbon(W * .27, cx - 10, ny - 10, sag=26, w=22 * H / 900))
    o.append(ribbon(cx + 10, W * .73, ny - 10, sag=26, w=22 * H / 900))
    o.append(bow(cx, ny, 0.9 * H / 900))
    # NaN's scissors aimed at the ribbon; the egg and the krapow on the counter
    o.append(scissors(W * .3, ny + 230 * H / 900, -52, L=300 * H / 900, open_deg=26))
    o.append(onsen_egg(W * .3, cy - 6, 0.95 * H / 900))
    o.append(krapow_box(W * .7, cy + 4, 0.95 * H / 900))
    # a prik nam pla baggie beside the box
    o.append(bag(W * .585, cy - 97 * H / 900, 0.3 * H / 900, SAUCES[0][1], SAUCES[0][2], level=118, uid="pnp", seed=9))
    return svg(W, H, "".join(o), ' role="img"')


def main():
    os.makedirs(IMG, exist_ok=True)
    open(os.path.join(IMG, "hero.svg"), "w").write(scene())
    for who in ("nan", "beer"):
        body = (nan.profile() if who == "nan" else draw.profile())
        inner = body[body.index(">") + 1:body.rindex("</svg>")]
        open(os.path.join(IMG, who + ".svg"), "w").write(
            svg(1024, 1024, f'<defs><clipPath id="o{who}"><circle cx="512" cy="512" r="512"/></clipPath></defs><g clip-path="url(#o{who})">{inner}</g>'))
    open(os.path.join(IMG, "egg.svg"), "w").write(svg(360, 220, onsen_egg(180, 120, 1.7), ' role="img"'))
    open(os.path.join(IMG, "krapow.svg"), "w").write(svg(420, 260, krapow_box(190, 150, 1.4)
                                                         + bag(370, 60, .4, SAUCES[0][1], SAUCES[0][2], level=118, uid="kp", seed=4), ' role="img"'))
    open(os.path.join(IMG, "scissors.svg"), "w").write(svg(420, 200, scissors(250, 100, 180, L=200, open_deg=30), ' role="img"'))
    b = os.path.join(ROOT, "build")
    os.makedirs(b, exist_ok=True)
    open(os.path.join(b, "card-scene.svg"), "w").write(scene(1200, 630))
    print("docs/img: hero, nan, beer, egg, krapow, scissors; build/card-scene.svg")


if __name__ == "__main__":
    main()
