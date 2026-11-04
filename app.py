from flask import Flask, render_template, request, redirect, url_for, flash, session
from datetime import datetime

app = Flask(__name__)
app.secret_key = 'your_secret_key_here'

# 7 個討論區分台選單
CATEGORIES = [
    {'id': 'all', 'name': '所有主題', 'icon': '🏠'},
    {'id': '1', 'name': '吹水台', 'icon': '💬'},
    {'id': '2', 'name': '時事台', 'icon': '📰'},
    {'id': '3', 'name': '財經台', 'icon': '📈'},
    {'id': '4', 'name': '科技台', 'icon': '💻'},
    {'id': '5', 'name': '娛樂台', 'icon': '🎬'},
    {'id': '6', 'name': '體育台', 'icon': '⚽'},
    {'id': '7', 'name': '遊戲台', 'icon': '🎮'}
]

# 7 個分台，各 5 個發帖討論 (共 35 篇主題)
threads_db = [
    # --- 1. 吹水台 (5 帖) ---
    {
        'id': 101, 'category_id': '1', 'category_name': '吹水台',
        'title': '【一人一個】諗返起都覺得尷尬嘅中學經歷 🤡', 'author': '連豬工程師',
        'created_at': '2026-11-01 12:00', 'upvotes': 842, 'downvotes': 18,
        'replies': [
            {'floor': 1, 'author': '連豬工程師', 'content': '我先：中三個陣喺全校早會代表班別講嘢，把聲突然變聲高咗八度...', 'created_at': '2026-11-01 12:00'},
            {'floor': 2, 'author': '九龍城劉德華', 'content': '告白信塞錯咗入班主任個文具盒...', 'created_at': '2026-11-01 12:15'}
        ]
    },
    {
        'id': 102, 'category_id': '1', 'category_name': '吹水台',
        'title': '邊樣香港小食先係街頭小食之王？🍢', 'author': '掃街大師',
        'created_at': '2026-11-01 13:20', 'upvotes': 430, 'downvotes': 25,
        'replies': [
            {'floor': 1, 'author': '掃街大師', 'content': '魚蛋、燒賣、雞蛋仔、腸粉，大家覺得邊樣最不可或缺？', 'created_at': '2026-11-01 13:20'},
            {'floor': 2, 'author': '辣醬控', 'content': '一定要係咖喱魚蛋！多辣多汁！', 'created_at': '2026-11-01 13:40'}
        ]
    },
    {
        'id': 103, 'category_id': '1', 'category_name': '吹水台',
        'title': '究竟打工仔放工之後仲有冇個人生活？😴', 'author': '社畜日常',
        'created_at': '2026-11-01 18:00', 'upvotes': 650, 'downvotes': 12,
        'replies': [
            {'floor': 1, 'author': '社畜日常', 'content': '每日返工連車程要11個鐘，返到屋企洗完澡就想睡覺，好灰。', 'created_at': '2026-11-01 18:00'}
        ]
    },
    {
        'id': 104, 'category_id': '1', 'category_name': '吹水台',
        'title': '大家覺得幾多歲結婚先叫最合適？💒', 'author': '緣份天注定',
        'created_at': '2026-11-01 19:30', 'upvotes': 290, 'downvotes': 40,
        'replies': [
            {'floor': 1, 'author': '緣份天注定', 'content': '身邊朋友一個個結婚，自己仲係單身，開始有啲壓力。', 'created_at': '2026-11-01 19:30'}
        ]
    },
    {
        'id': 105, 'category_id': '1', 'category_name': '吹水台',
        'title': '【深夜食堂】大家今晚宵夜食咩？🍜', 'author': '夜貓子',
        'created_at': '2026-11-01 23:45', 'upvotes': 510, 'downvotes': 8,
        'replies': [
            {'floor': 1, 'author': '夜貓子', 'content': '煮咗包出前一丁加隻煎蛋，正！', 'created_at': '2026-11-01 23:45'}
        ]
    },

    # --- 2. 時事台 (5 帖) ---
    {
        'id': 201, 'category_id': '2', 'category_name': '時事台',
        'title': '天文台預測下週將受強烈季候風影響顯著降溫 🥶', 'author': '天氣特警',
        'created_at': '2026-11-01 08:30', 'upvotes': 610, 'downvotes': 15,
        'replies': [
            {'floor': 1, 'author': '天氣特警', 'content': '氣溫將顯著下降至14度左右，新界再低兩三分，記得拿外套！', 'created_at': '2026-11-01 08:30'}
        ]
    },
    {
        'id': 202, 'category_id': '2', 'category_name': '時事台',
        'title': '新一代公共交通津貼調整細節公佈 🚌', 'author': '出行觀察員',
        'created_at': '2026-11-01 09:15', 'upvotes': 320, 'downvotes': 45,
        'replies': [
            {'floor': 1, 'author': '出行觀察員', 'content': '大家覺得新政策對每日長途跨區返工嘅打工仔幫助大唔大？', 'created_at': '2026-11-01 09:15'}
        ]
    },
    {
        'id': 203, 'category_id': '2', 'category_name': '時事台',
        'title': '國際油價回落，本港油價會唔會跟隨下調？⛽', 'author': '汽車愛好者',
        'created_at': '2026-11-01 11:00', 'upvotes': 480, 'downvotes': 10,
        'replies': [
            {'floor': 1, 'author': '汽車愛好者', 'content': '加快減慢行內常態，期待今次會回落。', 'created_at': '2026-11-01 11:00'}
        ]
    },
    {
        'id': 204, 'category_id': '2', 'category_name': '時事台',
        'title': '討論：近年環保餐具政策對市民生活的影響 🌿', 'author': '綠色生活',
        'created_at': '2026-11-01 14:20', 'upvotes': 920, 'downvotes': 110,
        'replies': [
            {'floor': 1, 'author': '綠色生活', 'content': '紙飲管跟木匙羮大家習慣咗未？', 'created_at': '2026-11-01 14:20'}
        ]
    },
    {
        'id': 205, 'category_id': '2', 'category_name': '時事台',
        'title': '全港多區推行夜市經濟活動，大家去咗未？🌃', 'author': '夜經濟關注組',
        'created_at': '2026-11-01 17:40', 'upvotes': 210, 'downvotes': 60,
        'replies': [
            {'floor': 1, 'author': '夜經濟關注組', 'content': '現場人流幾多，小食攤位幾熱鬧！', 'created_at': '2026-11-01 17:40'}
        ]
    },

    # --- 3. 財經台 (5 帖) ---
    {
        'id': 301, 'category_id': '3', 'category_name': '財經台',
        'title': '美股夜盤又破頂！到底有乜力量撐住個市？💰', 'author': '股神巴菲特子',
        'created_at': '2026-11-01 07:45', 'upvotes': 1240, 'downvotes': 89,
        'replies': [
            {'floor': 1, 'author': '股神巴菲特子', 'content': '科技股繼續狂拉，AI 熱潮完全冇退燒迹象！大家手頭上幾多成倉？', 'created_at': '2026-11-01 07:45'}
        ]
    },
    {
        'id': 302, 'category_id': '3', 'category_name': '財經台',
        'title': '定期存款利率微跌，仲有邊間銀行高息？🏦', 'author': '理財小達人',
        'created_at': '2026-11-01 10:15', 'upvotes': 350, 'downvotes': 12,
        'replies': [
            {'floor': 1, 'author': '理財小達人', 'content': '求推薦做3個月定存高息銀行！', 'created_at': '2026-11-01 10:15'}
        ]
    },
    {
        'id': 303, 'category_id': '3', 'category_name': '財經台',
        'title': '樓市成交量回升，買家入市態度轉趨積極？🏠', 'author': '地產分析師',
        'created_at': '2026-11-01 12:50', 'upvotes': 410, 'downvotes': 95,
        'replies': [
            {'floor': 1, 'author': '地產分析師', 'content': '一手新盤開價貼近二手，吸引唔少首置客觀望。', 'created_at': '2026-11-01 12:50'}
        ]
    },
    {
        'id': 304, 'category_id': '3', 'category_name': '財經台',
        'title': '加密貨幣比特幣再創新高，突破大關！🚀', 'author': 'CryptoKing',
        'created_at': '2026-11-01 15:30', 'upvotes': 890, 'downvotes': 130,
        'replies': [
            {'floor': 1, 'author': 'CryptoKing', 'content': 'HODL! 信念者終將獲得回報。', 'created_at': '2026-11-01 15:30'}
        ]
    },
    {
        'id': 305, 'category_id': '3', 'category_name': '財經台',
        'title': '黃金避險需求強勁，金價破頂可唔可以繼續追？💰', 'author': '金價追蹤者',
        'created_at': '2026-11-01 18:20', 'upvotes': 520, 'downvotes': 22,
        'replies': [
            {'floor': 1, 'author': '金價追蹤者', 'content': '買金條定係買黃金 ETF 好？大家點睇？', 'created_at': '2026-11-01 18:20'}
        ]
    },

    # --- 4. 科技台 (5 帖) ---
    {
        'id': 401, 'category_id': '4', 'category_name': '科技台',
        'title': '[開箱/評測] 最新晶片筆電實測！剪4K影片完全唔熱？💻', 'author': 'CodeMaster_HK',
        'created_at': '2026-11-01 10:30', 'upvotes': 520, 'downvotes': 34,
        'replies': [
            {'floor': 1, 'author': 'CodeMaster_HK', 'content': '剛剛入手最新一代筆電，實測跑 4K 60fps 影片只需1分40秒！', 'created_at': '2026-11-01 10:30'}
        ]
    },
    {
        'id': 402, 'category_id': '4', 'category_name': '科技台',
        'title': 'AI 生成程式碼已經可以代替初級程式員？🤖', 'author': 'FullStackDev',
        'created_at': '2026-11-01 11:45', 'upvotes': 780, 'downvotes': 50,
        'replies': [
            {'floor': 1, 'author': 'FullStackDev', 'content': '用咗最新 AI 工具，寫邏輯快咗三倍，前端後端通吃。', 'created_at': '2026-11-01 11:45'}
        ]
    },
    {
        'id': 403, 'category_id': '4', 'category_name': '科技台',
        'title': 'iOS / Android 新版系統發佈！邊個功能最實用？📱', 'author': '手機極客',
        'created_at': '2026-11-01 14:10', 'upvotes': 340, 'downvotes': 18,
        'replies': [
            {'floor': 1, 'author': '手機極客', 'content': '私隱控制跟電池續航都有改善！', 'created_at': '2026-11-01 14:10'}
        ]
    },
    {
        'id': 404, 'category_id': '4', 'category_name': '科技台',
        'title': '自組電腦 GPU 顯卡降價，升級現有配備好時機？🖥️', 'author': 'DIY玩家',
        'created_at': '2026-11-01 16:50', 'upvotes': 460, 'downvotes': 12,
        'replies': [
            {'floor': 1, 'author': 'DIY玩家', 'content': '等咗咁耐終於回落到建議售價。', 'created_at': '2026-11-01 16:50'}
        ]
    },
    {
        'id': 405, 'category_id': '4', 'category_name': '科技台',
        'title': '光纖寬頻升級 2.5G / 5G，實際上網爽快幾多？🌐', 'author': '極速網絡',
        'created_at': '2026-11-01 20:15', 'upvotes': 290, 'downvotes': 15,
        'replies': [
            {'floor': 1, 'author': '極速網絡', 'content': '下檔幾十GB大檔幾秒鐘完成，太狂。', 'created_at': '2026-11-01 20:15'}
        ]
    },

    # --- 5. 娛樂台 (5 帖) ---
    {
        'id': 501, 'category_id': '5', 'category_name': '娛樂台',
        'title': '今集熱播台劇大結局真係估佢唔到！彩蛋點睇？🍿', 'author': '追劇達人',
        'created_at': '2026-11-01 09:00', 'upvotes': 430, 'downvotes': 40,
        'replies': [
            {'floor': 1, 'author': '追劇達人', 'content': '劇透注意！男主角竟然係幕後黑手... 會有第二季定點？', 'created_at': '2026-11-01 09:00'}
        ]
    },
    {
        'id': 502, 'category_id': '5', 'category_name': '娛樂台',
        'title': '最新港產電影口碑炸裂！票房打破紀錄？🎬', 'author': '影迷會長',
        'created_at': '2026-11-01 13:10', 'upvotes': 670, 'downvotes': 20,
        'replies': [
            {'floor': 1, 'author': '影迷會長', 'content': '劇本紮實，演員演技大爆發，推薦大家去戲院支持！', 'created_at': '2026-11-01 13:10'}
        ]
    },
    {
        'id': 503, 'category_id': '5', 'category_name': '娛樂台',
        'title': '演唱會門票一開售即秒殺！大家買唔買到？🎟️', 'author': '搶飛大師',
        'created_at': '2026-11-01 15:40', 'upvotes': 810, 'downvotes': 90,
        'replies': [
            {'floor': 1, 'author': '搶飛大師', 'content': '驗證碼一直錯，入到去已經完售... 討厭炒飛！', 'created_at': '2026-11-01 15:40'}
        ]
    },
    {
        'id': 504, 'category_id': '5', 'category_name': '娛樂台',
        'title': '選秀節目新一季開播，邊個參賽者最具冠軍相？🎤', 'author': '星探小組',
        'created_at': '2026-11-01 19:10', 'upvotes': 250, 'downvotes': 35,
        'replies': [
            {'floor': 1, 'author': '星探小組', 'content': '3號參賽者把聲非常有辨識度！', 'created_at': '2026-11-01 19:10'}
        ]
    },
    {
        'id': 505, 'category_id': '5', 'category_name': '娛樂台',
        'title': '韓國新人女團首播 MV 破億播放，影響力驚人！💃', 'author': 'KPOP迷',
        'created_at': '2026-11-01 21:30', 'upvotes': 530, 'downvotes': 45,
        'replies': [
            {'floor': 1, 'author': 'KPOP迷', 'content': '舞蹈跟歌曲洗腦度極高！', 'created_at': '2026-11-01 21:30'}
        ]
    },

    # --- 6. 體育台 (5 帖) ---
    {
        'id': 601, 'category_id': '6', 'category_name': '體育台',
        'title': '英超形勢大亂！今季邊隊最有機會奪冠？⚽', 'author': '阿仙奴球迷',
        'created_at': '2026-11-01 08:00', 'upvotes': 380, 'downvotes': 55,
        'replies': [
            {'floor': 1, 'author': '阿仙奴球迷', 'content': '榜首位置幾次易手！曼城陣容深厚，兵工廠防守穩健！', 'created_at': '2026-11-01 08:00'}
        ]
    },
    {
        'id': 602, 'category_id': '6', 'category_name': '體育台',
        'title': 'NBA 季後賽爭奪戰！湖人能否保住季後賽席位？🏀', 'author': '紫金軍團',
        'created_at': '2026-11-01 11:20', 'upvotes': 620, 'downvotes': 30,
        'replies': [
            {'floor': 1, 'author': '紫金軍團', 'content': '老將依然神勇，但防守效率需要提高。', 'created_at': '2026-11-01 11:20'}
        ]
    },
    {
        'id': 603, 'category_id': '6', 'category_name': '體育台',
        'title': '香港運動員國際賽事再奪金牌！真係香港人驕傲！🥇', 'author': '體育精神',
        'created_at': '2026-11-01 14:50', 'upvotes': 1450, 'downvotes': 10,
        'replies': [
            {'floor': 1, 'author': '體育精神', 'content': '決賽逆轉勝太熱血了！香港隊加油！', 'created_at': '2026-11-01 14:50'}
        ]
    },
    {
        'id': 604, 'category_id': '6', 'category_name': '體育台',
        'title': '歐聯淘汰賽抽籤結果公佈！死亡之組正式誕生！🏆', 'author': '歐聯迷',
        'created_at': '2026-11-01 17:30', 'upvotes': 410, 'downvotes': 18,
        'replies': [
            {'floor': 1, 'author': '歐聯迷', 'content': '幾場強強對決都非常有睇頭！', 'created_at': '2026-11-01 17:30'}
        ]
    },
    {
        'id': 605, 'category_id': '6', 'category_name': '體育台',
        'title': '網球大滿貫決賽打足5盤，經典史詩對決！🎾', 'author': '網球狂熱',
        'created_at': '2026-11-01 22:10', 'upvotes': 330, 'downvotes': 8,
        'replies': [
            {'floor': 1, 'author': '網球狂熱', 'content': '兩邊打咗4個幾鐘，意志力大比拼！', 'created_at': '2026-11-01 22:10'}
        ]
    },

    # --- 7. 遊戲台 (5 帖) ---
    {
        'id': 701, 'category_id': '7', 'category_name': '遊戲台',
        'title': '【GTA 6】最新預告片解析，地圖大到誇張！🎮', 'author': 'GamerX',
        'created_at': '2026-11-01 09:40', 'upvotes': 1980, 'downvotes': 22,
        'replies': [
            {'floor': 1, 'author': 'GamerX', 'content': 'NPC AI 互動性提升300%，大家準備好出機未？', 'created_at': '2026-11-01 09:40'}
        ]
    },
    {
        'id': 702, 'category_id': '7', 'category_name': '遊戲台',
        'title': 'Steam 季度大特賣開啟！有咩必買抵玩推薦？💸', 'author': '折扣獵人',
        'created_at': '2026-11-01 12:30', 'upvotes': 740, 'downvotes': 15,
        'replies': [
            {'floor': 1, 'author': '折扣獵人', 'content': '不少 3A 大作打折高達 70% off，買咗先算！', 'created_at': '2026-11-01 12:30'}
        ]
    },
    {
        'id': 703, 'category_id': '7', 'category_name': '遊戲台',
        'title': '電競世界大賽總決賽今晚開打，邊隊可以奪冠？🏆', 'author': 'EsportsFan',
        'created_at': '2026-11-01 16:00', 'upvotes': 910, 'downvotes': 40,
        'replies': [
            {'floor': 1, 'author': 'EsportsFan', 'content': '加油！期待看到精彩的 5 局大戰！', 'created_at': '2026-11-01 16:00'}
        ]
    },
    {
        'id': 704, 'category_id': '7', 'category_name': '遊戲台',
        'title': 'PS5 / Switch 2 次世代主機消息，傳聞性能大提升？🕹️', 'author': '主機黨',
        'created_at': '2026-11-01 18:40', 'upvotes': 620, 'downvotes': 25,
        'replies': [
            {'floor': 1, 'author': '主機黨', 'content': '希望能達到穩定 4K 60fps！', 'created_at': '2026-11-01 18:40'}
        ]
    },
    {
        'id': 705, 'category_id': '7', 'category_name': '遊戲台',
        'title': '獨立遊戲突然爆紅！單人開發也能做成神作？✨', 'author': 'IndieLove',
        'created_at': '2026-11-01 21:00', 'upvotes': 480, 'downvotes': 10,
        'replies': [
            {'floor': 1, 'author': 'IndieLove', 'content': '玩法極具創意，畫面風格也很獨特！', 'created_at': '2026-11-01 21:00'}
        ]
    }
]

@app.route('/')
def home():
    cat_id = request.args.get('cat', 'all')
    if cat_id != 'all':
        filtered_threads = [t for t in threads_db if t['category_id'] == cat_id]
    else:
        filtered_threads = threads_db

    return render_template('index.html', 
                           categories=CATEGORIES, 
                           threads=filtered_threads, 
                           current_cat=cat_id,
                           user=session.get('user'))

# 處理「發帖」表單提交
@app.route('/create', methods=['POST'])
def create_thread():
    title = request.form.get('title')
    cat_id = request.form.get('category_id')
    body = request.form.get('body')

    cat_obj = next((c for c in CATEGORIES if c['id'] == cat_id), CATEGORIES[1])

    if title and body:
        # 自動取當前最大的 ID 再加 1，確保發帖不重覆 ID
        new_id = max(t['id'] for t in threads_db) + 1 if threads_db else 101
        author = session.get('user', '連豬大師')
        now_str = datetime.now().strftime('%Y-%m-%d %H:%M')
        
        new_thread = {
            'id': new_id,
            'category_id': cat_id,
            'category_name': cat_obj['name'],
            'title': title,
            'author': author,
            'created_at': now_str,
            'upvotes': 1,
            'downvotes': 0,
            'replies': [
                {'floor': 1, 'author': author, 'content': body, 'created_at': now_str}
            ]
        }
        threads_db.insert(0, new_thread)
        return redirect(url_for('thread_detail', thread_id=new_id))

    return redirect(url_for('home'))

@app.route('/thread/<int:thread_id>', methods=['GET', 'POST'])
def thread_detail(thread_id):
    thread = next((t for t in threads_db if t['id'] == thread_id), None)
    if not thread:
        return "Thread not found", 404

    if request.method == 'POST':
        reply_content = request.form.get('reply_content')
        if reply_content:
            author = session.get('user', '連豬大師')
            new_floor = len(thread['replies']) + 1
            thread['replies'].append({
                'floor': new_floor,
                'author': author,
                'content': reply_content,
                'created_at': datetime.now().strftime('%Y-%m-%d %H:%M')
            })
            return redirect(url_for('thread_detail', thread_id=thread_id))

    return render_template('thread_detail.html', 
                           categories=CATEGORIES, 
                           thread=thread,
                           user=session.get('user'))

@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        username = request.form.get('username')
        password = request.form.get('password')
        if username and password:
            session['user'] = username
            return redirect(url_for('home'))
    return render_template('login.html')

@app.route('/logout')
def logout():
    session.pop('user', None)
    return redirect(url_for('home'))

if __name__ == '__main__':
    # 相容 GitHub Codespaces 監聽 port
    app.run(host='0.0.0.0', port=5000, debug=True)