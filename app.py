import os
from datetime import datetime

from flask import Flask, flash, redirect, render_template, request, url_for


app = Flask(__name__)
app.secret_key = os.environ.get("SECRET_KEY", "local-forum-demo-key")

CATEGORIES = [
    {"id": "all", "name": "全部", "icon": "✳", "color": "#e94f3d"},
    {"id": "1", "name": "吹水台", "icon": "◉", "color": "#e94f3d"},
    {"id": "2", "name": "時事台", "icon": "▤", "color": "#4779c7"},
    {"id": "3", "name": "感情台", "icon": "♡", "color": "#d85a85"},
    {"id": "4", "name": "娛樂台", "icon": "♪", "color": "#9663bd"},
    {"id": "5", "name": "科技台", "icon": "⌘", "color": "#438f72"},
    {"id": "6", "name": "飲食台", "icon": "♨", "color": "#d68b31"},
]

THREADS = [
    {"id": 1, "category": "1", "title": "如果突然多咗一日假，你會點安排？", "body": "最近成日覺得時間唔夠用。如果星期一突然變成公眾假期，你會留喺屋企休息，定係即刻出門玩？", "author": "星期一觀察員", "initial": "一", "avatar": "coral", "votes": 1284, "replies": 286, "time": "2 分鐘前", "minutes": 2, "tag": "熱門討論"},
    {"id": 2, "category": "2", "title": "整理咗今朝幾則重要新聞，有冇漏？", "body": "想用幾分鐘跟進一下今日焦點，歡迎補充有來源嘅消息。", "author": "早晨新聞台", "initial": "早", "avatar": "blue", "votes": 846, "replies": 194, "time": "8 分鐘前", "minutes": 8, "tag": "即時"},
    {"id": 3, "category": "6", "title": "放工後一個人食飯，有咩推介？", "body": "港島區優先，預算大概二百蚊內，想食得舒服又唔使等太耐。", "author": "今晚食乜好", "initial": "食", "avatar": "amber", "votes": 539, "replies": 173, "time": "14 分鐘前", "minutes": 14, "tag": "求推薦"},
    {"id": 4, "category": "3", "title": "點樣先算係一段健康嘅關係？", "body": "最近同伴侶傾緊相處界線，想聽下大家覺得舒服嘅相處模式係點。", "author": "慢慢傾", "initial": "慢", "avatar": "pink", "votes": 412, "replies": 98, "time": "22 分鐘前", "minutes": 22, "tag": "傾下計"},
    {"id": 5, "category": "5", "title": "大家最近有冇轉用咩實用 app？", "body": "唔限平台，工作、生活或者純粹好玩都可以。", "author": "工具控", "initial": "工", "avatar": "green", "votes": 366, "replies": 81, "time": "35 分鐘前", "minutes": 35, "tag": "分享"},
    {"id": 6, "category": "4", "title": "今年最值得入場睇嘅演出係邊場？", "body": "想買飛支持現場演出，大家有冇睇過邊場特別值得推薦？", "author": "前排留位", "initial": "前", "avatar": "violet", "votes": 291, "replies": 65, "time": "48 分鐘前", "minutes": 48, "tag": "娛樂"},
    {"id": 7, "category": "1", "title": "最近學識咗一樣咩新技能？", "body": "唔一定要好厲害，學識煮一道菜都算。", "author": "慢慢進步", "initial": "慢", "avatar": "blue", "votes": 187, "replies": 43, "time": "1 小時前", "minutes": 60, "tag": "日常"},
    {"id": 8, "category": "6", "title": "有冇平靚正嘅週末 brunch 推介？", "body": "兩個人，最好可以訂位，九龍新界都可以。", "author": "週末清單", "initial": "週", "avatar": "amber", "votes": 154, "replies": 32, "time": "2 小時前", "minutes": 120, "tag": "飲食"},
]


@app.route("/", methods=["GET", "POST"])
def home():
    if request.method == "POST":
        title = request.form.get("title", "").strip()
        body = request.form.get("body", "").strip()
        category_id = request.form.get("category", "1")
        if not title or not body:
            flash("請填寫主題和內容。", "error")
            return redirect(url_for("home", compose="1"))
        category = next((item for item in CATEGORIES if item["id"] == category_id), None)
        if category is None or category_id == "all":
            category_id = "1"
        THREADS.insert(0, {
            "id": max(thread["id"] for thread in THREADS) + 1,
            "category": category_id,
            "title": title[:120],
            "body": body[:1000],
            "author": "新會員",
            "initial": "新",
            "avatar": "coral",
            "votes": 0,
            "replies": 0,
            "time": "剛剛",
            "minutes": 0,
            "tag": "新主題",
        })
        flash("主題已發佈。", "success")
        return redirect(url_for("home", category=category_id))

    category_id = request.args.get("category", "all")
    if category_id not in {category["id"] for category in CATEGORIES}:
        category_id = "all"
    order = request.args.get("order", "now")
    if order not in {"now", "hot"}:
        order = "now"
    query = request.args.get("q", "").strip()
    threads = [thread for thread in THREADS if category_id == "all" or thread["category"] == category_id]
    if query:
        threads = [thread for thread in threads if query.casefold() in f"{thread['title']} {thread['body']}".casefold()]
    if order == "hot":
        threads.sort(key=lambda thread: thread["votes"] + thread["replies"] * 2, reverse=True)
    else:
        threads.sort(key=lambda thread: thread["minutes"])

    return render_template(
        "index.html",
        categories=CATEGORIES,
        threads=threads,
        category_id=category_id,
        order=order,
        query=query,
        now=datetime.now(),
        open_composer=request.args.get("compose") == "1",
    )


if __name__ == "__main__":
    app.run(debug=os.environ.get("FLASK_DEBUG") == "1")