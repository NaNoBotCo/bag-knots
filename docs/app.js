/* Bag Knots: every tie drawn as keyframes. Data: window.KNOTS (tools/ties.py), words: window.KNOTS_UI. */
(function () {
  "use strict";
  var DATA = window.KNOTS || [], UI = window.KNOTS_UI || {};
  var W = 480, H = 400, CX = 240;
  var REDUCED = window.matchMedia && matchMedia("(prefers-reduced-motion: reduce)").matches;
  var DEF = {g: 0, air: 0, twist: 0, wraps: 0, lock: 0, fold: 0, over: 99, drop: 0, slide: 0, finger: 0, knot: 0, tuck: 0,
    pull: 0, taut: 0, folds: 0, tab: 0, piggy: 0, pfall: 0, straw: 0, string: 0, ice: 0, bowl: 0, scis: 0, sx: 0, sy: 0,
    sa: 0, sc: 1, slim: 0, sever: 0, corner: 0, pour: 0, level: 168, size: 1, roll: 0, band: 0, k: 0, h: 0, bow: 0, jaw: 0,
    seal: 0, tear: 0, label: 0, staple: 0, contents: "curry", arrows: "", style: ""};
  var C = {
    curry: ["#E0601F", ["#B3121F", "#2E7D32", "#F4E3B5"]], tomyum: ["#E98A2E", ["#C1272D", "#7CB342", "#F7E7C6"]],
    green: ["#A3B84A", ["#2E5E1E", "#F4E3B5", "#C1272D"]], soup: ["#E8C066", ["#5E8C31", "#F7F0DC", "#B3121F"]],
    tea: ["#E8892B", []], namplaprik: ["#C98A2B", ["#D62828", "#F1E3B4"]], ice: ["#CBEAF6", []],
    fruit: ["#F6C445", []], rice: ["#F4EEDC", ["#E3D9BF"]], soy: ["#5A2E14", []], crackling: ["#E6B771", []]
  };
  var BAND = "#E07A1F", BAND2 = "#B85B10", ARROW = "#1F5FA8", PLASTIC = "rgba(255,255,255,.42)", EDGE = "rgba(70,76,84,.6)";

  function lerp(a, b, t) { return a + (b - a) * t; }
  function clamp(t) { return t < 0 ? 0 : t > 1 ? 1 : t; }
  function ease(t) { t = clamp(t); return 0.5 - 0.5 * Math.cos(Math.PI * t); }
  function merge(a, b) { var o = {}, k; for (k in a) o[k] = a[k]; for (k in b) if (k !== "reset") o[k] = b[k]; return o; }
  function mix(a, b, t) {
    var o = {}, k;
    for (k in b) o[k] = (typeof b[k] === "number" && typeof a[k] === "number") ? lerp(a[k], b[k], t) : b[k];
    return o;
  }
  function rng(seed) { var s = seed >>> 0 || 1; return function () { s = (s * 1664525 + 1013904223) >>> 0; return s / 4294967296; }; }

  /* ---------- the bag ---------- */
  function wTied(u, st) {
    var tab = st.tab > 0.5;
    if (u < 38) return tab ? 46 : 18 + (38 - u) * 1.65;
    var nw = tab ? 26 : 18 + (st.straw > 0.5 ? 4 : 0);
    if (u < 88) return nw;
    if (u < 150) { var e = ease((u - 88) / 62); return nw + (182 - (nw - 18)) * e + 14 * st.air * e; }
    return 200 + 14 * st.air * Math.sin(Math.min(1, (u - 150) / 170) * Math.PI * 0.9);
  }
  function wOpen(u) { return 150 + 50 * Math.min(1, u / 290); }
  function wAt(u, st) { return lerp(wOpen(u), wTied(u, st), ease(st.g)); }
  function geo(st) { var s = st.size, top = 195 - 165 * s; return {s: s, top: top, y: function (u) { return top + u * s; }}; }

  function bodyPath(ctx, st, G, u0) {
    var s = G.s, u, pts = [];
    ctx.beginPath();
    for (u = u0; u <= 290; u += 3) ctx.lineTo(CX - wAt(u, st) / 2 * s, G.y(u));
    var wb = wAt(290, st) / 2 * s;
    for (var i = 0; i <= 24; i++) { var a = Math.PI - Math.PI * i / 24; ctx.lineTo(CX + wb * Math.cos(a), G.y(290) + 34 * s * Math.sin(a)); }
    for (u = 290; u >= u0; u -= 3) ctx.lineTo(CX + wAt(u, st) / 2 * s, G.y(u));
    ctx.closePath();
  }
  function tipPath(ctx, st, G, u0) {
    var s = G.s, u;
    ctx.beginPath();
    for (u = u0; u <= 40; u += 2) ctx.lineTo(CX - wAt(u, st) / 2 * s, G.y(u));
    for (u = 40; u >= u0; u -= 2) ctx.lineTo(CX + wAt(u, st) / 2 * s, G.y(u));
    if (st.g > 0.6 && st.tab < 0.5) {   // ruffled top edge
      var w0 = wAt(u0, st) * s, n = 8;
      for (var i = n; i >= 0; i--) ctx.lineTo(CX - w0 / 2 + w0 * i / n, G.y(u0) + (i % 2 ? 0 : 5 * s * st.g));
    }
    ctx.closePath();
  }
  function plastic(ctx, s) {
    ctx.fillStyle = PLASTIC; ctx.fill();
    ctx.strokeStyle = EDGE; ctx.lineWidth = Math.max(1.3, 2.2 * s); ctx.lineJoin = "round"; ctx.stroke();
  }
  function contents(ctx, st, G, seed, clipFn) {
    var c = C[st.contents] || C.curry, s = G.s;
    var lv = st.level + st.pour * 110;
    ctx.save(); clipFn(); ctx.clip();
    var y0 = G.y(lv);
    ctx.fillStyle = c[0]; ctx.fillRect(0, y0, W, H);
    ctx.strokeStyle = "rgba(255,255,255,.4)"; ctx.lineWidth = 3 * s;
    ctx.beginPath(); ctx.moveTo(0, y0); ctx.quadraticCurveTo(CX, y0 + 8 * s, W, y0); ctx.stroke();
    var r = rng(seed);
    if (st.contents === "tea" || st.ice > 0.5) {
      for (var i = 0; i < 9; i++) {
        var x = CX + (r() - 0.5) * 150 * s, y = G.y(lv + 20 + r() * 110);
        ctx.save(); ctx.translate(x, y); ctx.rotate(r() * 1.5);
        ctx.fillStyle = "rgba(255,255,255,.55)"; rr(ctx, -13 * s, -13 * s, 26 * s, 26 * s, 6 * s); ctx.fill(); ctx.restore();
      }
    }
    var bits = c[1];
    for (var j = 0; bits.length && j < 22; j++) {
      var bx = CX + (r() - 0.5) * 170 * s, by = G.y(lv + 18 + r() * (300 - lv));
      ctx.fillStyle = bits[j % bits.length];
      ctx.beginPath();
      if (j % 3 === 0) ctx.ellipse(bx, by, 9 * s, 4 * s, r() * 3, 0, Math.PI * 2);
      else ctx.arc(bx, by, (2.5 + r() * 2.5) * s, 0, Math.PI * 2);
      ctx.fill();
    }
    ctx.restore();
  }
  function rr(ctx, x, y, w, h, r) {
    ctx.beginPath(); ctx.moveTo(x + r, y); ctx.arcTo(x + w, y, x + w, y + h, r); ctx.arcTo(x + w, y + h, x, y + h, r);
    ctx.arcTo(x, y + h, x, y, r); ctx.arcTo(x, y, x + w, y, r); ctx.closePath();
  }
  function shine(ctx, G) {
    var s = G.s;
    ctx.strokeStyle = "rgba(255,255,255,.8)"; ctx.lineWidth = 7 * s; ctx.lineCap = "round";
    ctx.beginPath(); ctx.moveTo(CX - 70 * s, G.y(178)); ctx.quadraticCurveTo(CX - 92 * s, G.y(232), CX - 72 * s, G.y(282)); ctx.stroke();
  }

  /* rubber band turns */
  function ringU(i) { return 82 - i * 7.2; }
  function ring(ctx, x, y, rx, ry, frac, lw, part) {
    // part: "back" draws the far half, "front" the near half; frac = how much of the turn exists
    var a0 = Math.PI, a1 = Math.PI + 2 * Math.PI * frac;
    ctx.lineWidth = lw; ctx.lineCap = "round";
    if (part === "back") {
      var e = Math.min(a1, 2 * Math.PI);
      if (e > a0) { ctx.strokeStyle = BAND2; ctx.beginPath(); ctx.ellipse(x, y, rx, ry, 0, a0, e); ctx.stroke(); }
    } else if (a1 > 2 * Math.PI) {
      ctx.strokeStyle = BAND; ctx.beginPath(); ctx.ellipse(x, y, rx, ry, 0, 2 * Math.PI, a1); ctx.stroke();
    }
  }
  function rings(ctx, st, G, part) {
    var s = G.s, n = Math.ceil(st.wraps - 1e-6);
    if (n <= 0) return;
    var fall = st.drop, sl = st.slide;
    for (var i = 0; i < n; i++) {
      var frac = clamp(st.wraps - i), u = ringU(i);
      var rx = (wAt(u, st) / 2 + 2.6) * s, cx = CX;
      if (i >= st.over) { var o = Math.max(clamp(st.fold * 2 - 1), clamp(st.piggy * 2 - 1)); rx += 7 * s * o; cx += 5 * s * o; }
      var y = G.y(u) - fall * 40 * s - sl * (u + 60) * s;
      rx *= 1 + fall * 0.9;
      ctx.globalAlpha = (1 - fall) * (sl > 0.7 ? (1 - sl) / 0.3 : 1);
      ring(ctx, cx, y, rx, 3.6 * s * (1 + fall), frac, 3.4 * s, part);
      ctx.globalAlpha = 1;
    }
  }
  function lockLoop(ctx, st, G, part) {
    var L = st.lock, s = G.s;
    if (L <= 0.001 || L >= 1.999) return;
    var n = Math.max(1, Math.ceil(st.wraps - 1e-6)), uTop = ringU(n - 1), u, rx, a = 1;
    var rxTip = (wAt(0, st) / 2 + 7) * s, rxN = (wAt(31, st) / 2 + 3) * s;
    if (L < 0.5) { u = lerp(uTop, -10, ease(L / 0.5)); rx = lerp((wAt(uTop, st) / 2 + 3) * s, rxTip, ease(L / 0.5)); }
    else if (L <= 1) { u = lerp(-10, 31, ease((L - 0.5) / 0.5)); rx = lerp(rxTip, rxN, ease((L - 0.5) / 0.5)); }
    else if (L < 1.5) { u = lerp(31, -10, ease((L - 1) / 0.5)); rx = lerp(rxN, rxTip, ease((L - 1) / 0.5)); }
    else { u = lerp(-10, -60, ease((L - 1.5) / 0.5)); rx = rxTip; a = 1 - (L - 1.5) / 0.5; }
    var y = G.y(u) - st.slide * 60 * s, yt = G.y(uTop) - st.slide * 60 * s;
    ctx.globalAlpha = a * (st.wraps > 0.01 ? 1 : 0);
    if (part === "front") {
      ctx.strokeStyle = BAND; ctx.lineWidth = 3 * s; ctx.lineCap = "round";
      ctx.beginPath(); ctx.moveTo(CX - (wAt(uTop, st) / 2 + 2.6) * s, yt); ctx.lineTo(CX - rx * 0.9, y);
      ctx.moveTo(CX + (wAt(uTop, st) / 2 + 2.6) * s, yt); ctx.lineTo(CX + rx * 0.9, y); ctx.stroke();
    }
    ring(ctx, CX, y, rx, 3.6 * s, 1, 3.4 * s, part);
    ctx.globalAlpha = 1;
  }
  function twistLines(ctx, st, G) {
    if (st.twist < 0.02 || st.g < 0.8) return;
    var s = G.s;
    ctx.strokeStyle = "rgba(70,76,84," + (0.4 * st.twist) + ")"; ctx.lineWidth = 1.4 * s;
    for (var u = 44; u < 86; u += 6) {
      ctx.beginPath(); ctx.moveTo(CX - 9 * s, G.y(u) + 3 * s); ctx.lineTo(CX + 9 * s, G.y(u) - 3 * s); ctx.stroke();
    }
  }
  function finger(ctx, st, G) {
    if (st.finger < 0.02) return;
    var s = G.s, y = G.y(78), x0 = CX + 26 * s;
    ctx.globalAlpha = st.finger;
    ctx.fillStyle = "#E8B48C"; rr(ctx, x0, y - 10 * s, 120 * s, 20 * s, 10 * s); ctx.fill();
    ctx.fillStyle = "#F6D2BC"; rr(ctx, x0 + 3 * s, y - 7 * s, 14 * s, 12 * s, 5 * s); ctx.fill();
    ctx.strokeStyle = BAND; ctx.lineWidth = 3 * s;
    ctx.beginPath(); ctx.moveTo(CX + 13 * s, y + 2 * s); ctx.lineTo(x0 + 22 * s, y + 9 * s); ctx.stroke();
    ctx.beginPath(); ctx.ellipse(x0 + 24 * s, y, 4 * s, 11 * s, 0, 0, Math.PI * 2); ctx.stroke();
    if (st.knot > 0.02) { ctx.globalAlpha = st.finger * st.knot; ctx.beginPath(); ctx.ellipse(x0 + 34 * s, y, 4 * s, 11 * s, 0, 0, Math.PI * 2); ctx.stroke(); }
    ctx.globalAlpha = 1;
  }
  function knotTail(ctx, st, G) {
    var s = G.s, n = Math.ceil(st.wraps - 1e-6);
    if (n <= 0) return;
    var y = G.y(ringU(n - 1));
    if (st.knot > 0.02 && st.finger < 0.5) {   // the little-finger knot, sitting on the top turn
      ctx.globalAlpha = st.knot; ctx.strokeStyle = BAND; ctx.lineWidth = 3 * s;
      ctx.beginPath(); ctx.ellipse(CX + 15 * s, y - 2 * s, 5 * s, 3 * s, 0.5, 0, Math.PI * 2); ctx.stroke(); ctx.globalAlpha = 1;
    }
    if (st.tuck > 0.02) {
      ctx.globalAlpha = st.tuck; ctx.strokeStyle = BAND; ctx.lineWidth = 3 * s;
      ctx.beginPath(); ctx.moveTo(CX + 14 * s, y); ctx.quadraticCurveTo(CX + 18 * s, y - 16 * s, CX + 8 * s, y - 24 * s * st.tuck); ctx.stroke(); ctx.globalAlpha = 1;
    }
    if (st.pull > 0.02) {
      ctx.strokeStyle = BAND; ctx.lineWidth = 3 * s;
      ctx.beginPath(); ctx.moveTo(CX + 14 * s, y); ctx.lineTo(CX + (14 + 70 * st.pull) * s, y - 30 * s * st.pull); ctx.stroke();
    }
  }
  function straw(ctx, st, G) {
    if (st.straw < 0.02) return;
    var s = G.s, off = (1 - st.straw) * 260, x = CX + 2 * s;
    var y0 = G.y(-70) - off, y1 = G.y(250) - off;
    ctx.save(); ctx.globalAlpha = Math.min(1, st.straw * 2);
    ctx.lineCap = "round"; ctx.strokeStyle = "#F7F7F2"; ctx.lineWidth = 8 * s;
    ctx.beginPath(); ctx.moveTo(x + 10 * s, y0); ctx.lineTo(x, y1); ctx.stroke();
    ctx.strokeStyle = "#E23B5A"; ctx.lineWidth = 8 * s; ctx.setLineDash([7 * s, 9 * s]);
    ctx.beginPath(); ctx.moveTo(x + 10 * s, y0); ctx.lineTo(x, y1); ctx.stroke();
    ctx.restore();
  }
  function string(ctx, st, G) {
    if (st.string < 0.02) return;
    var s = G.s;
    ctx.save(); ctx.strokeStyle = "#EC407A"; ctx.lineWidth = 4 * s; ctx.lineCap = "round";
    ctx.setLineDash([520 * s * st.string, 2000]);
    ctx.beginPath(); ctx.moveTo(CX - 12 * s, G.y(86));
    ctx.bezierCurveTo(CX - 90 * s, G.y(60), CX - 70 * s, G.y(-100), CX, G.y(-104));
    ctx.bezierCurveTo(CX + 70 * s, G.y(-100), CX + 90 * s, G.y(60), CX + 12 * s, G.y(86));
    ctx.stroke(); ctx.restore();
  }
  function bowl(ctx, st, part) {
    if (st.bowl < 0.02) return;
    var y = 318, rx = 168;
    ctx.globalAlpha = st.bowl;
    if (part === "back") {
      ctx.fillStyle = "#E6DECF"; ctx.beginPath(); ctx.ellipse(CX, y, rx, 24, 0, 0, Math.PI * 2); ctx.fill();
    } else {
      ctx.fillStyle = "#FFFFFF";
      ctx.beginPath(); ctx.ellipse(CX, y, rx, 24, 0, 0, Math.PI); ctx.lineTo(CX - rx, y);
      ctx.bezierCurveTo(CX - rx + 6, y + 70, CX - 60, y + 80, CX, y + 80); ctx.bezierCurveTo(CX + 60, y + 80, CX + rx - 6, y + 70, CX + rx, y);
      ctx.fill();
      ctx.strokeStyle = "#283A6E"; ctx.lineWidth = 5;
      ctx.beginPath(); ctx.ellipse(CX, y + 14, rx - 6, 26, 0, 0.15, Math.PI - 0.15); ctx.stroke();
      ctx.strokeStyle = "rgba(0,0,0,.12)"; ctx.lineWidth = 2;
      ctx.beginPath(); ctx.ellipse(CX, y, rx, 24, 0, 0, Math.PI); ctx.stroke();
    }
    ctx.globalAlpha = 1;
  }
  function miniBag(ctx, st, G) {
    if (st.piggy < 0.02) return;
    var s = G.s * 0.36, m = {s: s};
    var x = CX + 46 * G.s + (1 - ease(st.piggy)) * 150 * G.s, top = G.y(60) - 50 * s;
    top += st.pfall * 150; x += st.pfall * 30;
    ctx.save(); ctx.translate(x, top); ctx.rotate(-0.32 + st.pfall * 0.9); ctx.translate(-x, -top);
    var mst = merge(DEF, {g: 1, air: 1, size: s, level: 140});
    var MG = {s: s, top: top, y: function (u) { return top + u * s; }};
    var save = CX; CX = x;
    var clip = function () { bodyPath(ctx, mst, MG, 38); };
    bodyPath(ctx, mst, MG, 38); ctx.fillStyle = PLASTIC; ctx.fill();
    contents(ctx, merge(mst, {contents: "namplaprik"}), MG, 11, clip);
    bodyPath(ctx, mst, MG, 38); ctx.strokeStyle = EDGE; ctx.lineWidth = 1.5; ctx.stroke();
    tipPath(ctx, mst, MG, 0); plastic(ctx, 1);
    CX = save; ctx.restore();
  }

  function drawBalloon(ctx, st, seed) {
    var G = geo(st), s = G.s, u0 = st.tab > 0.5 ? Math.min(30, st.folds * 14) * (1 - ease(st.g)) : 0;
    bowl(ctx, st, "back");
    // back halves of the band go behind the plastic
    rings(ctx, st, G, "back"); lockLoop(ctx, st, G, "back");
    var clip = function () { bodyPath(ctx, st, G, 38); };
    bodyPath(ctx, st, G, 38); ctx.fillStyle = PLASTIC; ctx.fill();
    contents(ctx, st, G, seed, clip);
    bodyPath(ctx, st, G, 38); ctx.strokeStyle = EDGE; ctx.lineWidth = Math.max(1.3, 2.2 * s); ctx.stroke();
    // the tip, folded down beside the neck when fold > 0
    ctx.save();
    if (st.fold > 0.001) { var px = CX, py = G.y(40), ef = ease(st.fold); ctx.translate(px + 4 * s * ef, py); ctx.rotate(ef * Math.PI * 0.96); ctx.scale(1 - 0.55 * ef, 1); ctx.translate(-px, -py); }
    tipPath(ctx, st, G, u0); plastic(ctx, s);
    if (st.tab > 0.5) {   // fold lines on the folded mouth
      ctx.strokeStyle = "rgba(70,76,84,.45)"; ctx.lineWidth = 1.5 * s;
      var nf = Math.round(st.folds);
      for (var f = 1; f <= nf; f++) { var uu = u0 + f * 9; var ww = wAt(uu, st) / 2 * s; ctx.beginPath(); ctx.moveTo(CX - ww, G.y(uu)); ctx.lineTo(CX + ww, G.y(uu)); ctx.stroke(); }
      if (st.g > 0.5) { ctx.globalAlpha = (st.g - 0.5) * 2; ctx.beginPath(); ctx.moveTo(CX - 23 * s, G.y(4)); ctx.lineTo(CX - 6 * s, G.y(36)); ctx.moveTo(CX + 23 * s, G.y(4)); ctx.lineTo(CX + 6 * s, G.y(36)); ctx.stroke(); ctx.globalAlpha = 1; }
    }
    ctx.restore();
    twistLines(ctx, st, G);
    shine(ctx, G);
    straw(ctx, st, G);
    miniBag(ctx, st, G);
    rings(ctx, st, G, "front"); lockLoop(ctx, st, G, "front");
    knotTail(ctx, st, G);
    string(ctx, st, G);
    finger(ctx, st, G);
    if (st.pour > 0.01) {   // sauce running from the snipped corner
      var cx2 = CX + 52 * s, cy2 = G.y(318);
      ctx.strokeStyle = (C[st.contents] || C.curry)[0]; ctx.lineWidth = 4; ctx.lineCap = "round";
      ctx.beginPath(); ctx.moveTo(cx2, cy2);
      for (var i = 1; i <= 12; i++) ctx.lineTo(cx2 + 2 * Math.sin(i + st.pour * 20), cy2 + i * (H - cy2) / 12 * Math.min(1, st.pour * 3));
      ctx.stroke();
    }
    if (st.corner > 0.01) {
      ctx.fillStyle = "#FBF6EC"; ctx.globalAlpha = st.corner;
      ctx.beginPath(); ctx.moveTo(CX + 44 * s, G.y(322)); ctx.lineTo(CX + 66 * s, G.y(306)); ctx.lineTo(CX + 72 * s, G.y(330)); ctx.closePath(); ctx.fill();
      ctx.globalAlpha = 1;
    }
    bowl(ctx, st, "front");
  }

  /* ---------- rolled dry bag ---------- */
  function drawRoll(ctx, st, seed) {
    var yT = 60 + ease(st.roll) * 92, x0 = CX - 88, x1 = CX + 88, yB = 352;
    rr(ctx, x0, yT, x1 - x0, yB - yT, 14); ctx.fillStyle = PLASTIC; ctx.fill();
    ctx.save(); rr(ctx, x0, yT, x1 - x0, yB - yT, 14); ctx.clip();
    ctx.fillStyle = C.rice[0]; ctx.fillRect(x0, 176, x1 - x0, yB);
    var r = rng(seed);
    ctx.fillStyle = "#E1D6B8";
    for (var i = 0; i < 90; i++) { ctx.beginPath(); ctx.ellipse(x0 + r() * 176, 182 + r() * 170, 4, 1.8, r() * 3, 0, Math.PI * 2); ctx.fill(); }
    ctx.restore();
    rr(ctx, x0, yT, x1 - x0, yB - yT, 14); ctx.strokeStyle = EDGE; ctx.lineWidth = 2; ctx.stroke();
    if (st.roll > 0.02) {
      ctx.globalAlpha = clamp(st.roll * 3);
      rr(ctx, x0 - 4, yT - 14, x1 - x0 + 8, 28, 14); ctx.fillStyle = "rgba(235,238,242,.95)"; ctx.fill(); ctx.strokeStyle = EDGE; ctx.stroke();
      ctx.strokeStyle = "rgba(70,76,84,.4)"; ctx.lineWidth = 1.5;
      for (var k = 0; k < 4; k++) { var x = x0 + 30 + k * 40; ctx.beginPath(); ctx.arc(x, yT, 9, -1.2, 1.9); ctx.stroke(); }
      ctx.globalAlpha = 1;
    }
    ctx.fillStyle = "rgba(255,255,255,.75)"; rr(ctx, x0 + 18, 200, 8, 120, 4); ctx.fill();
    if (st.band > 0.02) {
      var by = 248 + st.drop * 150, ext = 92 * ease(st.band);
      ctx.globalAlpha = 1 - st.drop;
      ctx.strokeStyle = BAND; ctx.lineWidth = 4; ctx.lineCap = "round";
      ctx.beginPath(); ctx.moveTo(CX - ext, by); ctx.lineTo(CX + ext, by); ctx.stroke();
      ctx.strokeStyle = BAND2; ctx.lineWidth = 3;
      ctx.beginPath(); ctx.ellipse(CX - ext, by - 3, 4, 4, 0, Math.PI * 0.5, Math.PI * 1.5); ctx.stroke();
      ctx.beginPath(); ctx.ellipse(CX + ext, by - 3, 4, 4, 0, -Math.PI * 0.5, Math.PI * 0.5); ctx.stroke();
      ctx.globalAlpha = 1;
    }
  }

  /* ---------- a knot tied in the bag's own neck ---------- */
  function knotStage(i, n) {
    var pts = [], t, k;
    for (k = 0; k < n; k++) {
      t = k / (n - 1);
      var p;
      if (i === 0) p = [3 * Math.sin(t * 6), -t * 130];
      else if (i === 3) {
        if (t < 0.35) p = [0, -t / 0.35 * 30];
        else if (t < 0.8) { var a = Math.PI + (t - 0.35) / 0.45 * 2 * Math.PI * 0.85; p = [8 + 8 * Math.cos(a), -34 + 8 * Math.sin(a)]; }
        else p = [lerp(2, 10, (t - 0.8) / 0.2), lerp(-36, -70, (t - 0.8) / 0.2)];
      } else {
        var cx = 24, cy = -64, R = 24;
        if (t < 0.35) p = [0, -t / 0.35 * 64];
        else if (t < 0.8) { var b = Math.PI + (t - 0.35) / 0.45 * 2 * Math.PI * 0.82; p = [cx + R * Math.cos(b), cy + R * Math.sin(b)]; }
        else {
          var e = (t - 0.8) / 0.2, b2 = Math.PI + 2 * Math.PI * 0.82, sx = cx + R * Math.cos(b2), sy = cy + R * Math.sin(b2);
          p = i === 1 ? [lerp(sx, -22, e), lerp(sy, -46, e)] : [lerp(sx, cx + 10, e), lerp(sy, -110, e)];
        }
      }
      pts.push(p);
    }
    return pts;
  }
  var KS = [0, 1, 2, 3].map(function (i) { return knotStage(i, 48); });
  function drawKnot(ctx, st, seed) {
    var bst = merge(st, {g: 1, air: 0.7}), G = geo(bst), s = G.s;
    var clip = function () { bodyPath(ctx, bst, G, 70); };
    bodyPath(ctx, bst, G, 70); ctx.fillStyle = PLASTIC; ctx.fill();
    contents(ctx, merge(bst, {ice: 1}), G, seed, clip);
    bodyPath(ctx, bst, G, 70); ctx.strokeStyle = EDGE; ctx.lineWidth = 2; ctx.stroke();
    shine(ctx, G);
    var k = Math.max(0, Math.min(3, st.k)), i = Math.min(2, Math.floor(k)), f = k - i, A = KS[i], B = KS[i + 1];
    var bx = CX, by = G.y(74), sc = 1.15;
    ctx.lineCap = "round"; ctx.lineJoin = "round";
    var path = function () { ctx.beginPath(); for (var j = 0; j < A.length; j++) ctx.lineTo(bx + lerp(A[j][0], B[j][0], f) * sc, by + lerp(A[j][1], B[j][1], f) * sc); };
    path(); ctx.strokeStyle = "rgba(70,76,84,.55)"; ctx.lineWidth = 15; ctx.stroke();
    path(); ctx.strokeStyle = "rgba(250,252,255,.96)"; ctx.lineWidth = 11; ctx.stroke();
    ctx.strokeStyle = "rgba(70,76,84,.35)"; ctx.lineWidth = 1.2;
    for (var j = 2; j < A.length - 2; j += 3) {
      var x = bx + lerp(A[j][0], B[j][0], f) * sc, y = by + lerp(A[j][1], B[j][1], f) * sc;
      ctx.beginPath(); ctx.moveTo(x - 4, y + 2); ctx.lineTo(x + 4, y - 2); ctx.stroke();
    }
    if (k > 2) { ctx.globalAlpha = k - 2; ctx.fillStyle = "rgba(240,243,247,1)"; ctx.strokeStyle = EDGE; ctx.lineWidth = 2; ctx.beginPath(); ctx.ellipse(bx + 9, by - 39, 13, 11, 0.3, 0, Math.PI * 2); ctx.fill(); ctx.stroke(); ctx.globalAlpha = 1; }
  }

  /* ---------- carrier bag handles ---------- */
  function hStage(i, side, n) {
    var pts = [], bx = CX + side * 80, by = 172;
    for (var k = 0; k < n; k++) {
      var t = k / (n - 1), p;
      if (i === 0) p = [lerp(bx, CX + side * 66, t) + side * 14 * Math.sin(Math.PI * t), lerp(by, 56, t)];
      else if (i === 1) p = [lerp(bx, CX - side * 34, t) + side * 10 * Math.sin(Math.PI * t), lerp(by, 66, t) - 20 * Math.sin(Math.PI * t)];
      else if (i === 2) p = t < 0.7 ? [lerp(bx, CX, t / 0.7), lerp(by, 112, t / 0.7) - 16 * Math.sin(Math.PI * t / 0.7)] : [lerp(CX, CX - side * 34, (t - 0.7) / 0.3), lerp(112, 70, (t - 0.7) / 0.3)];
      else p = t < 0.78 ? [lerp(bx, CX, t / 0.78), lerp(by, 106, t / 0.78) - 14 * Math.sin(Math.PI * t / 0.78)] : [lerp(CX, CX - side * 20, (t - 0.78) / 0.22), lerp(106, 80, (t - 0.78) / 0.22)];
      pts.push(p);
    }
    return pts;
  }
  var HS = {"-1": [0, 1, 2, 3].map(function (i) { return hStage(i, -1, 30); }), "1": [0, 1, 2, 3].map(function (i) { return hStage(i, 1, 30); })};
  function drawHandles(ctx, st, seed) {
    var x0 = CX - 102, x1 = CX + 102, y0 = 170, y1 = 356;
    ctx.beginPath(); ctx.moveTo(x0, y0); ctx.lineTo(x1, y0); ctx.lineTo(x1 + 4, y1 - 20); ctx.quadraticCurveTo(x1 + 4, y1, x1 - 16, y1);
    ctx.lineTo(x0 + 16, y1); ctx.quadraticCurveTo(x0 - 4, y1, x0 - 4, y1 - 20); ctx.closePath();
    ctx.fillStyle = PLASTIC; ctx.fill();
    var r = rng(seed);
    for (var i = 0; i < 6; i++) {   // mangoes
      var mx = CX - 70 + (i % 3) * 70 + (r() - 0.5) * 10, my = 300 - Math.floor(i / 3) * 62 + (r() - 0.5) * 8;
      ctx.save(); ctx.translate(mx, my); ctx.rotate(-0.5 + r());
      ctx.fillStyle = i % 2 ? "#F6C445" : "#F2A93B"; ctx.beginPath(); ctx.ellipse(0, 0, 38, 26, 0, 0, Math.PI * 2); ctx.fill();
      ctx.fillStyle = "#7BAA3A"; ctx.beginPath(); ctx.ellipse(-34, -4, 6, 4, 0, 0, Math.PI * 2); ctx.fill(); ctx.restore();
    }
    ctx.strokeStyle = EDGE; ctx.lineWidth = 2; ctx.stroke();
    var h = Math.max(0, Math.min(3, st.h)), i0 = Math.min(2, Math.floor(h)), f = h - i0;
    ctx.lineCap = "round"; ctx.lineJoin = "round";
    [-1, 1].forEach(function (side) {
      var A = HS[side][i0], B = HS[side][i0 + 1];
      var path = function () { ctx.beginPath(); for (var j = 0; j < A.length; j++) ctx.lineTo(lerp(A[j][0], B[j][0], f), lerp(A[j][1], B[j][1], f)); };
      path(); ctx.strokeStyle = "rgba(70,76,84,.5)"; ctx.lineWidth = 22; ctx.stroke();
      path(); ctx.strokeStyle = "rgba(250,252,255,.97)"; ctx.lineWidth = 18; ctx.stroke();
      path(); ctx.strokeStyle = "rgba(70,76,84,.25)"; ctx.lineWidth = 3; ctx.stroke();
    });
    if (h > 1.5) {
      var a = clamp((h - 1.5) * 2), big = h > 2 ? 1 + (h - 2) * 0.35 : 1;
      ctx.globalAlpha = a; ctx.fillStyle = "#F2F4F7"; ctx.strokeStyle = EDGE; ctx.lineWidth = 2;
      ctx.beginPath(); ctx.ellipse(CX, h > 2 ? lerp(110, 104, h - 2) : 110, 15 * big, 12 * big, 0, 0, Math.PI * 2); ctx.fill(); ctx.stroke();
      if (h > 2.2) { ctx.globalAlpha = clamp((h - 2.2) * 1.4); ctx.beginPath(); ctx.ellipse(CX, 88, 14, 11, 0, 0, Math.PI * 2); ctx.fill(); ctx.stroke(); }
      ctx.globalAlpha = 1;
    }
    if (st.bow > 0.02) {
      ctx.globalAlpha = clamp(st.bow * 1.5); ctx.strokeStyle = "rgba(70,76,84,.5)"; ctx.lineWidth = 14;
      var loops = function (col, lw) {
        ctx.strokeStyle = col; ctx.lineWidth = lw;
        ctx.beginPath(); ctx.ellipse(CX - 40, 84, 36, 16, -0.35, 0, Math.PI * 2); ctx.stroke();
        ctx.beginPath(); ctx.moveTo(CX + 8, 106); ctx.quadraticCurveTo(CX + 40, 100, CX + 60, 140); ctx.stroke();
      };
      loops("rgba(70,76,84,.5)", 14); loops("rgba(250,252,255,.97)", 10);
      ctx.fillStyle = "#F2F4F7"; ctx.strokeStyle = EDGE; ctx.lineWidth = 2; ctx.beginPath(); ctx.ellipse(CX, 104, 14, 11, 0, 0, Math.PI * 2); ctx.fill(); ctx.stroke();
      ctx.globalAlpha = 1;
    }
  }

  /* ---------- flat bags: heat seal, staple ---------- */
  function drawFlat(ctx, st, seed) {
    var seal = st.style === "seal", x0 = seal ? CX - 82 : CX - 92, x1 = seal ? CX + 82 : CX + 92;
    var yT = seal ? 92 : 70 + ease(Math.min(st.folds, 2) / 2) * 32, yB = seal ? 330 : 350;
    var tearY = seal ? 128 : yT + 52;
    var body = function () { rr(ctx, x0, yT, x1 - x0, yB - yT, seal ? 6 : 12); };
    var paint = function () {
      body(); ctx.fillStyle = PLASTIC; ctx.fill();
      ctx.save(); body(); ctx.clip();
      var r = rng(seed);
      if (seal) { ctx.fillStyle = C.soy[0]; ctx.fillRect(x0, 178, x1 - x0, yB); ctx.fillStyle = "rgba(255,255,255,.25)"; ctx.fillRect(x0, 178, x1 - x0, 4); }
      else {
        for (var i = 0; i < 26; i++) {
          var x = x0 + 14 + r() * (x1 - x0 - 28), y = 190 + r() * 150;
          ctx.fillStyle = i % 2 ? "#E6B771" : "#D99A4E"; ctx.beginPath();
          for (var q = 0; q < 7; q++) { var a = q / 7 * Math.PI * 2, R = 14 + r() * 9; ctx.lineTo(x + R * Math.cos(a), y + R * 0.7 * Math.sin(a)); }
          ctx.fill();
        }
      }
      ctx.restore();
      body(); ctx.strokeStyle = EDGE; ctx.lineWidth = 2; ctx.stroke();
      if (seal) {   // side seals and the notch
        ctx.strokeStyle = "rgba(70,76,84,.25)"; ctx.lineWidth = 1;
        for (var y = yT + 4; y < yB - 4; y += 5) { ctx.beginPath(); ctx.moveTo(x0 + 2, y); ctx.lineTo(x0 + 10, y); ctx.moveTo(x1 - 10, y); ctx.lineTo(x1 - 2, y); ctx.stroke(); }
        ctx.fillStyle = "#FBF6EC"; ctx.beginPath(); ctx.moveTo(x0 - 1, tearY - 7); ctx.lineTo(x0 + 9, tearY); ctx.lineTo(x0 - 1, tearY + 7); ctx.fill();
        if (st.seal > 0.02) {
          ctx.globalAlpha = st.seal; ctx.fillStyle = "rgba(200,205,212,.7)"; ctx.fillRect(x0, yT, x1 - x0, 22);
          ctx.strokeStyle = "rgba(70,76,84,.45)";
          for (var xx = x0 + 3; xx < x1; xx += 5) { ctx.beginPath(); ctx.moveTo(xx, yT + 2); ctx.lineTo(xx, yT + 20); ctx.stroke(); }
          ctx.globalAlpha = 1;
        } else { ctx.strokeStyle = EDGE; ctx.beginPath(); ctx.moveTo(x0 + 10, yT + 2); ctx.quadraticCurveTo(CX, yT + 14, x1 - 10, yT + 2); ctx.stroke(); }
      } else {
        ctx.strokeStyle = "rgba(70,76,84,.45)"; ctx.lineWidth = 1.5;
        for (var f = 1; f <= Math.round(st.folds); f++) { ctx.beginPath(); ctx.moveTo(x0, yT + f * 9); ctx.lineTo(x1, yT + f * 9); ctx.stroke(); }
        if (st.label > 0.02) {
          var ly = yT - 18 - (1 - ease(st.label)) * 140;
          ctx.fillStyle = "#FFF6DF"; rr(ctx, x0 - 6, ly, x1 - x0 + 12, 58, 4); ctx.fill(); ctx.strokeStyle = "#C9B58A"; ctx.stroke();
          ctx.fillStyle = "#C8102E"; ctx.fillRect(x0 + 18, ly + 14, 110, 9); ctx.fillStyle = "#283A6E"; ctx.fillRect(x0 + 18, ly + 31, 70, 6);
          ctx.fillStyle = "#D6A42C"; ctx.beginPath(); ctx.arc(x1 - 30, ly + 28, 13, 0, Math.PI * 2); ctx.fill();
          if (st.staple > 0.02) {
            ctx.globalAlpha = st.staple; ctx.strokeStyle = "#7D858F"; ctx.lineWidth = 3.5;
            [-50, 50].forEach(function (dx) { ctx.beginPath(); ctx.moveTo(CX + dx - 12, ly + 46); ctx.lineTo(CX + dx + 12, ly + 46); ctx.stroke(); });
            ctx.globalAlpha = 1;
          }
        }
      }
    };
    if (st.tear > 0.01) {
      ctx.save(); ctx.beginPath(); ctx.rect(0, tearY, W, H); ctx.clip(); paint(); ctx.restore();
      ctx.save(); ctx.beginPath(); ctx.rect(0, 0, W, tearY); ctx.clip();
      ctx.translate(x1, tearY); ctx.rotate(-ease(st.tear) * 0.45); ctx.translate(-x1, -tearY - ease(st.tear) * 18);
      paint(); ctx.restore();
    } else paint();
    if (seal && st.jaw > 0.01) {
      var d = (1 - ease(st.jaw)) * 40;
      ctx.fillStyle = "#3C4149"; rr(ctx, x0 - 20, yT - 22 - d, x1 - x0 + 40, 20, 4); ctx.fill(); rr(ctx, x0 - 20, yT + 24 + d, x1 - x0 + 40, 20, 4); ctx.fill();
      ctx.fillStyle = "rgba(255,90,40," + (0.8 * st.jaw) + ")"; ctx.fillRect(x0 - 16, yT - 5 - d, x1 - x0 + 32, 3); ctx.fillRect(x0 - 16, yT + 24 + d, x1 - x0 + 32, 3);
    }
  }

  /* ---------- scissors and arrows ---------- */
  function scissors(ctx, st) {
    if (st.scis < 0.02) return;
    var L = st.slim ? 130 : 150, open = st.sc * (st.slim ? 0.32 : 0.42);
    ctx.save(); ctx.globalAlpha = Math.min(1, st.scis * 1.5);
    ctx.translate(st.sx, st.sy); ctx.rotate(st.sa * Math.PI / 180);
    [-1, 1].forEach(function (sg) {
      ctx.save(); ctx.rotate(sg * open / 2);
      ctx.fillStyle = "#DCE1E7"; ctx.beginPath(); ctx.moveTo(-6, -sg * 6); ctx.lineTo(L, sg * 1.5); ctx.lineTo(L * 0.12, sg * 14); ctx.closePath(); ctx.fill();
      ctx.strokeStyle = "#8C96A1"; ctx.lineWidth = 1.5; ctx.beginPath(); ctx.moveTo(-6, -sg * 6); ctx.lineTo(L, sg * 1.5); ctx.stroke();
      ctx.strokeStyle = "#2F6FB0"; ctx.lineWidth = 10; ctx.lineCap = "round";
      ctx.beginPath(); ctx.moveTo(0, 0); ctx.lineTo(-28, sg * 14); ctx.stroke();
      ctx.beginPath(); ctx.ellipse(-48, sg * 22, 22, 13, sg * 0.3, 0, Math.PI * 2); ctx.stroke();
      ctx.restore();
    });
    ctx.fillStyle = "#1E4F84"; ctx.beginPath(); ctx.arc(0, 0, 5, 0, Math.PI * 2); ctx.fill();
    ctx.restore();
    if (st.sc > 0.5 && st.scis > 0.9 && !st.slim) {   // cut line
      ctx.save(); ctx.setLineDash([6, 6]); ctx.strokeStyle = "rgba(200,16,46,.75)"; ctx.lineWidth = 2;
      ctx.beginPath(); ctx.moveTo(st.sx + 150 * Math.cos(st.sa * Math.PI / 180) - 200, st.sy); ctx.lineTo(st.sx + 320, st.sy); ctx.stroke(); ctx.restore();
    }
  }
  function arrow(ctx, pts, a) {
    if (a <= 0) return;
    ctx.save(); ctx.globalAlpha = a; ctx.strokeStyle = ARROW; ctx.fillStyle = ARROW; ctx.lineWidth = 3.5; ctx.lineCap = "round";
    ctx.beginPath(); pts.forEach(function (p, i) { i ? ctx.lineTo(p[0], p[1]) : ctx.moveTo(p[0], p[1]); }); ctx.stroke();
    var p1 = pts[pts.length - 1], p0 = pts[pts.length - 2], ang = Math.atan2(p1[1] - p0[1], p1[0] - p0[0]);
    ctx.translate(p1[0], p1[1]); ctx.rotate(ang);
    ctx.beginPath(); ctx.moveTo(4, 0); ctx.lineTo(-10, -8); ctx.lineTo(-10, 8); ctx.closePath(); ctx.fill();
    ctx.restore();
  }
  function arc(cx, cy, rx, ry, a0, a1) { var p = []; for (var i = 0; i <= 20; i++) { var a = lerp(a0, a1, i / 20); p.push([cx + rx * Math.cos(a), cy + ry * Math.sin(a)]); } return p; }
  function arrows(ctx, st, a) {
    var G = geo(st), s = G.s, k = st.arrows;
    if (!k) return;
    if (k === "twist") arrow(ctx, arc(CX, G.y(62), 34 * s, 9 * s, 0.2, Math.PI - 0.2), a);
    else if (k === "spin") arrow(ctx, arc(CX, G.y(220), 130 * s, 22 * s, 0.3, Math.PI - 0.3), a);
    else if (k === "unspin") arrow(ctx, arc(CX, G.y(220), 130 * s, 22 * s, Math.PI - 0.3, 0.3), a);
    else if (k === "up") arrow(ctx, [[CX + 46 * s, G.y(70)], [CX + 46 * s, G.y(-30)]], a);
    else if (k === "out") { arrow(ctx, [[CX - 60, 52], [CX - 120, 40]], a); arrow(ctx, [[CX + 60, 52], [CX + 120, 40]], a); }
    else if (k === "pullend") arrow(ctx, [[CX + 40 * s, G.y(40)], [CX + 120 * s, G.y(10)]], a);
    else if (k === "tug") arrow(ctx, [[CX + 50 * s, G.y(80)], [CX + 50 * s, G.y(-30)]], a);
    else if (k === "down") arrow(ctx, [[CX + 120, 240], [CX + 120, 370]], a);
    else if (k === "sip") arrow(ctx, [[CX + 40, G.y(10)], [CX + 40, G.y(-70)]], a);
    else if (k === "pullknot") arrow(ctx, [[CX + 46, 60], [CX + 46, 10]], a);
    else if (k === "push") { arrow(ctx, [[CX + 70, 40], [CX + 30, 70]], a); }
    else if (k === "pushh") { arrow(ctx, [[CX - 150, 120], [CX - 70, 132]], a); arrow(ctx, [[CX + 150, 120], [CX + 70, 132]], a); }
    else if (k === "pullbow") arrow(ctx, [[CX + 66, 146], [CX + 120, 200]], a);
    else if (k === "tear") arrow(ctx, [[CX - 110, 132], [CX - 40, 118], [CX + 60, 112]], a);
  }

  function drawScene(ctx, st, seed) {
    if (st.kind === "roll") drawRoll(ctx, st, seed);
    else if (st.kind === "knot") drawKnot(ctx, st, seed);
    else if (st.kind === "handles") drawHandles(ctx, st, seed);
    else if (st.kind === "flat") drawFlat(ctx, st, seed);
    else drawBalloon(ctx, st, seed);
  }
  function render(ctx, st, seed, a) {
    ctx.clearRect(0, 0, W, H);
    ctx.fillStyle = "#FBF6EC"; ctx.fillRect(0, 0, W, H);
    ctx.fillStyle = "#EFE4CF"; ctx.fillRect(0, 372, W, 28);
    if (st.sever > 0.001) {
      var y = st.sy, e = ease(st.sever);
      ctx.save(); ctx.beginPath(); ctx.rect(0, y, W, H); ctx.clip(); drawScene(ctx, st, seed); ctx.restore();
      ctx.save(); ctx.globalAlpha = 1 - e * 0.85;
      ctx.translate(-90 * e, -50 * e); ctx.translate(CX, y); ctx.rotate(-0.5 * e); ctx.translate(-CX, -y);
      ctx.beginPath(); ctx.rect(0, 0, W, y); ctx.clip();
      drawScene(ctx, merge(st, {bowl: 0}), seed); ctx.restore();
    } else drawScene(ctx, st, seed);
    scissors(ctx, st);
    arrows(ctx, st, a);
  }

  /* ---------- players ---------- */
  function Player(el, tie) {
    var cv = el.querySelector("canvas"), ctx = cv.getContext("2d"), cap = el.querySelector(".cap"), cnt = el.querySelector(".cnt");
    var lis = el.querySelectorAll("li[data-i]"), chips = el.querySelectorAll("[data-phase]"), playB = el.querySelector(".play");
    var steps = tie.steps, n = steps.length, states = [], froms = [], seed = 0, i;
    for (i = 0; i < tie.id.length; i++) seed = seed * 31 + tie.id.charCodeAt(i);
    var base = merge(merge(DEF, tie.base), {kind: tie.kind});
    states[0] = merge(base, steps[0].s); froms[0] = states[0];
    for (i = 1; i < n; i++) {
      var r = steps[i].s.reset;
      froms[i] = (r !== undefined) ? merge(states[r], {arrows: "", bowl: 0, scis: 0, sever: 0}) : states[i - 1];
      states[i] = merge(froms[i], steps[i].s);
    }
    var cur = 0, t0 = 0, playing = false, visible = false, userPaused = false, holdUntil = 0, dpr = 1, dirty = true;
    function size() {
      dpr = Math.min(2, window.devicePixelRatio || 1);
      var w = cv.clientWidth || W; cv.width = Math.round(w * dpr); cv.height = Math.round(w * H / W * dpr);
      ctx.setTransform(cv.width / W, 0, 0, cv.height / H, 0, 0); dirty = true;
    }
    function show(k, animate) {
      cur = k; t0 = performance.now(); holdUntil = 0;
      if (!animate) t0 -= 1e6;
      cap.textContent = steps[k].t; cnt.textContent = (k + 1) + " / " + n;
      lis.forEach(function (li) { li.classList.toggle("on", +li.getAttribute("data-i") === k); });
      chips.forEach(function (c) { c.setAttribute("aria-pressed", c.getAttribute("data-phase") === steps[k].p ? "true" : "false"); });
      dirty = true;
    }
    function frame(now) {
      if (!dirty && !playing) return;
      var ms = Math.max(1, steps[cur].ms), p = clamp((now - t0) / ms);
      var st = mix(froms[cur], states[cur], ease(p));
      st.kind = tie.kind;
      render(ctx, st, seed, Math.min(1, p * 3) * (p < 1 || playing ? 1 : 1));
      dirty = p < 1;
      if (playing && p >= 1) {
        if (!holdUntil) holdUntil = now + (cur === n - 1 ? 2600 : 1100);
        else if (now >= holdUntil) show(cur === n - 1 ? 0 : cur + 1, true);
      }
    }
    function setPlay(on) { playing = on; playB.textContent = on ? UI.pause : UI.play; playB.setAttribute("aria-pressed", on ? "true" : "false"); dirty = true; }
    playB.addEventListener("click", function () { userPaused = playing; setPlay(!playing); if (playing && cur === n - 1) show(0, true); });
    el.querySelector(".prev").addEventListener("click", function () { setPlay(false); userPaused = true; show(Math.max(0, cur - 1), true); });
    el.querySelector(".next").addEventListener("click", function () { setPlay(false); userPaused = true; show(Math.min(n - 1, cur + 1), true); });
    chips.forEach(function (c) {
      c.addEventListener("click", function () {
        var ph = c.getAttribute("data-phase");
        for (var k = 0; k < n; k++) if (steps[k].p === ph) { show(k, true); break; }
        setPlay(!REDUCED); userPaused = REDUCED;
      });
    });
    lis.forEach(function (li) { li.addEventListener("click", function () { setPlay(false); userPaused = true; show(+li.getAttribute("data-i"), true); }); });
    var q = /[?&]s=(\d+)/.exec(location.search);
    var ds = el.getAttribute("data-step");
    size(); show(ds !== null ? +ds : q ? Math.min(n - 1, +q[1]) : 0, false);
    if (q || ds !== null) userPaused = true;
    return {
      frame: frame, size: size, el: el,
      vis: function (v) { visible = v; if (v && !userPaused && !REDUCED && !playing) setPlay(true); if (!v && playing) setPlay(false); }
    };
  }

  var players = [];
  document.querySelectorAll(".tie[data-tie]").forEach(function (el) {
    var id = el.getAttribute("data-tie"), tie = DATA.filter(function (d) { return d.id === id; })[0];
    if (tie) players.push(Player(el, tie));
  });
  if ("IntersectionObserver" in window) {
    var io = new IntersectionObserver(function (es) {
      es.forEach(function (e) { players.forEach(function (p) { if (p.el === e.target) p.vis(e.isIntersecting); }); });
    }, {threshold: 0.45});
    players.forEach(function (p) { io.observe(p.el); });
  }
  var rz;
  addEventListener("resize", function () { clearTimeout(rz); rz = setTimeout(function () { players.forEach(function (p) { p.size(); }); }, 120); });
  (function loop(now) { players.forEach(function (p) { p.frame(now); }); requestAnimationFrame(loop); })(performance.now());
})();
