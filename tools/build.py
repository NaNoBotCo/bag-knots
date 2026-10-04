#!/usr/bin/env python3
"""build.py: writes docs/index.html (English), docs/th/index.html (Thai), sitemap.xml, robots.txt, llms.txt.
All words, both languages, are written by hand here and in ties.py.
    python3 tools/art.py && python3 tools/build.py
"""
import html
import json
import os
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)
from ties import TIES, js_data  # noqa: E402
from art import SAUCES, baggie_svg  # noqa: E402

DOCS = os.path.join(HERE, "..", "docs")
BASE = "https://nanobotco.github.io/bag-knots/"
E = html.escape
CSS = open(os.path.join(HERE, "site.css")).read()
GOOGLE_ESCAPE = '<script>if(/[.]translate[.]goog$/.test(location.hostname))location.replace("https://"+location.hostname.slice(0,-15).replace(/--/g,"~").replace(/-/g,".").replace(/~/g,"-")+location.pathname+location.search.replace(/([?&])_x_tr_[^&]*/g,"$1").replace(/[?&]+$/,"").replace(/[?]&+/,"?")+location.hash)</script>'
WHO = {"nan": ("NaN", "แนน"), "beer": ("Beer", "เบียร์")}

U = {
    "en": {
        "title": "Bag Knots", "other_title": "มัดถุง", "lang_this": "EN", "lang_other": "ไทย",
        "desc": "Every way a Thai shop ties a bag shut, drawn step by step, and how to get each one open: by hand, or with scissors cut in the right place. With NaN and Beer.",
        "kicker": "NaN & Beer · grand opening",
        "lede": "Every way a Thai shop ties a bag shut, drawn step by step, and how to get each one open: by hand, or with scissors, cut in the right place.",
        "nav": [("band", "Rubber band"), ("plain", "No band"), ("scissors", "Scissors"), ("sauces", "Sauces"), ("sources", "Sources")],
        "play": "Play", "pause": "Pause", "make": "Make", "hand": "By hand", "scis": "Scissors",
        "open": [
            ("nan", "Today we cut the ribbon on… the bag knot!"),
            ("beer", "Every knot. Every band. Every last little sauce bag."),
            ("nan", "Scissors ready!"),
            ("beer", "NaN, those are ribbon scissors."),
            ("nan", "Exactly!"),
        ],
        "band_h": "Rubber band", "band_kick": "หนังยาง · nang yang",
        "band_p": "A rubber band goes on a bag a dozen ways. These are the ones you meet most, each drawn from the open bag to the last turn, then undone by hand, then cut. Tap a step to jump to it.",
        "plain_h": "No band", "plain_kick": "Knots, handles, heat, staples",
        "plain_p": "Some bags skip the band: the plastic is knotted on itself, the handles are tied, the mouth is melted shut, or a label is stapled over it.",
        "egg_h": "Onsen egg", "egg_kick": "ไข่ออนเซ็น · a detour",
        "egg_say": [("beer", "Wait. Is that an onsen egg?"), ("nan", "On krapow?!"), ("beer", "We were cutting a ribbon.")],
        "egg_p": "An onsen egg is cooked slowly in water at about 65 to 68 °C, hot enough to set the yolk and too cool to set the white, so the white stays soft as custard. Its sauce usually comes in a little heat-sealed sachet: the Heat seal tie below shows how that one opens.",
        "krapow_h": "Pad krapow", "krapow_kick": "ผัดกะเพรา · another detour",
        "krapow_say": [("nan", "Pad krapow. Onsen egg on top."), ("beer", "And the prik nam pla in its own tiny bag. Tied, of course.")],
        "krapow_p": "Holy basil (กะเพรา) stir-fried hard with garlic, chilies and minced pork or chicken, over rice, usually with a fried egg. To take away it comes in a box or a bag, and the prik nam pla rides along in a baggie the size of a thumb, banded or knotted. That one opens best over the rice: snip a corner.",
        "sauces_h": "Sauce baggies", "sauces_kick": "ถุงน้ำจิ้ม · the parade",
        "sauces_say": [("nan", "Sauce baggies!"), ("beer", "NaN. The ribbon."), ("nan", "Seven sauce baggies!")],
        "sauces_p": "Each one tied the same way: a spoonful, a puff of air, a twist, five or six turns of band. Each one opens the same way: a corner snipped over the food.",
        "scis_h": "Scissors", "scis_kick": "กรรไกร · where to cut",
        "scis_say": [("beer", "Back to the ribbon."), ("nan", "The ribbon IS the neck of the bag."), ("beer", "Then kitchen scissors, NaN.")],
        "rules": [
            "Kitchen scissors. The ribbon pair is for ribbons.",
            "Bowl first. Stand a soup or curry bag in its bowl before cutting anything, and hold it by the neck, under the band.",
            "Below the band. A cut above the band takes off the tip and the bag stays shut.",
            "About 1 cm below the lowest turn, one snip straight across the twisted neck. Tip, twist and band come off in one piece.",
            "To keep the bag whole, cut the band instead: slide one blade flat under the turns, along the neck, point toward the tip, and snip. Every turn parts at once. Keep the point off the plastic under the band.",
            "Sauce baggies: over the food, snip a bottom corner, 2 to 3 mm for runny sauce, 5 mm or more for thick. The band stays on.",
            "Carrier bags: snip one handle beside the knot.",
            "Heat seals and staples: straight across, just under the seal or the label.",
            "Hot bags puff out steam when they open. Face back, and the blades pointing away from the hand that holds the bag.",
        ],
        "tbl": ("Tie", "By hand", "Scissors"),
        "end_say": [("nan", "Grand opening!"), ("beer", "Lunch is open.")],
        "sources_h": "Sources",
        "sources_note": "The drawings are diagrams of the steps, not traces of anyone's hands. The folded-mouth knot follows Krua Khun Toi step by step; the tip tug follows a Thai news headline about a seller's trick. The drink bag, roll-and-band, carrier-bag knots, heat seal and staple are drawn from everyday shop practice rather than one written source.",
        "foot": "Text CC BY 4.0, NaNoBotCo. Code MIT.",
        "tie_word": "Tie",
    },
    "th": {
        "title": "มัดถุง", "other_title": "Bag Knots", "lang_this": "ไทย", "lang_other": "EN",
        "desc": "ทุกวิธีที่ร้านค้าไทยมัดปากถุง วาดทีละขั้น และวิธีแกะแต่ละแบบ ด้วยมือ หรือด้วยกรรไกร ตัดให้ถูกที่ กับแนนและเบียร์",
        "kicker": "แนน & เบียร์ · พิธีเปิด",
        "lede": "ทุกวิธีที่ร้านค้าไทยมัดปากถุง วาดทีละขั้น และวิธีแกะแต่ละแบบ ด้วยมือ หรือด้วยกรรไกร ตัดให้ถูกที่",
        "nav": [("band", "หนังยาง"), ("plain", "ไม่ใช้ยาง"), ("scissors", "กรรไกร"), ("sauces", "น้ำจิ้ม"), ("sources", "ที่มา")],
        "play": "เล่น", "pause": "หยุด", "make": "มัด", "hand": "แกะมือ", "scis": "กรรไกร",
        "open": [
            ("nan", "วันนี้เราตัดริบบิ้นเปิด… ปมถุง!"),
            ("beer", "ทุกปม ทุกยาง ทุกถุงน้ำจิ้มใบจิ๋ว"),
            ("nan", "กรรไกรพร้อม!"),
            ("beer", "แนน นั่นกรรไกรตัดริบบิ้นนะ"),
            ("nan", "ใช่เลย!"),
        ],
        "band_h": "หนังยาง", "band_kick": "rubber band",
        "band_p": "หนังยางรัดปากถุงได้เป็นสิบแบบ นี่คือแบบที่เจอบ่อยที่สุด วาดตั้งแต่ถุงยังเปิดจนยางรอบสุดท้าย แล้วแกะด้วยมือ แล้วตัดด้วยกรรไกร แตะขั้นไหนก็ข้ามไปขั้นนั้นได้",
        "plain_h": "ไม่ใช้ยาง", "plain_kick": "ผูกปม ผูกหู ซีล เย็บแม็ก",
        "plain_p": "บางถุงไม่ใช้ยาง ผูกปมที่ตัวถุงเอง ผูกหูถุง ซีลปากด้วยความร้อน หรือเย็บแม็กป้ายครอบไว้",
        "egg_h": "ไข่ออนเซ็น", "egg_kick": "onsen egg · แวะข้างทาง",
        "egg_say": [("beer", "เดี๋ยวนะ นั่นไข่ออนเซ็นเหรอ"), ("nan", "บนกะเพรา?!"), ("beer", "เรากำลังตัดริบบิ้นอยู่นะ")],
        "egg_p": "ไข่ออนเซ็นต้มช้าๆ ในน้ำราว 65 ถึง 68 องศา ร้อนพอให้ไข่แดงเซ็ตตัว แต่ไม่ร้อนพอให้ไข่ขาวสุก ไข่ขาวจึงนุ่มเหมือนคัสตาร์ด ซอสมักมาในซองเล็กที่ซีลด้วยความร้อน วิธีเปิดซองแบบนี้อยู่ในหัวข้อซีลด้วยความร้อนข้างล่าง",
        "krapow_h": "ผัดกะเพรา", "krapow_kick": "pad krapow · แวะอีกที",
        "krapow_say": [("nan", "ผัดกะเพรา ไข่ออนเซ็นโปะ"), ("beer", "แล้วก็น้ำปลาพริกถุงจิ๋ว มัดยางแน่นอน")],
        "krapow_p": "ใบกะเพราผัดไฟแรงกับกระเทียม พริก หมูสับหรือไก่สับ ราดข้าว ส่วนใหญ่มีไข่ดาว ซื้อกลับบ้านใส่กล่องหรือใส่ถุง มีน้ำปลาพริกถุงเท่านิ้วโป้งติดมาด้วย รัดยางหรือผูกปม ถุงนี้เปิดเหนือข้าวดีที่สุด ตัดมุมเอา",
        "sauces_h": "ถุงน้ำจิ้ม", "sauces_kick": "sauce baggies · ขบวนแห่",
        "sauces_say": [("nan", "ถุงน้ำจิ้ม!"), ("beer", "แนน ริบบิ้นล่ะ"), ("nan", "น้ำจิ้มเจ็ดถุง!")],
        "sauces_p": "มัดแบบเดียวกันทุกถุง ตักหนึ่งช้อน ขังลม บิดคอ พันยางห้าหกรอบ และเปิดแบบเดียวกันทุกถุง ตัดมุมเหนืออาหาร",
        "scis_h": "กรรไกร", "scis_kick": "scissors · ตัดตรงไหน",
        "scis_say": [("beer", "กลับมาที่ริบบิ้น"), ("nan", "ริบบิ้นก็คือคอถุงนั่นแหละ"), ("beer", "งั้นใช้กรรไกรครัวนะแนน")],
        "rules": [
            "กรรไกรครัว กรรไกรตัดริบบิ้นเอาไว้ตัดริบบิ้น",
            "ชามก่อน ตั้งถุงแกงหรือถุงต้มในชามก่อนตัด แล้วจับคอถุงใต้ยางไว้",
            "ใต้ยาง ถ้าตัดเหนือยาง ปลายถุงหลุดไปแต่ถุงยังปิดอยู่",
            "ต่ำกว่ายางรอบล่างสุดราว 1 ซม. ตัดฉับเดียวขวางคอถุงที่บิดไว้ ปลาย เกลียว และยาง หลุดออกเป็นชิ้นเดียว",
            "อยากให้ถุงไม่ขาด ตัดยางแทน สอดใบกรรไกรใบหนึ่งแนบใต้รอบยาง ตามแนวคอถุง ปลายใบชี้ไปทางปลายถุง แล้วตัด ยางขาดทุกรอบพร้อมกัน ปลายกรรไกรห่างจากพลาสติกใต้ยาง",
            "ถุงน้ำจิ้ม ถือเหนืออาหาร ตัดมุมก้นถุง 2-3 มม. สำหรับน้ำจิ้มใส 5 มม. ขึ้นไปสำหรับน้ำจิ้มข้น ยางไม่ต้องแกะ",
            "ถุงหูหิ้ว ตัดหูข้างหนึ่งชิดปม",
            "ซีลกับเย็บแม็ก ตัดตรงๆ ใต้รอยซีลหรือใต้ป้าย",
            "ถุงร้อนจะพ่นไอออกตอนเปิด หน้าถอยห่าง ปลายกรรไกรชี้ออกจากมือที่จับถุง",
        ],
        "tbl": ("แบบ", "แกะมือ", "กรรไกร"),
        "end_say": [("nan", "เปิดแล้ว!"), ("beer", "ข้าวเที่ยงเปิดแล้ว")],
        "sources_h": "ที่มา",
        "sources_note": "ภาพวาดเป็นแผนภาพของขั้นตอน ไม่ได้ลอกมือของใคร แบบพับปากถุงทำตามครัวคุณต๋อยทีละขั้น แบบกระตุกปลายถุงมาจากพาดหัวข่าวทริคของพ่อค้า ถุงน้ำ แบบม้วนรัดยาง ผูกหูถุง ซีล และเย็บแม็ก วาดจากที่ร้านค้าทำกันทุกวัน ไม่ได้มาจากแหล่งเขียนแหล่งเดียว",
        "foot": "ข้อความ CC BY 4.0 NaNoBotCo · โค้ด MIT",
        "tie_word": "แบบ",
    },
}

SOURCES = [
    ("Nation Thailand", "Why Thai food bags are so hard to untie and how to do it right", "https://www.nationthailand.com/life/art-culture/40050678",
     "twist, several turns, one more twist", "บิดคอ พันหลายรอบ บิดอีกที"),
    ("Krua Khun Toi · ครัวคุณต๋อย", "ทริค มัดถุงแกง แกะง่าย", "https://www.kruakhuntoi.com/tips/%E0%B8%97%E0%B8%A3%E0%B8%B4%E0%B8%84-%E0%B8%A1%E0%B8%B1%E0%B8%94%E0%B8%96%E0%B8%B8%E0%B8%87%E0%B9%81%E0%B8%81%E0%B8%87-%E0%B9%81%E0%B8%81%E0%B8%B0%E0%B8%87%E0%B9%88%E0%B8%B2%E0%B8%A2/",
     "folded mouth, little-finger knot, three turns, tucked end, pull to open", "พับปากถุง เกี่ยวนิ้วก้อย พันสามรอบ เหน็บปลาย ดึงเปิด"),
    ("Postjung News", "พ่อค้าโชว์! \"ทริคมัดถุงแกง\" ให้แกะง่าย เผยแค่กระตุกปลายถุง 1 ครั้ง ยางก็หลุดออกง่ายดาย", "https://news.postjung.com/1437062",
     "the tip tug (headline; the page no longer loads)", "กระตุกปลายถุง (พาดหัว หน้าเว็บเปิดไม่ได้แล้ว)"),
    ("Postjung", "\"มัดถุงแกง\" ทักษะขั้นสูงของแม่ค้าไทย ต่างชาติยังทึ่ง", "https://board.postjung.com/1549951",
     "the puff of air keeps food from being squashed", "ถุงพองกันอาหารโดนบีบ"),
    ("Pantip", "อยากทราบว่า มีโรงเรียนสอนมัดถุงแกงใช่ไหมครับ", "https://pantip.com/topic/33504484",
     "scissors, a knife, teeth, poking through the bottom", "กรรไกร มีด ฟัน สอยทะลุก้นถุง"),
    ("Eating Thai Food", "Thailand's One Finger Rule: the plastic bag phenomenon", "https://www.eatingthaifood.com/thailands-one-finger-rule-the-plastic-bag-phenomenon/",
     "the air bubble; carrying it all on one finger", "ฟองอากาศ หิ้วทุกอย่างด้วยนิ้วเดียว"),
    ("SAYS", "Guy shows hack to untie plastic bag knot when it's too tight", "https://says.com/my/lifestyle/video-guy-shows-hack-to-untie-plastic-bag-knot-when-its-too-tight",
     "twist both sides of a tight knot, then wiggle", "บิดสองข้างของปมแน่น แล้วโยก"),
    ("Wikipedia", "Onsen tamago", "https://en.wikipedia.org/wiki/Onsen_tamago",
     "65 to 68 °C; yolk sets, white stays soft", "65 ถึง 68 องศา ไข่แดงเซ็ต ไข่ขาวนุ่ม"),
]


def say(lang, who, text):
    name = WHO[who][0 if lang == "en" else 1]
    return (f'<div class="say say-{who}"><img src="{{root}}img/{who}.svg" alt="" width="52" height="52">'
            f'<p><b>{E(name)}</b> {E(text)}</p></div>')


def talk(lang, lines):
    return '<div class="talk">' + "".join(say(lang, w, t) for w, t in lines) + "</div>"


def tie_card(lang, t, u):
    name = t[lang]
    where = t["where_" + lang]
    lists = []
    for ph in ("make", "hand", "scis"):
        items = [(i, st) for i, st in enumerate(t["steps"]) if st[0] == ph]
        if not items:
            continue
        lis = "".join(f'<li data-i="{i}">{E(st[3] if lang == "en" else st[4])}</li>' for i, st in items)
        lists.append(f'<div class="ph"><h4>{E(u[ph])}</h4><ol>{lis}</ol></div>')
    phases = "".join(f'<button type="button" class="chip" data-phase="{ph}" aria-pressed="false">{E(u[ph])}</button>'
                     for ph in ("make", "hand", "scis") if any(st[0] == ph for st in t["steps"]))
    who, en, th = t["say"]
    return f'''<article class="tie" id="tie-{t["id"]}" data-tie="{t["id"]}">
<header><h3>{E(name)}</h3><p class="where">{E(where)}</p></header>
<div class="tie-g"><div class="stage"><canvas width="480" height="400" role="img" aria-label="{E(name)}"></canvas>
<p class="cap" aria-live="polite"></p>
<div class="ctl"><button type="button" class="pill prev" aria-label="‹">‹</button><button type="button" class="pill play hot" aria-pressed="false">{E(u["play"])}</button><button type="button" class="pill next" aria-label="›">›</button><span class="cnt"></span></div>
<div class="phases">{phases}</div></div>
<div class="steps">{"".join(lists)}</div></div>
{say(lang, who, en if lang == "en" else th)}
</article>'''


def detour(lang, u, key, img, w, h):
    return f'''<section class="detour" id="{key}"><div class="in">
<p class="kick">{E(u[key + "_kick"])}</p><h2>{E(u[key + "_h"])}</h2>
<div class="det-g"><img src="{{root}}img/{img}" alt="" width="{w}" height="{h}" loading="lazy">
<div>{talk(lang, u[key + "_say"])}<p>{E(u[key + "_p"])}</p></div></div></div></section>'''


def sauces(lang, u):
    cells = []
    for sid, col, bits, en, th, what_en, what_th in SAUCES:
        nm, other = (en, th) if lang == "en" else (th, en)
        cells.append(f'<figure class="sauce">{baggie_svg(sid, col, bits)}<figcaption><b>{E(nm)}</b> <span>{E(other)}</span>'
                     f'<small>{E(what_en if lang == "en" else what_th)}</small></figcaption></figure>')
    return f'''<section class="detour" id="sauces"><div class="in">
<p class="kick">{E(u["sauces_kick"])}</p><h2>{E(u["sauces_h"])}</h2>
{talk(lang, u["sauces_say"])}<p>{E(u["sauces_p"])}</p>
<div class="parade">{"".join(cells)}</div></div></section>'''


def page(lang):
    u = U[lang]
    root = "" if lang == "en" else "../"
    url = BASE if lang == "en" else BASE + "th/"
    other = (BASE + "th/", "ไทย", "th") if lang == "en" else (BASE, "EN", "en")
    band = [t for t in TIES if t["group"] == "band"]
    plain = [t for t in TIES if t["group"] == "plain"]
    body = []
    for t in band:
        body.append(tie_card(lang, t, u))
        if t["id"] == "balloon":
            body.append("</div></section>" + detour(lang, u, "egg", "egg.svg", 360, 220) + '<section class="sec"><div class="in">')
        if t["id"] == "piggyback":
            body.append("</div></section>" + detour(lang, u, "krapow", "krapow.svg", 420, 260) + '<section class="sec"><div class="in">')
        if t["id"] == "baggie":
            body.append("</div></section>" + sauces(lang, u) + '<section class="sec"><div class="in">')
    band_html = "".join(body)
    plain_html = "".join(tie_card(lang, t, u) for t in plain)
    rows = "".join(f'<tr><th scope="row"><a href="#tie-{t["id"]}">{E(t[lang])}</a></th><td>{E(t["hand_" + lang])}</td><td>{E(t["scis_" + lang])}</td></tr>' for t in TIES)
    src = "".join(f'<li><a href="{E(h)}">{E(pub)}: {E(ti)}</a> · {E(en if lang == "en" else th)}</li>' for pub, ti, h, en, th in SOURCES)
    nav = "".join(f'<a href="#{k}">{E(v)}</a>' for k, v in u["nav"])
    data = json.dumps(js_data(lang), ensure_ascii=False, separators=(",", ":"))
    ui = json.dumps({"play": u["play"], "pause": u["pause"]}, ensure_ascii=False)
    head = f'''<!doctype html><html lang="{lang}" translate="no" class="notranslate"><head>
<meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1"><meta name="google" content="notranslate">
{GOOGLE_ESCAPE}
<title>{E(u["title"])} · {E(u["other_title"])}</title>
<meta name="description" content="{E(u["desc"])}">
<link rel="canonical" href="{url}">
<link rel="alternate" hreflang="en" href="{BASE}"><link rel="alternate" hreflang="th" href="{BASE}th/"><link rel="alternate" hreflang="x-default" href="{BASE}">
<meta property="og:type" content="website"><meta property="og:site_name" content="Bag Knots · มัดถุง">
<meta property="og:title" content="{E(u["title"])} · {E(u["other_title"])}"><meta property="og:description" content="{E(u["desc"])}"><meta property="og:url" content="{url}">
<meta property="og:image" content="{BASE}card.jpg"><meta property="og:image:secure_url" content="{BASE}card.jpg"><meta property="og:image:type" content="image/jpeg">
<meta property="og:image:width" content="1200"><meta property="og:image:height" content="630">
<meta property="og:image:alt" content="NaN and Beer behind a shop counter with giant ribbon scissors, a puffed curry bag tied with a red bow, an onsen egg, pad krapow and a string of sauce baggies">
<meta property="og:locale" content="{"en_US" if lang == "en" else "th_TH"}"><meta property="og:locale:alternate" content="{"th_TH" if lang == "en" else "en_US"}">
<meta name="twitter:card" content="summary_large_image">
<link rel="icon" href="{root}icon.svg" type="image/svg+xml">
<link rel="preconnect" href="https://fonts.googleapis.com"><link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
<link href="https://fonts.googleapis.com/css2?family=Fraunces:opsz,wght@9..144,700&family=Noto+Sans+Thai:wght@400;600;700&family=Noto+Serif+Thai:wght@700&display=swap" rel="stylesheet">
<style>{CSS}</style></head><body>
<header class="top"><div class="in"><a class="brand" href="#top"><img src="{root}icon.svg" alt="" width="28" height="28"><span>{E(u["title"])}</span></a>
<nav>{nav}</nav>
<span class="lang"><b>{E(u["lang_this"])}</b> | <a href="{other[0]}" hreflang="{other[2]}">{E(other[1])}</a></span></div></header>
<main id="top">'''
    main = f'''<section class="hero"><img class="hero-img" src="{root}img/hero.svg" alt="NaN and Beer behind a shop counter. NaN holds giant gold ribbon scissors; a puffed curry bag stands between them with a red bow on its neck; an onsen egg, a box of pad krapow and a string of sauce baggies are in the way." width="1600" height="900">
<div class="in"><p class="kick">{E(u["kicker"])}</p><h1>{E(u["title"])} <span>{E(u["other_title"])}</span></h1>
<p class="intro">{E(u["lede"])}</p>{talk(lang, u["open"])}</div></section>
<section class="sec" id="band"><div class="in"><p class="kick">{E(u["band_kick"])}</p><h2>{E(u["band_h"])}</h2><p>{E(u["band_p"])}</p>
{band_html}</div></section>
<section class="sec alt" id="plain"><div class="in"><p class="kick">{E(u["plain_kick"])}</p><h2>{E(u["plain_h"])}</h2><p>{E(u["plain_p"])}</p>
{plain_html}</div></section>
<section class="sec scis" id="scissors"><div class="in"><p class="kick">{E(u["scis_kick"])}</p><h2>{E(u["scis_h"])}</h2>
<div class="scis-g"><img src="{root}img/scissors.svg" alt="" width="420" height="200" loading="lazy">{talk(lang, u["scis_say"])}</div>
<ol class="rules">{"".join(f"<li>{E(r)}</li>" for r in u["rules"])}</ol>
<div class="tbl"><table><thead><tr><th scope="col">{E(u["tbl"][0])}</th><th scope="col">{E(u["tbl"][1])}</th><th scope="col">{E(u["tbl"][2])}</th></tr></thead><tbody>{rows}</tbody></table></div>
{talk(lang, u["end_say"])}</div></section>
<section class="sec" id="sources"><div class="in"><h2>{E(u["sources_h"])}</h2><ul class="src">{src}</ul><p class="note">{E(u["sources_note"])}</p></div></section>
</main>'''
    tail = f'''<footer class="bot"><div class="in">{E(u["foot"])} · <a href="https://github.com/NaNoBotCo/bag-knots">GitHub</a> · <a href="https://motdang.net/">motdang.net</a> · <a href="https://hongdam.net/">hongdam.net</a></div></footer>
<script>window.KNOTS={data};window.KNOTS_UI={ui};</script>
<script src="{root}app.js"></script><script src="{root}top.js"></script>
</body></html>
'''
    return (head + main + tail).replace("{root}", root)


def llms():
    L = ["# Bag Knots · มัดถุง", "", U["en"]["desc"], "", f"English: {BASE}", f"Thai: {BASE}th/", ""]
    for t in TIES:
        L.append(f"## {t['en']} · {t['th']}")
        L.append(t["where_en"])
        for ph, name in (("make", "Make"), ("hand", "By hand"), ("scis", "Scissors")):
            st = [s[3] for s in t["steps"] if s[0] == ph]
            if st:
                L.append(f"{name}: " + " ".join(st))
        L.append("")
    L.append("## Scissors")
    L += ["- " + r for r in U["en"]["rules"]]
    L += ["", "## Sources"] + [f"- {p}: {ti} {h}" for p, ti, h, _, _ in SOURCES]
    return "\n".join(L) + "\n"


def main():
    os.makedirs(os.path.join(DOCS, "th"), exist_ok=True)
    open(os.path.join(DOCS, "index.html"), "w").write(page("en"))
    open(os.path.join(DOCS, "th", "index.html"), "w").write(page("th"))
    open(os.path.join(DOCS, "llms.txt"), "w").write(llms())
    open(os.path.join(DOCS, "robots.txt"), "w").write(f"User-agent: *\nAllow: /\nSitemap: {BASE}sitemap.xml\n")
    open(os.path.join(DOCS, "sitemap.xml"), "w").write(
        '<?xml version="1.0" encoding="UTF-8"?>\n<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">\n'
        f"<url><loc>{BASE}</loc></url>\n<url><loc>{BASE}th/</loc></url>\n</urlset>\n")
    open(os.path.join(DOCS, "icon.svg"), "w").write(
        '<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 64 64"><rect width="64" height="64" rx="14" fill="#C9485A"/>'
        '<path d="M22 6 L42 6 L35 22 L35 30 Q52 34 52 46 Q52 58 32 58 Q12 58 12 46 Q12 34 29 30 L29 22Z" fill="#FBF3E4" fill-opacity=".92"/>'
        '<path d="M14 46 Q32 52 50 46 Q50 57 32 57 Q14 57 14 46Z" fill="#E0601F"/>'
        '<ellipse cx="32" cy="24" rx="6" ry="2" fill="none" stroke="#D6A42C" stroke-width="2.4"/><ellipse cx="32" cy="27.5" rx="6" ry="2" fill="none" stroke="#D6A42C" stroke-width="2.4"/></svg>')
    print("docs/index.html, docs/th/index.html, llms.txt, robots.txt, sitemap.xml, icon.svg")


if __name__ == "__main__":
    main()
