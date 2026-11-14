#!/usr/bin/env python3
"""docs/public/ の本文だけの HTML から、単体で開ける guide.html と、SUB_PAGES のページ (minecraft.html など) を作る。

使い方: python3 tools/build_guide.py
"""
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
HEAD = """<!doctype html>
<html lang="ja">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1, viewport-fit=cover">
<meta name="description" content="ボクセル工房の使い方の説明です。文字・画像・風景をブロックの立体にする手順と、できること・できないことをまとめています。">
<link rel="canonical" href="https://fu-yu.github.io/voxel-maker/guide.html">
<meta property="og:type" content="website">
<meta property="og:site_name" content="ボクセル工房">
<meta property="og:locale" content="ja_JP">
<meta property="og:title" content="ボクセル工房のてびき — 使い方とできること">
<meta property="og:description" content="ボクセル工房の使い方の説明です。文字・画像・風景をブロックの立体にする手順と、できること・できないことをまとめています。">
<meta property="og:url" content="https://fu-yu.github.io/voxel-maker/guide.html">
<meta property="og:image" content="https://fu-yu.github.io/voxel-maker/docs/public/images/og.jpg">
<meta property="og:image:width" content="1200">
<meta property="og:image:height" content="630">
<meta property="og:image:alt" content="ブロックを積んで作った、山と湖と木のある小さな風景。左に「ボクセル工房」の文字">
<meta name="twitter:card" content="summary_large_image">
<style>body{margin:0}img{max-width:100%}[hidden]{display:none!important}</style>
"""
OPEN_APP = '<p class="open"><a href="./">ボクセル工房を開く</a></p>'
OPEN_CSS = ".open a{display:inline-block;font-weight:700;color:var(--bg);background:var(--fg);padding:8px 18px;text-decoration:none}.open a:focus-visible{outline:3px solid var(--orange);outline-offset:2px}"


GUIDE_URL = "https://fu-yu.github.io/voxel-maker/guide.html"
GUIDE_DESC = "ボクセル工房の使い方の説明です。文字・画像・風景をブロックの立体にする手順と、できること・できないことをまとめています。"
GUIDE_TITLE = "ボクセル工房のてびき — 使い方とできること"
# 本文だけのページ: (ファイル名, 説明文, 共有したときの題)
SUB_PAGES = [
    ("minecraft.html", "ボクセル工房で作った立体を、マインクラフト (Java 版) のワールドに置く手順です。保存したファイルを入れて、コマンドを 1 つ打ちます。", "マインクラフトに置く — ボクセル工房"),
    ("tried.html", "ボクセル工房で作った立体を、本物のマインクラフトに置いて確かめた記録です。うまくいったことも、見つけた問題も書いています。", "マインクラフトで試してみた — ボクセル工房"),
]


# すべてのページの一覧。ここに足すと、どのページの「ページの一覧」にも出る: (ファイル名, 名前, ひとことの説明)
SITE_PAGES = [
    ("./", "ボクセル工房", "文字・画像・風景を、ブロックの立体にする道具です。"),
    ("guide.html", "てびき", "使い方と、できること・できないことの説明です。"),
    ("minecraft.html", "マインクラフトに置く", "作った立体を、マインクラフトのワールドに置く手順です。"),
    ("tried.html", "マインクラフトで試してみた", "本物のマインクラフトに置いて確かめた、写真つきの記録です。"),
]
NAV_CSS = (
    ".sitenav{display:flex;flex-wrap:wrap;gap:8px;font-size:14px;margin:0}"
    ".sitenav a{padding:3px 10px;border:1px solid var(--line);background:var(--surface);color:var(--fg);text-decoration:none;font-weight:700}"
    ".sitenav a[aria-current]{background:var(--fg);border-color:var(--fg);color:var(--bg)}"
    ".sitenav a:focus-visible,.siteindex a:focus-visible{outline:3px solid var(--orange);outline-offset:2px}"
    ".siteindex ul{list-style:none;padding:0;gap:10px}"
    ".siteindex li{background:var(--surface);border:1px solid var(--line);padding:12px 16px;display:flex;flex-direction:column;gap:2px}"
    ".siteindex li a{font-weight:700}.siteindex li span{font-size:14px;color:var(--muted)}"
)


def add_site_nav(body: str, current: str) -> str:
    """ページの上に短い一覧を、下に説明つきの一覧を入れる。current は今のページのファイル名。"""
    top = '<nav class="sitenav" aria-label="ページの一覧">' + "".join(
        f'<a href="{href}"' + (' aria-current="page"' if href == current else "") + f">{name}</a>" for href, name, _ in SITE_PAGES
    ) + "</nav>"
    items = "\n".join(f'    <li><a href="{href}">{name}</a><span>{desc}</span></li>' for href, name, desc in SITE_PAGES if href != current)
    bottom = f'<section class="siteindex">\n  <h2>ページの一覧</h2>\n  <ul>\n{items}\n  </ul>\n</section>\n\n'
    for marker in ('<div class="page">\n', "<footer>", "</style>"):
        assert body.count(marker) == 1, marker
    body = body.replace('<div class="page">\n', '<div class="page">\n' + top + "\n", 1)
    body = body.replace("<footer>", bottom + "<footer>", 1)
    return body.replace("</style>", NAV_CSS + "\n</style>", 1)


def shared_style() -> str:
    """docs/public/index.html の <style> の中身 (説明ページ共通の見た目)。"""
    body = (ROOT / "docs/public/index.html").read_text(encoding="utf-8")
    return body[body.index("<style>") + len("<style>"):body.index("</style>")]


def build_guide() -> None:
    body = (ROOT / "docs/public/index.html").read_text(encoding="utf-8")
    body = body.replace('src="images/', 'src="docs/public/images/')
    body = body.replace("</style>", OPEN_CSS + "\n</style>", 1)
    marker = '<figure><img src="docs/public/images/cover.jpg"'
    assert marker in body, "表紙の画像が見つかりません"
    body = body.replace(marker, OPEN_APP + "\n  " + marker, 1)
    body = add_site_nav(body, "guide.html")
    style_end = body.index("</style>") + len("</style>")
    out = HEAD + body[:style_end] + "\n</head>\n<body>\n" + body[style_end:] + "</body>\n</html>\n"
    (ROOT / "guide.html").write_text(out, encoding="utf-8")
    print("guide.html を書き出しました")


def build_sub(name: str, desc: str, title: str) -> None:
    """docs/public/<name> (そのページだけの決まり + 本文) に、共通の見た目を足して、単体で開ける <name> を作る。"""
    for part in (GUIDE_URL, GUIDE_DESC, GUIDE_TITLE):
        assert part in HEAD, part
    head = HEAD.replace(GUIDE_URL, "https://fu-yu.github.io/voxel-maker/" + name).replace(GUIDE_DESC, desc).replace(GUIDE_TITLE, title)
    body = (ROOT / "docs/public" / name).read_text(encoding="utf-8")
    body = body.replace("<style>", "<style>" + shared_style(), 1)
    body = body.replace('src="images/', 'src="docs/public/images/')
    # 公開ページの中では、同じ場所のページどうしを短いアドレスでつなぐ
    body = body.replace('href="https://fu-yu.github.io/voxel-maker/"', 'href="./"').replace('href="https://fu-yu.github.io/voxel-maker/', 'href="')
    body = add_site_nav(body, name)
    style_end = body.index("</style>") + len("</style>")
    out = head + body[:style_end] + "\n</head>\n<body>\n" + body[style_end:] + "</body>\n</html>\n"
    (ROOT / name).write_text(out, encoding="utf-8")
    print(name + " を書き出しました")


def main() -> None:
    build_guide()
    for page in SUB_PAGES:
        build_sub(*page)


if __name__ == "__main__":
    main()
