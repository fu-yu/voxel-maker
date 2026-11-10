# GitHub で公開する準備

日付: 2026-11-11

## 目的
ユーザーが「GitHub に公開したい」と頼んだ。範囲は voxel-maker だけ、公開 (Public)、GitHub Pages でだれでも開けるようにする、と決まった。

## やったこと
- `index.html`: 見出しの下の説明文に、`guide.html` へのリンク「使い方の説明」を追加
- `tools/build_guide.py`: 追加。Artifact 用の `docs/public/index.html` に `<!doctype>` と `<head>` を付け、画像のパスを直し、「ボクセル工房を開く」ボタンを足して `guide.html` を書き出す
- `guide.html`: 上の道具で生成
- `docs/public/index.md`, `docs/public/index.html`: 「公開の場所は用意していません」の注意を削除、更新履歴に 2026-11-11 を追加
- `README.md`, `.gitignore`: 追加
- 手元で `git init` (ブランチ `main`) し、最初のコミットを作成

## 確認したこと / していないこと
| 項目 | 状態 |
| --- | --- |
| `guide.html` の表示 | 確認済み (ローカルの静的サーバー。文字コード UTF-8、標準モード、横スクロールなし、画像 2 枚読み込み、幅 1024px) |
| 本体のリンク「使い方の説明」 | 確認済み (リンクがあること。本体も動く) |
| 公開するファイルに秘密情報・ローカルのパスがないこと | 確認済み (`grep` で検索) |
| GitHub への SSH 接続 | 確認済み (`ssh -T git@github.com`) |
| GitHub 側のリポジトリ作成、push、Pages の設定、公開後の表示 | **未完了** |
| `guide.html` のスマホ幅での表示 | **未確認** |

## 会話の中で決まったこと
- 公開するのは voxel-maker だけ。Gemini との協調の道具 (別フォルダ) は出さない。
- 挿絵の絵柄はフラットイラストで確定 (2026-11-10)。
- ライセンスは MIT、著作権の表示の名前は GitHub のアカウント名にする (ユーザーが選んだ)。`LICENSE` を追加し、`README.md` に節を足した。

## 追記: 公開元を gh-pages にする
- ユーザーは、ほかのリポジトリに合わせて `gh-pages` ブランチを公開元にしたいと言った。
- 最初に GitHub Actions (`.github/workflows/deploy.yml`) で `main` への push のたびに `gh-pages` を作る形にして送った。1 回動いて `gh-pages` ができた。
- そのあとユーザーが「自動で別ブランチを作るのは望まない」と言ったので、ワークフローを削除し、手で実行する `tools/publish_pages.sh` に置き換えた。
- `gh-pages` ブランチ自体は、ワークフローが作ったものが GitHub に残っている (中身は公開用のファイルだけ)。

## 試してうまくいかなかったこと
- 頼まれていない自動化 (GitHub Actions) を入れて、取り消すことになった。公開のやり方は先に確認する。
- `gh` コマンドは入っていない。コマンドからリポジトリを作れない。
- アプリ内のブラウザは GitHub にサインインしていない。リポジトリの作成と Pages の設定はユーザーの操作が要る。

## 残っている課題・次にやること
- GitHub に空のリポジトリを作ってもらい、`git remote add origin` と `git push -u origin main` をする。
- Settings → Pages で `main` ブランチのルートを公開元にする。
- 公開後の URL を `docs/public/index.md` と `docs/public/PUBLISHED.md` に書き、表示を確かめる。
