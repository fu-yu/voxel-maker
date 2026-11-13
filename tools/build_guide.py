#!/usr/bin/env python3
"""docs/public/index.html (Artifact 用の本文だけの HTML) から、単体で開ける guide.html を作る。

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


def main() -> None:
    body = (ROOT / "docs/public/index.html").read_text(encoding="utf-8")
    body = body.replace('src="images/', 'src="docs/public/images/')
    body = body.replace("</style>", OPEN_CSS + "\n</style>", 1)
    marker = '<figure><img src="docs/public/images/cover.jpg"'
    assert marker in body, "表紙の画像が見つかりません"
    body = body.replace(marker, OPEN_APP + "\n  " + marker, 1)
    style_end = body.index("</style>") + len("</style>")
    out = HEAD + body[:style_end] + "\n</head>\n<body>\n" + body[style_end:] + "</body>\n</html>\n"
    (ROOT / "guide.html").write_text(out, encoding="utf-8")
    print("guide.html を書き出しました")


if __name__ == "__main__":
    main()
