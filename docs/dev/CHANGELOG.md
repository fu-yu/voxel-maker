# CHANGELOG

## 2026-11-13
- 検索と共有のための設定を追加: 題、説明文、共有用の画像 (`docs/public/images/og.jpg`) と `og:*`、正式な URL、言語の指定。説明ページに Zenn の記事へのリンク。作業ブランチ `work/seo` (詳細: sessions/2026-11-13-seo.md)
- 「風景を作る」タブを追加。番号から山・水・木のある風景を自動で作る (地形 3 種、季節 3 種)。水の量と木の量は広さの割合。同じ日に `main` に取り込んで公開 (詳細: sessions/2026-11-13-landscape.md)
- 説明ページの「しくみ」の挿絵 (`docs/public/images/parts.jpg`) の影を直した (ばらばらのブロックの影を、表紙とハートと同じ真下にそろえた)

## 2026-11-11
- 見本のドット絵を差し替えた (ゲームのきのこに似ていた図柄 → 説明ページの表紙をもとにしたオレンジのきのこ)
- 書体の選択肢に「へたうま（太い）」(Darumadrop One) と「へたうま（ペン書き）」(Slackside One) を追加。説明ページの書体の数を 5 → 7 に修正
- 文字のデモの初期の色をサイトの色に合わせた (オレンジ `#f08a3c` → 若草色 `#8fbf5a` のグラデーション)
- 縦長の画面で立体が左右にはみ出すのを修正 (`fitCamera()` が横の視野も見て引きを決める)
- スマホで画面が縮んで表示される不具合を修正 (`index.html` に画面幅の指定 `<meta name="viewport">` を追加)
- 本体の色合いを説明ページに合わせた (生成りとオレンジ。明るい画面・暗い画面の両方)。`index.html` の色の変数だけを変更
- GitHub Pages で公開を開始。公開先の URL を `README.md` と説明ページに記載
- GitHub 公開の準備: `guide.html` (説明ページ) と `tools/build_guide.py`、`README.md` を追加。本体に説明へのリンクを追加 (詳細: sessions/2026-11-11-github-publish.md)
- `LICENSE` (MIT) を追加
- ブランチの決まりを決めた: `main` は公開してよい状態、作業は `work/<名前>` ブランチ、`main` → `gh-pages` は自動 (`.github/workflows/deploy.yml`)

## 2026-11-10
- 一般向けの説明 `docs/public/` を追加 (挿絵 2 枚つき)
