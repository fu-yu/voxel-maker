"""てびきの「できること・できないこと」のまとめの図 (SVG 2 枚) を作る。色はページの CSS 変数を使う。

使い方: python3 tools/cancan_figure.py <出力先.html>
出力 (<figure class="cancan">…</figure> の 1 行) で、docs/public/index.html の同じ行を差し替え、python3 tools/build_guide.py を動かす。
"""
import sys

S = 13  # cube edge (screen px)
C = 0.866

DIRT, TRUNK, STONE = "#b0845a", "#8a5a36", "#9a9892"


def cube(cx, cy, x, y, z, fill):
    """isometric cube; grid x to the right-down, y to the left-down, z up. (cx, cy) is the screen origin."""
    px = cx + (x - y) * S * C
    py = cy + (x + y) * S * 0.5 - z * S
    top = [(px, py - S), (px + S * C, py - S * 0.5), (px, py), (px - S * C, py - S * 0.5)]
    left = [(px - S * C, py - S * 0.5), (px, py), (px, py + S), (px - S * C, py + S * 0.5)]
    right = [(px, py), (px + S * C, py - S * 0.5), (px + S * C, py + S * 0.5), (px, py + S)]
    pts = lambda ps: " ".join(f"{a:.1f},{b:.1f}".replace(".0,", ",").rstrip("0").rstrip(".") if False else f"{round(a,1):g},{round(b,1):g}" for a, b in ps)
    out = []
    for face, shade in ((top, 0), (left, 14), (right, 28)):
        fill_s = fill if not shade else f"color-mix(in srgb,{fill},#000 {shade}%)"
        out.append(f'<polygon points="{pts(face)}" fill="{fill_s}"/>')
    return "".join(out)


def model(cx, cy, cells, **kw):
    """cells: list of (x, y, z, fill). Drawn back to front."""
    cells = sorted(cells, key=lambda c: (c[0] + c[1] + c[2], c[2]))
    alpha, dash = kw.get("alpha", 1), kw.get("dash", False)
    g = '<g stroke="var(--fg)" stroke-opacity=".28" stroke-width=".8" stroke-linejoin="round"' + (' stroke-dasharray="2 2"' if dash else "") + (f' opacity="{alpha}"' if alpha < 1 else "") + ">"
    return g + "".join(cube(cx, cy, x, y, z, f) for x, y, z, f in cells) + "</g>"


def center(cells):
    """screen offset so that the model's bounding box is centred on (0, 0)."""
    xs, ys = [], []
    for x, y, z, _ in cells:
        px, py = (x - y) * S * C, (x + y) * S * 0.5 - z * S
        xs += [px - S * C, px + S * C]; ys += [py - S, py + S]
    return -(min(xs) + max(xs)) / 2, -(min(ys) + max(ys)) / 2


def place(cx, cy, cells, **kw):
    dx, dy = center(cells)
    return model(cx + dx, cy + dy, cells, **kw)


# ---- models (x: right-down, y: left-down, z: up). Flat things stand in the x-z plane at y=0, facing the viewer's right.
def letter():  # 「工」 orange on top, green at the bottom
    rows = ["#####", "..#..", "..#..", "..#..", "#####"]
    col = ["var(--orange)", "var(--orange)", "#c0a54b", "var(--green)", "var(--green)"]
    return [(x, y, 4 - r, col[r]) for r, row in enumerate(rows) for x, ch in enumerate(row) if ch == "#" for y in (0, 1)]


def heart():
    rows = [".##.##.", "#######", "#######", ".#####.", "..###..", "...#..."]
    return [(x, y, 5 - r, "var(--orange)") for r, row in enumerate(rows) for x, ch in enumerate(row) if ch == "#" for y in (0, 1)]


def island():
    c = []
    for x in range(5):
        for y in range(5):
            water = x >= 3 and y >= 3
            c.append((x, y, 0, DIRT))
            if not water:
                c.append((x, y, 1, "var(--green)"))
            else:
                c.append((x, y, 1, "var(--blue)"))
    c += [(1, 1, 2, TRUNK), (1, 1, 3, TRUNK)]
    c += [(a, b, 4, "var(--green)") for a in (0, 1, 2) for b in (0, 1, 2)] + [(1, 1, 5, "var(--green)")]
    return c


def turntable():
    return [(x, y, z, "var(--cream-block)" if (x + y + z) % 2 else "var(--orange)") for x in range(2) for y in range(2) for z in range(2)]


def pile():
    c = []
    for z, n in ((0, 3), (1, 2), (2, 1)):
        for x in range(n):
            for y in range(n):
                c.append((x + z * 0, y, z, "var(--blue)"))
    c = [(x, y, z, "var(--blue)") for x, y, z, _ in c]
    c = [(x, y, z, "var(--orange)" if (x, y, z) == (2, 2, 0) else f) for x, y, z, f in c]
    return c


def house():
    c = [(x, y, z, "var(--cream-block)") for x in range(3) for y in range(3) for z in range(2)]
    c += [(x, 1, 2, DIRT) for x in range(3)] + [(x, y, 2, DIRT) for x in range(3) for y in (0, 2)]
    c += [(x, 1, 3, DIRT) for x in range(3)]
    return c


def tower():
    return [(0, 0, z, STONE if z % 2 else "var(--cream-block)") for z in range(7)] + [(1, 0, 0, STONE), (0, 1, 0, STONE)]


def text(x, y, s, size=17, w=700, fill="var(--fg)"):
    return f'<text x="{x}" y="{y}" text-anchor="middle" font-size="{size}" font-weight="{w}" fill="{fill}">{s}</text>'


def cross(x, y):
    return (f'<circle cx="{x}" cy="{y}" r="11" fill="var(--surface)" stroke="var(--accent)" stroke-width="2.4"/>'
            f'<path d="M{x-5} {y-5} L{x+5} {y+5} M{x+5} {y-5} L{x-5} {y+5}" stroke="var(--accent)" stroke-width="2.6" stroke-linecap="round"/>')


def panel(title, mark, items, label):
    W, H = 360, 400
    out = [f'<svg viewBox="0 0 {W} {H}" role="img" aria-label="{label}" font-family="inherit">',
           f'<rect x="1" y="1" width="{W-2}" height="{H-2}" rx="14" fill="var(--surface)" stroke="var(--line)" stroke-width="1.5"/>',
           f'<rect x="20" y="22" width="16" height="16" fill="{mark}"/>',
           f'<text x="46" y="37" font-size="20" font-weight="700" fill="var(--fg)">{title}</text>']
    for i, (cells, l1, l2, extra, kw) in enumerate(items):
        cx = 92 + (i % 2) * 176
        top = 58 + (i // 2) * 170
        global S
        S = kw.pop("s", 13)
        if kw.pop("page", False):
            px, py = cx - 30, top + 62 - 44
            out.append(f'<path d="M{px} {py} h44 l16 16 v72 h-60 z" fill="var(--bg)" stroke="var(--muted)" stroke-width="1.8" stroke-linejoin="round"/>'
                       f'<path d="M{px+44} {py} v16 h16" fill="none" stroke="var(--muted)" stroke-width="1.8" stroke-linejoin="round"/>')
        out.append(place(cx, top + 66, cells, **kw))
        if extra:
            out.append(extra(cx, top + 62))
        out.append(text(cx, top + 132, l1))
        out.append(text(cx, top + 154, l2))
    out.append("</svg>")
    return "".join(out)


can = panel("できること", "var(--orange)", [
    (letter(), "文字を", "立体にする", None, {"s": 11}),
    (heart(), "絵や写真を", "立体にする", None, {"s": 10}),
    (island(), "山・水・木の", "風景を作る", None, {"s": 10}),
    (turntable(), "回して眺め、", "保存できる",
     lambda x, y: f'<path d="M{x-48} {y+10} A50 22 0 0 0 {x+48} {y+10}" fill="none" stroke="var(--accent)" stroke-width="2.4"/>'
                  f'<path d="M{x+48} {y+10} l-2 -10 l-8 7 z" fill="var(--accent)"/>', {}),
], "できること: 文字を立体にする、絵や写真を立体にする、山・水・木の風景を作る、回して眺めて保存できる")

cannot = panel("できないこと・注意", "var(--muted)", [
    ([(0, 0, 0, "var(--orange)"), (1, 0, 0, "var(--orange)"), (0, 1, 0, "var(--orange)"), (0, 0, 1, "var(--orange)")], "3D のファイルには", "保存できない",
     lambda x, y: cross(x + 34, y - 30), {"page": True}),
    (pile(), "色は近い", "ブロックになる", None, {}),
    (house(), "家や道は", "作れない", lambda x, y: cross(x + 34, y - 26), {"alpha": .45, "dash": True}),
    (tower(), "数が多いと", "重くなる", None, {}),
], "できないこと・注意: 3D のファイルには保存できない、色は近いブロックに置きかわる、家や道は作れない、ブロックの数が多いと重くなる")

html = f'<figure class="cancan"><div>{can}{cannot}</div><figcaption>ボクセル工房で、できることと、できないこと・注意をまとめた図です。</figcaption></figure>'
open(sys.argv[1], "w", encoding="utf-8").write(html)
print(len(html))
