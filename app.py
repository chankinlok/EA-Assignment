from flask import Flask, render_template, request, redirect, url_for, flash, session
from datetime import datetime

app = Flask(__name__)
app.secret_key = 'your_secret_key_here'

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

threads_db = [
    {
        'id': 101,
        'category_id': '1',
        'category_name': '吹水台',
        'title': '【一人一個】諗返起都覺得尷尬嘅中學經歷 🤡',
        'author': '連豬工程師',
        'created_at': '2026-11-01 12:00',
        'upvotes': 842,
        'downvotes': 18,
        'replies': [
            {'floor': 1, 'author': '連豬工程師', 'content': '我先：中三個陣喺全校早會代表班別講嘢，把聲突然變聲高咗八度...', 'created_at': '2026-11-01 12:00'},
            {'floor': 2, 'author': '九龍城劉德華', 'content': '告白信塞錯咗入班主任個文具盒...', 'created_at': '2026-11-01 12:15'}
        ]
    },
    {
        'id': 102,
        'category_id': '4',
        'category_name': '科技台',
        'title': '[開箱/評測] 最新晶片筆電實測！剪4K影片完全唔熱？',
        'author': 'CodeMaster_HK',
        'created_at': '2026-11-01 10:30',
        'upvotes': 520,
        'downvotes': 34,
        'replies': [
            {'floor': 1, 'author': 'CodeMaster_HK', 'content': '剛剛入手最新一代筆電...', 'created_at': '2026-11-01 10:30'}
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
        new_id = len(threads_db) + 101
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
    app.run(debug=True, port=5000)