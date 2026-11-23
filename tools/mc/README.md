# マインクラフトで確かめるための道具

本体が書き出すデータパックを、公式のサーバー版で確かめるための道具。サーバーのプログラムとワールドは、このリポジトリの外の開発環境のフォルダ (`voxel-maker` のとなりの `voxel-maker-devenv/mc-server/`) に置く。マインクラフトのファイルはリポジトリに入れない。

- `rcon.py`: サーバーにコマンドを送る (RCON。`server.properties` の `rcon.port=25598`、`rcon.password=localtest`。外から入れないよう `server-ip=127.0.0.1`)。
- `recv.py`: ブラウザの「マインクラフト用に保存」の zip を受け取る小さな受け口 (`127.0.0.1:8767`)。ページから `fetch('http://127.0.0.1:8767/<名前>', {method: 'POST', body})` で送ると `<出力フォルダ>/<名前>.zip` に保存する。
- `probe_tree.py`: サーバーに木を生やし (`place feature`)、原木と葉の位置を 1 マスずつ読む。
- `texture_avg.py`: ゲームのクライアントの絵 (PNG) の平均の色を出す。透明のマスは数えない。

## サーバーの用意 (初めてのとき)
1. Mojang の公式の一覧 (`piston-meta.mojang.com/mc/game/version_manifest_v2.json`) から、使う版の `server.jar` の URL と SHA-1 を調べて取り、SHA-1 を照合する。
2. `server.properties` を上の設定にし、平らな世界 (`level-type=minecraft:flat`) にする。`eula.txt` は、ユーザーが利用規約に同意したときだけ `eula=true` にする。
3. 起動: `java -Xmx2G -jar server.jar nogui` (26.3 は Java 25 が要る)。
