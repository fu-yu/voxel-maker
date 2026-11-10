# CHANGELOG

## 2026-11-11
- 文字のデモの初期の色をサイトの色に合わせた (オレンジ `#f08a3c` → ボタンと同じ濃いオレンジ茶 `#ad4c0b` のグラデーション)
- 縦長の画面で立体が左右にはみ出すのを修正 (`fitCamera()` が横の視野も見て引きを決める)
- スマホで画面が縮んで表示される不具合を修正 (`index.html` に画面幅の指定 `<meta name="viewport">` を追加)
- 本体の色合いを説明ページに合わせた (生成りとオレンジ。明るい画面・暗い画面の両方)。`index.html` の色の変数だけを変更
- GitHub Pages で公開を開始。公開先の URL を `README.md` と説明ページに記載
- GitHub 公開の準備: `guide.html` (説明ページ) と `tools/build_guide.py`、`README.md` を追加。本体に説明へのリンクを追加 (詳細: sessions/2026-11-11-github-publish.md)
- `LICENSE` (MIT) を追加
- ブランチの決まりを決めた: `main` は公開してよい状態、作業は `work/<名前>` ブランチ、`main` → `gh-pages` は自動 (`.github/workflows/deploy.yml`)

## 2026-11-10
- 一般向けの説明 `docs/public/` を追加 (挿絵 2 枚つき)
