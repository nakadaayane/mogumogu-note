"""もぐもぐノートの recipes.js を扱う道具。

  python recipes_tool.py list            … いま載っているレシピ（id・料理名・つくった人）
  python recipes_tool.py check           … recipes.js の中身を点検（ページが壊れないか）
  python recipes_tool.py add new.json    … new.json（配列）のレシピを最後に足し、added を今日にして書き直す
"""
import datetime
import io
import json
import re
import sys
from pathlib import Path

HERE = Path(__file__).resolve().parent
JS = HERE / "recipes.js"
HEADER = "// もぐもぐノートのレシピデータ。新しいレシピは配列の最後に足す（added は足した日）。書き方は README.md\n"

CATEGORIES = {"おかず", "副菜", "ごはんもの", "麺", "パン", "スープ", "スイーツ", "ドリンク"}
GENRES = {"和風", "洋風", "中華", "韓国", "エスニック"}
PLATFORMS = {"X", "Instagram", "TikTok", "YouTube"}
REQUIRED = ["id", "title", "catch", "platform", "creator", "sourceUrl", "buzzYear", "category", "genre",
            "time", "servings", "ingredients", "steps", "emoji", "added"]


def load():
    text = JS.read_text(encoding="utf-8")
    m = re.search(r"window\.RECIPES\s*=\s*(\[.*\])\s*;\s*window\.RECIPES_UPDATED", text, re.S)
    if not m:
        raise SystemExit("recipes.js の形が読めません（window.RECIPES = [...]; window.RECIPES_UPDATED = ...）")
    return json.loads(m.group(1))


def save(recipes):
    updated = max(r["added"] for r in recipes)
    body = ",\n".join("  " + json.dumps(r, ensure_ascii=False) for r in recipes)
    JS.write_text(HEADER + "window.RECIPES = [\n" + body + "\n];\nwindow.RECIPES_UPDATED = \"" + updated + "\";\n",
                  encoding="utf-8", newline="\n")


def problems(recipes):
    errs, seen_id, seen_title = [], set(), set()
    for n, r in enumerate(recipes):
        who = f"{n + 1}品目 {r.get('title', '?')}"
        for k in REQUIRED:
            if r.get(k) in (None, "", []):
                errs.append(f"{who}: {k} がありません")
        rid = r.get("id", "")
        if not re.fullmatch(r"[a-z0-9]+(-[a-z0-9]+)*", str(rid)):
            errs.append(f"{who}: id は英小文字・数字・ハイフンだけにしてください（{rid}）")
        if rid in seen_id:
            errs.append(f"{who}: id が重複しています（{rid}）")
        seen_id.add(rid)
        t = re.sub(r"\s|（.*?）", "", str(r.get("title", "")))
        if t in seen_title:
            errs.append(f"{who}: 同じ料理名がすでにあります")
        seen_title.add(t)
        if r.get("category") not in CATEGORIES:
            errs.append(f"{who}: category は {sorted(CATEGORIES)} のどれか")
        if r.get("genre") not in GENRES:
            errs.append(f"{who}: genre は {sorted(GENRES)} のどれか")
        if r.get("platform") not in PLATFORMS:
            errs.append(f"{who}: platform は {sorted(PLATFORMS)} のどれか")
        if not isinstance(r.get("time"), int) or r["time"] <= 0:
            errs.append(f"{who}: time は分の整数")
        if not isinstance(r.get("buzzYear"), int) or not 2005 <= r["buzzYear"] <= datetime.date.today().year:
            errs.append(f"{who}: buzzYear は西暦の整数")
        for key in ("sourceUrl", "buzzUrl"):
            u = r.get(key)
            if u and not str(u).startswith("https://"):
                errs.append(f"{who}: {key} は https:// で始まるURL")
        for it in r.get("ingredients") or []:
            if not isinstance(it, dict) or not it.get("name"):
                errs.append(f"{who}: 材料に name のないものがあります")
        if not all(isinstance(s, str) and s.strip() for s in r.get("steps") or []):
            errs.append(f"{who}: 作り方に空の手順があります")
        if not re.fullmatch(r"\d{4}-\d{2}-\d{2}", str(r.get("added", ""))):
            errs.append(f"{who}: added は yyyy-mm-dd")
    return errs


def main():
    sys.stdout.reconfigure(encoding="utf-8")
    cmd = sys.argv[1] if len(sys.argv) > 1 else "check"
    recipes = load()
    if cmd == "list":
        for r in recipes:
            print(f"{r['id']}\t{r['title']}\t{r.get('creator', '')}\t{r.get('buzzYear', '')}\t{r['category']}")
        print(f"計 {len(recipes)} 品")
        return
    if cmd == "add":
        new = json.loads(io.open(sys.argv[2], encoding="utf-8").read())
        if isinstance(new, dict):
            new = [new]
        today = datetime.date.today().isoformat()
        for r in new:
            r["added"] = today
            r["tags"] = list(dict.fromkeys(r.get("tags") or []))
        merged = recipes + new
        errs = problems(merged)
        if errs:
            print("足せませんでした。直してからもう一度：")
            print("\n".join(errs))
            sys.exit(1)
        save(merged)
        print(f"{len(new)} 品を足しました（計 {len(merged)} 品）：" + "、".join(r["title"] for r in new))
        return
    errs = problems(recipes)
    if errs:
        print("\n".join(errs))
        sys.exit(1)
    print(f"OK：{len(recipes)} 品、問題なし")


if __name__ == "__main__":
    main()
