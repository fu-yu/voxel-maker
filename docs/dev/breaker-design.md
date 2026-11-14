# 設計書: 「壊す係」つきで少しずつ壊す (`voxel:break_slow`)

日付: 2026-11-14
状態: **本体 (`index.html`) への組み込み、ポートを使わない照合 (5 種類)、ゲームの画面での確認 (最大設定の風景)、`tried/break.html` と説明ページの更新まで完了。**
作業ブランチ: `work/breaker`

## 引き継ぎについて
途中でトークン切れや中断が起きた場合は、この設計書 (`docs/dev/breaker-design.md`) と `docs/AI_CONTEXT.md` を見て続きを進めること。
- 確認用のファイルの場所: `/tmp/voxel-mc/` (リポジトリの外。Mac を再起動すると消える)。
- ポートを使う処理 (ローカルのサーバー版 26.3 への RCON 接続や Chrome のリモートデバッグ) は、権限確認で止まりやすいため、省いてよい。まずはポートを使わない 방법 (Node の `vm` で `index.html` から zip を書き出し、`/tmp/voxel-mc/tool/offline_check.py` で照合する) で確認を完結させる。

## 目的
`/function voxel:build` や `/function voxel:build_slow` で置いた立体を、小さな生き物 (壊す係) が飛び回りながら、爆発の粒と音を出しつつ上の段から少しずつ消していく `/function voxel:break_slow` を足す。途中で止める `/function voxel:break_stop` もあわせて足す。

## ユーザーが決めたこと (2026-11-14)
| 項目 | 決定 |
| --- | --- |
| 壊す係の姿 | ヴェックス (`minecraft:vex`) に `{Charging:1b}` (赤い模様が光る姿) をつける |
| 順番 | 上の段から順番に、飛び回りながら爆発させて消していく (水や砂が途中でこぼれない順序) |
| 基準の位置 | 最後に置いた立体の場所 (目印 `marker`、タグ `voxel_site`) を覚えておいて、どこからコマンドを打ってもそこを壊す。記録がなければ、いま立っている場所を基準にする |
| 通過するときの演出 | 移動した場所で爆発の粒 (`minecraft:explosion`, `minecraft:large_smoke`) と軽めの爆発音 (`minecraft:entity.generic.explode`) を出す |
| 終わったとき | 大きな爆発の粒 (`minecraft:explosion_emitter`) と爆発音を出し、「すべて壊しました」と表示して消える。目印 (`voxel_site`) も消す |
| 本体への入れ方 | 同じ zip (`voxel-koubou-datapack.zip`) に `voxel:break_slow` と `voxel:break_stop` を足す。画面のボタンや選択肢は増やさない |

## しくみ

### 1. 最後に置いた場所の記憶 (`voxel_site`)
- `/function voxel:build` (分割時は `build1`) を実行したとき、古い `voxel_site` を消して、いま立っている場所 (ブロックの角) に新しい `voxel_site` を置く。
  ```
  kill @e[type=minecraft:marker,tag=voxel_site]
  execute align xyz run summon minecraft:marker ~ ~ ~ {Tags:["voxel_site","voxel_new"]}
  scoreboard players operation @e[tag=voxel_new] voxel = #run voxel
  tag @e[tag=voxel_new] remove voxel_new
  ```
- `/function voxel:build_slow` を実行したときも、最初に `kill @e[type=minecraft:marker,tag=voxel_site]` で前の目印を消してから新しい `voxel_site` を置く。
- **重要**: `slow/done.mcfunction` (建て終わり) と `build_stop.mcfunction` (途中でやめる) では、`voxel_site` を**消さずに残す**。これにより、建て終わったあとに離れた場所から `/function voxel:break_slow` を打っても、その立体の場所を壊せる。
- `/function voxel:break_slow` を打ったとき、`@e[type=minecraft:marker,tag=voxel_site]` が 1 つもなければ、いま立っている場所に `voxel_site` を作ってそこを壊す。
- 最後まで壊し終わったとき (`break/done.mcfunction`) に `voxel_site` を消す。途中で `/function voxel:break_stop` で止めたときは `voxel_site` を残す (もう一度 `break_slow` を打てば続きや残りを壊せるようにする)。

### 2. スコアボード `#on voxel` の状態
- `0`: 何もしていない
- `1`: 建てている最中 (`voxel:build_slow`)
- `2`: 壊している最中 (`voxel:break_slow`)

`build_slow` 実行時に `#on` が `2` なら「いま壊しているところです。やめるときは /function voxel:break_stop」と出して始めない。
`break_slow` 実行時に `#on` が `1` なら「いま建てているところです。やめるときは /function voxel:build_stop」と出して始めない。

### 3. 水や砂がこぼれない壊し順 (`b0.mcfunction` 〜 `b(N-1).mcfunction`)
建てる段階 `s0` 〜 `s(N-1)` は、「下の段 (`y = 0`) から上の段へ、同じ段の中では水以外 (`dry`) が先、水 (`wet`) が最後」に並んでいる。
したがって、壊す段階 `b0` 〜 `b(N-1)` は **建てる段階の逆順 (`s = N - 1` から `s = 0`)** を基本にする。

- 上の段 (`y + 1`) がすべて消えてから下の段 (`y`) が消えるため、砂が下に落ちない。
- 同じ段 (`y`) の中では、水 (`wet`) が先に消えてから、まわりのガラスや岸 (`dry`) が消えるため、ガラスが先に消えて外へ水があふれることがない。
- **同じ段の水が複数の段階に分かれるときの対策**:
  マインクラフトの水は 5 ティックで隣の空気マスへ流れる。大きな湖で同じ段 (`y`) の水が複数の段階 (複数ティック) に分かれていると、先に消した水マスへ、まだ残っている隣の水源から水が流れ込むことがある。
  これを防ぐため、各段 (`y`) で「その段の水を含む最後の壊す段階 (つまりその段で最初に置かれた水を含む段階)」では、その段 (`y`) の水マスすべてをもう一度 `minecraft:air` で消すコマンドを入れる。これで水源がなくなった瞬間にその段の水がすべて空気になり、流れ残りが 0 になる。

### 4. zip に足す・変更するファイル

`data/minecraft/tags/function/tick.json`:
```json
{"values":["voxel:slow/tick"]}
```
(`slow/tick.mcfunction` の中で `#on` が `1` なら `voxel:slow/next`、`2` なら `voxel:break/next` を呼ぶ)

`slow/tick.mcfunction`:
```
execute if score #on voxel matches 1 as @e[type=minecraft:marker,tag=voxel_site] at @s run function voxel:slow/next
execute if score #on voxel matches 2 as @e[type=minecraft:marker,tag=voxel_site] at @s run function voxel:slow/bnext
```

`break_slow.mcfunction` (使う人が打つ):
```
execute if score #on voxel matches 1 run return run tellraw @s "いま建てているところです。やめるときは /function voxel:build_stop"
execute if score #on voxel matches 2 run return run tellraw @s "いま壊しているところです。やめるときは /function voxel:break_stop"
scoreboard players add #run voxel 1
execute unless entity @e[type=minecraft:marker,tag=voxel_site] align xyz run summon minecraft:marker ~ ~ ~ {Tags:["voxel_site"]}
scoreboard players operation @e[type=minecraft:marker,tag=voxel_site] voxel = #run voxel
execute at @e[type=minecraft:marker,tag=voxel_site,limit=1,sort=nearest] align xyz run summon minecraft:vex ~2.5 ~1 ~0.5 {NoAI:1b,Invulnerable:1b,PersistenceRequired:1b,Silent:1b,NoGravity:1b,Charging:1b,Tags:["voxel_breaker","voxel_new"]}
execute unless entity @e[tag=voxel_breaker] at @e[type=minecraft:marker,tag=voxel_site,limit=1,sort=nearest] align xyz run summon minecraft:allay ~2.5 ~1 ~0.5 {NoAI:1b,Invulnerable:1b,PersistenceRequired:1b,Silent:1b,NoGravity:1b,Tags:["voxel_breaker","voxel_new"]}
scoreboard players operation @e[tag=voxel_new] voxel = #run voxel
tag @e[tag=voxel_new] remove voxel_new
scoreboard players set #i voxel 0
scoreboard players set #t voxel 0
scoreboard players set #id voxel ID
scoreboard players set #on voxel 2
tellraw @s "壊す係が壊しはじめます。やめるときは /function voxel:break_stop"
```

`break_stop.mcfunction` (使う人が打つ):
```
execute unless score #on voxel matches 2 run return run tellraw @s "いまは壊していません"
function voxel:slow/bstop
tellraw @s "やめました。残ったブロックはそのまま残ります"
```

`slow/bnext.mcfunction` (内部用の関数は `/function voxel:b` の入力候補を埋めないよう `slow/` の下に置く):
```
execute unless score @s voxel = #run voxel run return run kill @s
execute unless score #id voxel matches ID run return run function voxel:slow/bstop
execute as @e[tag=voxel_breaker] unless score @s voxel = #run voxel run function voxel:slow/bye
execute unless entity @e[tag=voxel_breaker] align xyz run summon minecraft:allay ~2.5 ~1 ~0.5 {NoAI:1b,Invulnerable:1b,PersistenceRequired:1b,Silent:1b,NoGravity:1b,Tags:["voxel_breaker","voxel_new"]}
scoreboard players operation @e[tag=voxel_new] voxel = #run voxel
tag @e[tag=voxel_new] remove voxel_new
execute store result score #ok voxel run function voxel:slow/ready
execute if score #ok voxel matches 0 run return 0
scoreboard players add #t voxel 1
execute if score #t voxel matches ..1 run return 0
scoreboard players set #t voxel 0
execute store result storage voxel:slow i int 1 run scoreboard players get #i voxel
function voxel:slow/brun with storage voxel:slow
scoreboard players add #i voxel 1
execute if score #i voxel matches N.. run function voxel:slow/bdone
```

`slow/brun.mcfunction`:
```
$function voxel:slow/b$(i)
```

`slow/b0.mcfunction` … `slow/b(N-1).mcfunction` (段階ごと、`s = N - 1 - i` に対応):
```
fill / setblock … minecraft:air
tp @e[tag=voxel_breaker,limit=1] ~x ~y ~z
particle minecraft:explosion ~x ~y ~z 0.4 0.4 0.4 0.05 2
particle minecraft:large_smoke ~x ~y ~z 0.3 0.3 0.3 0.02 3
particle minecraft:flame ~x ~y ~z 0.25 0.25 0.25 0.01 3
playsound minecraft:entity.generic.explode block @a ~x ~y ~z 0.35 1.4
```

`slow/bdone.mcfunction`:
```
execute at @e[tag=voxel_breaker] run particle minecraft:explosion_emitter ~ ~0.5 ~ 0 0 0 0 1
execute at @e[tag=voxel_breaker] run playsound minecraft:entity.generic.explode block @a ~ ~ ~ 0.8 1.0
tellraw @a "すべて壊しました"
function voxel:slow/bstop
kill @e[type=minecraft:marker,tag=voxel_site]
```

`slow/bstop.mcfunction`:
```
scoreboard players set #on voxel 0
scoreboard players add #run voxel 1
execute as @e[type=minecraft:vex,tag=voxel_breaker] at @s run function voxel:slow/bye
```

## 確かめ方 (ポートを使わない)
1. Node の `vm` で `index.html` のスクリプトを動かし、5 種類の zip (`gen_text.zip`, `gen_image.zip`, `gen_lake_summer.zip`, `gen_lake_winter.zip`, `gen_lake_max.zip`) を `/tmp/voxel-mc/packs/` に書き出す。
2. `/tmp/voxel-mc/tool/offline_check.py` を拡張し、次を確かめる:
   - `build` と `slow/s*` の一致 (従来どおり、ちがうブロックの数 0)。
   - `build` (または `slow/s*`) で置いたブロックに対して `break/b0` 〜 `b(N-1)` を順に実行したあと、残るブロックの数が **0** になること。
   - 各段階 `b(i)` を実行する時点で、消そうとしているブロックのすぐ上に砂や水が残っていないこと、および同じ段に水源が残っているうちに外枠のガラスや底の石が消えないこと。
3. `unzip -t`、JSON の構文、段階数の一致を確かめる。
4. ユーザーにゲームの画面で `/function voxel:break_slow` を試してもらう。

## 残りの作業
1. `index.html` に `voxel:break_slow` と `voxel:break_stop` の出力を足す。
2. ポートを使わない照合スクリプトで 5 種類のデータパックを検査する。
3. 説明ページ (`docs/public/minecraft.md`, `docs/public/minecraft.html` → `python3 tools/build_guide.py`) に `voxel:break_slow` と `voxel:break_stop` の案内を足す。
4. ユーザーにゲームの画面で見てもらう。
5. セッション記録 (`docs/dev/sessions/2026-11-14-breaker.md`) と `docs/AI_CONTEXT.md` を更新し、ブランチを push して差分を見せる。
