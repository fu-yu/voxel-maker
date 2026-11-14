# 設計書: 「建てる係」つきで少しずつ置く (`voxel:build_slow`)

日付: 2026-11-14
状態: **設計と小さな試しまで終わり。本体 (`index.html`) はまだ変えていない。** 続きは別の担当 (Antigravity) に引き継ぐ。
作業ブランチ: `work/builder`

## 目的
今のデータパックは `/function voxel:build` で立体を一瞬で置く。これに加えて、小さな生き物 (建てる係) が飛び回りながら、
ブロックが少しずつ現れる置き方を足す。MOD もサーバーも要らず、ひとりで遊ぶモードで、データパックを入れるだけで動くこと。

## ユーザーが決めたこと (2026-11-14)
| 項目 | 決定 |
| --- | --- |
| 順番 | 下から 1 段ずつ。段の中は端から端へ |
| 速さ | 風景の初期設定 (約 2 万ブロック) で約 2 分。小さい立体はもっと早く終わる |
| 建てる係の姿 | アレイ (`minecraft:allay`) |
| 終わったら | きらきらして (光の粒と音) 消える。ワールドに何も残さない |
| 本体への入れ方 | 今の `voxel:build` は残す。同じ zip に `voxel:build_slow` を足す。**画面のボタンや選択肢は増やさない** (増やしたくなったら先にユーザーに聞く) |

建てる係に、既存のキャラクターを連想させる名前はつけない (名前の表示はつけない案)。

## 試して確かめたこと (公式のサーバー版 26.3)
小さな試し用のデータパック (石を 1 秒に 1 個、10 個並べる) で確かめた。

| 項目 | 結果 |
| --- | --- |
| `data/minecraft/tags/function/tick.json` と `load.json` で、毎ティックの関数と読み込み時の関数が動く | 動いた |
| 目印 (`marker`) を置き、`execute as <目印> at @s run function …` で、`~` の相対座標が目印を基準に働く | 動いた。`execute align xyz run summon marker ~ ~ ~` で、目印はブロックの角 (整数の座標) に置かれる |
| スコアボードの数え上げ + マクロ (`$function voxel:slow/s$(i)`、`function … with storage …`) で、番号つきの関数を順に呼ぶ | 動いた |
| `execute unless loaded ~x ~ ~z run return 0` と `execute store result score … run function …` で、読み込まれていないときは進めない | 動いた。読み込みを外すと数え上げが止まり、戻すと続きから進んだ |
| 建てている途中で `/reload` | 続きから進んだ (数え上げも建てる係の位置も保たれた) |
| 建てている途中でサーバーを止めて、起動し直す (ワールドを閉じて開き直すのに当たる) | 続きから進み、最後まで終わった |
| 建てている途中で、もう一度 `voxel:build_slow` を実行 | 2 回目は始まらない (`execute if score #on … run return run …`) |
| アレイを `{NoAI:1b,Invulnerable:1b,PersistenceRequired:1b,Silent:1b,NoGravity:1b,Tags:[…]}` で出し、`tp` で動かす | 出せて、動いた (位置の値で確認。見た目は未確認) |

確かめていないこと: ゲームの画面での見た目 (アレイの動き、粒、音、消え方)、26.3 より前の版、本物の立体 (文字・画像・風景) での動き。

### 試しでわかった注意
- サーバーは、誰もいないと 60 秒で時間が止まる (`pause-when-empty-seconds=60`)。試すときは `-1` にする (試し用のサーバーの設定は、もう `-1` に変えてある)。
- `schedule function` は使わない。実行した人の位置を引き継がないうえ、目印 + 数え上げのほうが、途中の状態がワールドに残ってわかりやすい。

## しくみ
状態は 3 つに持つ。どれもワールドに保存されるので、閉じて開き直しても続きから進む。
- 目印: `marker` (タグ `voxel_site`)。最初に立っていた場所に置く。すべての `~` の基準。
- 建てる係: `allay` (タグ `voxel_builder`)。
- スコアボード `voxel` (dummy) の名前つきの値: `#on` (建てている最中は 1)、`#i` (次に実行する段階の番号)、`#t` (待ち時間の数え上げ)、`#run` (何回目の実行か)、`#id` (どのデータパックで始めたか)、`#ok` (読み込みの確認の結果)。

### zip に足すファイル (`data/voxel/function/` の下。今の `build.mcfunction` はそのまま)
`N` は段階の数、`ID` は保存のたびに作る乱数 (1〜2147483647)。文字列は、JSON でも SNBT でも通る「ただの引用符つきの文字列」だけにする (1.21.5 から書式が変わったため)。

`data/minecraft/tags/function/tick.json`: `{"values":["voxel:slow/tick"]}`
`data/minecraft/tags/function/load.json`: `{"values":["voxel:slow/load"]}`

`slow/load.mcfunction`
```
scoreboard objectives add voxel dummy
```

`build_slow.mcfunction` (使う人が打つ)
```
execute if score #on voxel matches 1 run return run tellraw @s "いま建てているところです。やめるときは /function voxel:build_stop"
scoreboard players add #run voxel 1
execute align xyz run summon minecraft:marker ~ ~ ~ {Tags:["voxel_site","voxel_new"]}
execute align xyz run summon minecraft:allay ~2.5 ~1 ~0.5 {NoAI:1b,Invulnerable:1b,PersistenceRequired:1b,Silent:1b,NoGravity:1b,Tags:["voxel_builder","voxel_new"]}
scoreboard players operation @e[tag=voxel_new] voxel = #run voxel
tag @e[tag=voxel_new] remove voxel_new
scoreboard players set #i voxel 0
scoreboard players set #t voxel 0
scoreboard players set #id voxel ID
scoreboard players set #on voxel 1
tellraw @s "建てる係が建てはじめます。やめるときは /function voxel:build_stop"
```

`build_stop.mcfunction` (使う人が打つ)
```
execute unless score #on voxel matches 1 run return run tellraw @s "いまは建てていません"
function voxel:slow/stop
tellraw @s "やめました。置いたブロックはそのまま残ります"
```

`slow/tick.mcfunction` (毎ティック)
```
execute if score #on voxel matches 1 as @e[type=minecraft:marker,tag=voxel_site] at @s run function voxel:slow/next
```

`slow/next.mcfunction` (目印として、目印の場所で動く)
```
execute unless score @s voxel = #run voxel run return run kill @s
execute unless score #id voxel matches ID run return run function voxel:slow/stop
execute as @e[type=minecraft:allay,tag=voxel_builder] unless score @s voxel = #run voxel run function voxel:slow/bye
execute store result score #ok voxel run function voxel:slow/ready
execute if score #ok voxel matches 0 run return 0
scoreboard players add #t voxel 1
execute if score #t voxel matches ..1 run return 0
scoreboard players set #t voxel 0
execute store result storage voxel:slow i int 1 run scoreboard players get #i voxel
function voxel:slow/run with storage voxel:slow
scoreboard players add #i voxel 1
execute if score #i voxel matches N.. run function voxel:slow/done
```
- 1 行目: 前の実行の目印が、読み込まれていない場所に残っていた場合の片づけ。
- 2 行目: 建てている途中で、別の立体のデータパックに入れかえられたら、やめる (段階の中身が混ざるのを防ぐ)。
- `..1` は「2 ティックに 1 段階」の意味。

`slow/ready.mcfunction` (立体の置かれる範囲が、すべて読み込まれているか)
```
execute unless loaded ~X ~ ~Z run return 0     ← 範囲の x と z を 16 マスおきに (両端も) すべての組み合わせで
return 1
```
読み込まれていない所への `fill` は何も置かずに失敗する (前回の記録にある)。置きもらしを防ぐため、範囲の全部が読み込まれているときだけ進める。遠くへ離れると止まり、戻ると続きから進む。

`slow/run.mcfunction`
```
$function voxel:slow/s$(i)
```

`slow/s0.mcfunction` … `slow/s(N-1).mcfunction` (段階ごと)
```
fill / setblock …                       ← この段階のブロック
tp @e[type=minecraft:allay,tag=voxel_builder,limit=1] ~x ~y ~z     ← この段階のまん中のブロックの少し上 (x+2.5, y+1.2, z+0.5 の形)
particle minecraft:end_rod ~x ~y ~z 0.2 0.2 0.2 0.02 1
```

`slow/done.mcfunction`
```
execute at @e[type=minecraft:allay,tag=voxel_builder] run particle minecraft:firework ~ ~0.5 ~ 0.6 0.6 0.6 0.1 60
execute at @e[type=minecraft:allay,tag=voxel_builder] run playsound minecraft:entity.player.levelup neutral @a ~ ~ ~ 1 1.4
tellraw @a "できあがりました"
function voxel:slow/stop
```

`slow/stop.mcfunction`
```
scoreboard players set #on voxel 0
scoreboard players add #run voxel 1
execute as @e[type=minecraft:allay,tag=voxel_builder] at @s run function voxel:slow/bye
kill @e[type=minecraft:marker,tag=voxel_site]
```

`slow/bye.mcfunction` (建てる係を消す。倒れる動きを見せないため、先に下へ移す)
```
tp @s ~ -1000 ~
kill @s
```

粒の名前 (`end_rod`, `firework`) と音の名前は、サーバーで関数が読み込めるかを見て確かめること (粒は名前がちがうと読み込みエラーになる。音は名前がちがってもエラーにならない。ゲームのファイルの一覧に `minecraft/sounds/random/levelup.ogg` があることは確認した)。

## 本体 (`index.html`) の変え方
今ある関数: `mcBlocks()` (立体をブロック名の箱 `{w,h,d,ids,names}` にする)、`mcCommands()` (直方体にまとめる)、`zipStore()`、`#saveMc` の処理。

1. **`mcSteps(B)` を足す**: 置く順番と、段階への分け方を決める。
   - 順番: `y` (下から) → 水かどうか (水はその段の最後) → `z` (行) → `x` (行ごとに向きを逆にして、行ったり来たり)。
   - 段階の数 `N = min(1200, ceil(ブロック数 / 4))`、1 段階のブロック数 `per = ceil(ブロック数 / N)`。順番に並べたブロックを `per` 個ずつ区切る。
     2 ティックに 1 段階なので、風景の初期設定 (約 2 万) は 1,200 段階 = 約 2 分。文字 (3,530) は約 88 秒、見本の画像 (1,060) は約 26 秒、風景の最大 (約 32 万) も約 2 分。
   - 戻り値: マスごとの段階の番号 `stepOf` (Int32Array、空気は -1)、`N`、並べた順 `order`。
2. **`mcCommands(B, stepOf)`**: 2 つ目の引数があるときは、同じブロックで **同じ段階** のマスだけを直方体にまとめ、段階ごとの配列で返す (`free()` の条件に `stepOf[j] === stepOf[i0]` を足す)。引数がないときは今と同じ動き。
3. **`#saveMc` の処理**: 上のファイルを `files` に足す。`build.mcfunction` (60,000 行で分ける今の処理) は変えない。保存したあとの通知に、`voxel:build_slow` でも置けることを書く。

### 水を段の最後に置く理由
水は、まわりにブロックがないと流れ出す (流れは 5 ティック後に始まる)。その段の水以外のブロックと、下の段がすべて置かれてから水を置けば、流れ出す先がない。冬は氷なので関係ない。

## 引き継ぐ人が気をつけること (まだ確かめていない心配)
- **土が草に変わるかもしれない**: 建てている途中、あとで上がふさがる土が、しばらく空の下に出る。近くに草があると草に変わり、上がふさがると土に戻る (どちらもランダムに起きるので時間がかかる)。建て終わった直後と、ゲーム内の 2 分後の照合で、数を見ること。残っても、ふさがれて見えない場所のはず。
  どうしても合わせたいなら、建てている間だけ `randomTickSpeed` を 0 にする手があるが、使う人のワールドの設定を変えるので、先にユーザーに聞く。
- **砂は下がないと落ちる**: 下から置くので落ちないはず。落ちるブロック (`falling_block`) が 0 個かを見ること。
- **段階をまたぐ 1 ティックの中の順番**: 同じ段階の中では、水が先に置かれても、同じティックのうちにまわりが置かれれば流れない (はず。照合で確かめる)。
- 2 つのワールドの入れ物を同時に入れた場合 (ボクセル工房の zip を 2 つ) は、今の `voxel:build` と同じく考えていない。

## 確かめ方 (受け入れの条件)
くわしいやり方は `docs/dev/sessions/2026-11-14-minecraft-java.md` の「サーバー版での確認」。

1. データパックは、ブラウザの保存の処理を差し替えて、本体が作る zip そのものを取り出す。
2. サーバー版 26.3 (平らな世界、RCON) で、`forceload` で場所を読み込み、`execute positioned <位置> run function voxel:build_slow` を実行。`tick sprint` で時間を進め、`#on` が 0 になるのを待つ。
3. 確認用の関数 (ブロック 1 個ずつ `execute unless block`) で、**一気に置く `build.mcfunction` から読み取ったブロックと全部同じ** ことを数える。建て終わった直後と、ゲーム内の 2 分後の 2 回。
4. 対象: 文字 (初期設定)、見本の画像、風景の山と湖の夏・冬・最大の設定。あわせて、水が外に出ていない・落ちるブロックと落とし物がない・目印と建てる係が残っていない、も見る。
5. 関数の読み込みエラーがサーバーの記録に出ていないこと。
6. そのあと、ユーザーにゲームの画面 (Java 版 26.3、ひとりで遊ぶモード) で見てもらう。公開前なので、ローカル版で保存した zip を使ってもらう。

試し用のサーバーは、この Mac の作業用の一時フォルダにある (リポジトリの外。場所は引き継ぎのときに口頭で伝える)。利用規約への同意は、前の作業でユーザーの許可を得て書いたもの。**新しく取り直す・同意を書き直すときは、先にユーザーに聞く。**

## 残りの作業
1. 本体に `mcSteps()` を足し、`mcCommands()` と `#saveMc` の処理を上のとおりに変える。
2. サーバー版で照合する (上の「確かめ方」)。
3. ユーザーにゲームの画面で見てもらう。
4. 記録 (`docs/dev/sessions/`、`CHANGELOG.md`、`docs/AI_CONTEXT.md`) と、使い方の説明 (`docs/public/minecraft.md` と `minecraft.html` → `python3 tools/build_guide.py`)。確かめていない動作を「できる」と書かない。
5. 作業ブランチを push して差分をユーザーに見せる。`main` への取り込み (= 公開) は、ユーザーの「公開して」を待つ。

守る決まりは `docs/AI_CONTEXT.md` の「注意」にある (`main` に直接コミットしない、自動化を勝手に変えない、公開の場所に秘密情報・個人名・ローカルのファイルパスを書かない、ユーザーに見える文は日本語でやさしく)。
