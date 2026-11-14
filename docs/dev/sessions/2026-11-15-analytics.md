# アクセス解析 (Google Analytics / GA4) の導入

日付: 2026-11-15

## 目的
検索だけでなく、Zenn や X などからの流入や各ページの閲覧状況を把握するため、Google Analytics (GA4) の計測タグを導入する。

## やったこと
- `index.html`: `<head>` 内に GA4 (`G-95MYCKFBXJ`) の `gtag.js` タグを追加した。また「ページの一覧」の下に、Google アナリティクスとクッキーの利用案内 (`guide.html#analytics` へのリンクつき) を追加した。
- `tools/build_guide.py`: `HEAD` に同じ `gtag.js` タグを追加し、`add_site_nav()` 内の全ページ共通の「ページの一覧」の下にもアクセス解析とクッキーの案内・リンクを追加して、`python3 tools/build_guide.py` で生成ページ 7 つ (`guide.html`, `minecraft.html`, `tried/*.html`) に反映した。
- `docs/public/index.md`, `docs/public/index.html`, `guide.html`: Google アナリティクス利用規約 (プライバシー通知) に沿って「アクセス解析とクッキーについて」の項目を追加した (GA4 を使用していること、クッキーを使うが個人を特定する情報は収集しないこと、Google の解説ページ `https://www.google.com/intl/ja/policies/privacy/partners/` へのリンク、ブラウザ設定でクッキーを無効にできること)。

## 確認したこと / していないこと
| 項目 | 状態 |
| --- | --- |
| 全 8 ページに計測タグ (`G-95MYCKFBXJ`) と案内/リンクが入っていること | 確認済み (`grep` で 8 ファイルすべてに一致) |
| 生成ページの再組み立て (`python3 tools/build_guide.py`) | 確認済み (エラーなし) |
| 本体 (`index.html`) および各生成ページの画面表示での見た目・リンク確認 | **未確認** (コードの追加・組み立てのみ) |
| 公開ページでの表示とリンクの確認 | **未確認** (`main` に取り込んで公開した後に行う) |
| GA4 管理画面 (リアルタイムレポート等) で計測数が上がること | **未確認** (公開後にユーザーと確認する) |

## 残っている課題・次にやること
- `work/analytics` の差分をユーザーに確認してもらい、了承を得てから `main` に取り込んで公開する。
- 公開後、GA4 のリアルタイムレポート等でアクセスが計測されていることを確認してから、記録を更新する。
