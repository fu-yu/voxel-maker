# 「試してみた」の正式なアドレスをそろえ、サイトマップに更新日を入れる

日付: 2026-11-17

## 目的
Search Console と GA4 の設定を確かめたあと、Claude が出した小さな直しの案 2 つを、ユーザーが「tried/ にそろえて、更新日も入れて」と頼んだ。

## 前に行ったこと (同じ日、ユーザーの Chrome で)
- 公開ページで、GA4 (`G-95MYCKFBXJ`) の計測タグが 9 ページすべてに入り、クッキーが付くことを確かめた。GA4 の「ボクセル工房」のデータストリームは「過去 48 時間にデータを受信」。
- Zenn のアカウント設定には別の測定 ID (`G-7LJBDWMW39`) が入っている。Zenn の記事は Search Console には登録できない (`zenn.dev` の持ち主ではないため)。
- Search Console: サイトマップは 2026-11-16 に送信済みで「取得できませんでした」。ユーザーの了承を得て送り直した。トップページは URL 検査で「Google に登録されています」。ほかの 8 ページは「Google に認識されていない」だったので、ユーザーの了承を得て 1 ページずつ登録をリクエストした (秋のページは 2 回目で完了を確認)。

## やったこと
- `tools/build_guide.py`
  - `BASE_URL` と `public_path()` を足した。フォルダの入口の `index.html` は、正式なアドレスを「フォルダ名/」にする (`tried/index.html` → `https://fu-yu.github.io/voxel-maker/tried/`)。`rel="canonical"`, `og:url`, サイトマップがこれを使う。
  - `SITE_PAGES` の「マインクラフトで試してみた」を `tried/` にした。`tried/` の中のページから入口へのリンクは `./` になる。
  - `build_sitemap()`: 各ページに `<lastmod>` を入れた。日付は `updated_dates()` が決める。
  - `updated_dates()`: 生成したページ (本体は `index.html` そのもの) の中身の指紋 (SHA-256 の先頭 16 文字) と日付を `docs/dev/sitemap-dates.json` に残し、指紋が変わったページだけ今日の日付にする。初めて出てくるページは `git log -1 --format=%cs` の日付 (なければ今日)。
    - こうした理由: 公開の自動処理 (`.github/workflows/deploy.yml`) は `actions/checkout@v4` の初期設定で履歴を 1 つしか取らないので、そこで `git log` を使うと全ページが同じ日付になる。自動処理は変えずに済むよう、日付をリポジトリのファイルに持たせた。
- `docs/public/minecraft.*`, `docs/public/tried/*.{html,md}`: `.../tried/index.html` へのリンクを `.../tried/` にした。
- `index.html` (本体): 「ページの一覧」のリンクを `tried/` にした。
- 作業ブランチ `work/sitemap-tidy`。

## 確認したこと / していないこと
| 項目 | 状態 |
| --- | --- |
| サイトマップ | 確認済み (ローカル。9 ページ、`tried/` の形、すべてに `<lastmod>`。XML として読める) |
| 2 回目の組み立てで日付が変わらない | 確認済み (`python3 tools/build_guide.py` をもう一度実行して、`sitemap-dates.json` に差が出ない) |
| `tried/index.html` と `tried/scene.html` の正式なアドレス | 確認済み (`tried/` と `tried/scene.html`) |
| リンク | 確認済み (ローカル。風景のページの「試してみた一覧」と上の一覧が `tried/` を指し、開ける。本体の一覧も `tried/`) |
| 公開の自動処理 (CI) で日付が保たれること | **未確認** (公開後に、公開中の `sitemap.xml` の日付を見る) |
| Search Console がサイトマップを読めるようになるか | **未確認** (数日後) |

最初の日付は、どのページも 2026-11-17 になった (今日の取り込みでどのページも変わっていたため)。

## 残っている課題・次にやること
- ユーザーが良いと言ったら `main` に取り込む。公開後に `sitemap.xml` の日付が 2026-11-17 のままかを見る。
- Search Console でトップページ以外は「登録をリクエスト済み」。数日後にサイトマップの状態と登録の数を見る。
- `tried/index.html` を正式なアドレスとして送ったリクエストは古いアドレスのまま。`tried/` が正式になるので、次に見るとき `tried/` で URL 検査をする。
