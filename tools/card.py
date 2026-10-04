# -*- coding: utf-8 -*-
"""card.py: the 1200 x 630 share card. python3 tools/card.py  (needs rsvg-convert, magick)"""
import os, subprocess, sys
HERE = os.path.dirname(os.path.abspath(__file__)); sys.path.insert(0, HERE)
import art
ROOT = os.path.dirname(HERE); B = os.path.join(ROOT, "build"); os.makedirs(B, exist_ok=True)
sc = art.scene(1200, 630)
inner = sc[sc.index(">") + 1:sc.rindex("</svg>")]
plate = ('<rect x="390" y="128" width="420" height="104" rx="22" fill="#FBF3E4" opacity=".94"/>'
         '<text x="600" y="184" text-anchor="middle" font-size="54" font-weight="700" fill="#7A1A2C" font-family="Georgia,serif">Bag Knots</text>'
         '<text x="600" y="220" text-anchor="middle" font-size="30" font-weight="700" fill="#C9485A" font-family="Sukhumvit Set,Thonburi">มัดถุง · แกะถุง · กรรไกร</text>')
open(os.path.join(B, "card.svg"), "w").write(art.svg(1200, 630, inner + plate))
subprocess.run(["rsvg-convert", "-w", "1200", os.path.join(B, "card.svg"), "-o", os.path.join(B, "card.png")], check=True)
subprocess.run(["magick", os.path.join(B, "card.png"), "-quality", "86", os.path.join(ROOT, "docs", "card.jpg")], check=True)
print("docs/card.jpg")
