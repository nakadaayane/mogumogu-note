# もぐもぐノート

SNS（X・Instagram・TikTok・YouTube）で話題になったレシピを集めたレシピサイト。

- 公開ページ：https://nakadaayane.github.io/mogumogu-note/
- `index.html` … ページ本体
- `recipes.js` … レシピデータ。`window.RECIPES = [...]`
- `recipes_tool.py` … `list`（一覧）／`check`（点検）／`add new.json`（足す）

## レシピの足し方

1. 足したいレシピを `new.json`（配列）に書く。項目は下の表のとおり。`added` は書かなくてよい（今日の日付が入る）。
2. `python recipes_tool.py add new.json` … 点検に通ったものだけが `recipes.js` の最後に足される。
3. `git commit` → `git push`。1〜2分でページに反映される。

| 項目 | 中身 |
|---|---|
| id | 英小文字とハイフン（URLの `#id` になる） |
| title / catch | 料理名／ひとこと紹介（自分の言葉で。30〜45字） |
| platform | X / Instagram / TikTok / YouTube |
| creator / handle | 投稿者名／@アカウント（分からなければ null） |
| sourceUrl | 材料・分量を確かめた元の投稿やレシピページ |
| buzzUrl / buzzYear / buzzNote | 話題になったことを伝える記事／年／ひとこと（いいね数は出典にあるときだけ） |
| category | おかず / 副菜 / ごはんもの / 麺 / パン / スープ / スイーツ / ドリンク |
| genre | 和風 / 洋風 / 中華 / 韓国 / エスニック |
| time / timeEstimated | 分／出典に時間がなく見積もったら true |
| servings / tags / mainIngredients | 分量／かんたん条件／主な食材 |
| ingredients | `{name, amount, group?}` の配列（group は「A」「たれ」など） |
| steps / tip | 作り方（元の文を写さず言い換え）／コツ（なければ null） |
| emoji / photo | カードの絵（photo を入れると写真に替わる） |
| added | 足した日 `yyyy-mm-dd`（add で自動） |

tags は、いまある言葉を使う：レンジだけ・火を使わない・オーブンいらず・包丁いらず・ワンパン・材料5つ以下・混ぜるだけ・冷やすだけ・節約・おつまみ・映え・夜食・作りおき

## 守ること

- 材料・分量は出典で確かめる。推測で埋めない。
- 作り方は自分の言葉で短く。写真は投稿者のものを勝手に載せない（自分で作って撮った写真ならOK）。
- 元の投稿へのリンクを必ず付ける。
- サイト名・画面の文言に「バズ」は使わない。
