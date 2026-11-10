# AI_CONTEXT: voxel-maker (ボクセル工房)

最終更新: 2026-11-11

## これは何か
文字や画像を、立方体 (ボクセル) を積んだ立体に変える、ブラウザだけで動く道具。本体は `index.html` の 1 ファイル。
three.js (r128) と Google Fonts を CDN から読み込む。組み立て (ビルド) はない。

## 現在の状態
| 項目 | 状態 |
| --- | --- |
| 本体 `index.html` | 動作確認済み (2026-11-10、ローカルの静的サーバーで。文字、見本のドット絵、3 つの形、写真のイラスト化、背景を消す、下絵クリック、マス数・厚み、座標データのコピー) |
| 範囲の選択、「下絵をコピー」 | **未確認** (コードを読んだだけ) |
| スマホ幅 (375px) | 配置は切り替わる。文字の立体が左右にはみ出す (カメラの引きが足りない) のは **未解決** |
| GitHub Pages での公開 | 公開中 (https://fu-yu.github.io/voxel-maker/)。2026-11-11 に本体と `guide.html` の表示を確認 (デスクトップ幅と 375px 幅、コンソールエラーなし)。公開元は `gh-pages` ブランチのルート |

## 構成
- `index.html` — 本体
- `guide.html` — 使い方の説明ページ (生成物。手で直さない)
- `docs/public/index.md` — 説明の元原稿 (これが正)
- `docs/public/index.html` — 説明ページの本文 (Artifact 用。`<!doctype>` や `<head>` を持たない形)
- `docs/public/images/` — 挿絵 (AI が作った絵)
- `tools/build_guide.py` — `docs/public/index.html` から `guide.html` を作る
- `.github/workflows/deploy.yml` — `main` への push で `index.html`, `guide.html`, `LICENSE`, `docs/public/images/` だけを `gh-pages` ブランチに強制 push する (`gh-pages` は毎回 1 コミットに作り直される。手で触らない)

## 注意
- 説明を直すときは `docs/public/index.md` と `docs/public/index.html` の両方を直し、`python3 tools/build_guide.py` で `guide.html` を作り直す。
- `docs/public/index.html` は Artifact として公開するための形なので、`<!doctype>`・`<html>`・`<head>`・`<body>` を書かない。
- **ブランチの決まり** (ユーザーが 2026-11-11 に決めた): `main` は常に公開してよい状態。`main` に直接コミットしない。
  作業は `work/<短い名前>` ブランチで行い、push して差分をユーザーに見せ、**ユーザーが良いと言ってから** `main` に取り込む (`git merge --no-ff`)。取り込んだら作業ブランチを消す。
  `main` に取り込む = 公開、という意味になる。常設の `dev` ブランチは作らない。
- 自動化は「`main` → `gh-pages`」の 1 つだけ。これ以外の自動化を入れるときは先にユーザーに確認する。
- このリポジトリは公開。秘密情報、個人名、メールアドレス、ローカルのファイルパスを書かない。
- コミットのメールアドレスは GitHub の noreply アドレスを使う (リポジトリごとの設定に入れてある)。

## 最新のセッション
`docs/dev/sessions/2026-11-11-github-publish.md`
