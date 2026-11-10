#!/bin/bash
# 公開に必要なファイルだけを gh-pages ブランチに置く。自動では動かない。公開したいときに手で実行する。
# 使い方: bash tools/publish_pages.sh
set -euo pipefail
ROOT="$(cd "$(dirname "$0")/.." && pwd)"
cd "$ROOT"
if [ -n "$(git status --porcelain)" ]; then echo "コミットしていない変更があります。先にコミットしてください。" >&2; exit 1; fi
python3 tools/build_guide.py
if [ -n "$(git status --porcelain)" ]; then echo "guide.html が古かったので作り直しました。コミットしてからもう一度実行してください。" >&2; exit 1; fi
SHA="$(git rev-parse --short HEAD)"
URL="$(git remote get-url origin)"
SITE="$(mktemp -d)"
mkdir -p "$SITE/docs/public"
cp index.html guide.html LICENSE "$SITE/"
cp -R docs/public/images "$SITE/docs/public/"
touch "$SITE/.nojekyll"
cd "$SITE"
git init -q -b gh-pages
git config user.name "$(git -C "$ROOT" config user.name)"
git config user.email "$(git -C "$ROOT" config user.email)"
git add -A
git commit -q -m "公開: $SHA"
git push -f "$URL" gh-pages
echo "gh-pages に送りました (main の $SHA)"
