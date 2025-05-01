from flask import Flask, request, redirect, render_template
import sqlite3, string, random

app = Flask(__name__)
DB = 'urls.db'

# 🔧 Ensure DB is initialized every time the app starts
def init_db():
    with sqlite3.connect(DB) as conn:
        conn.execute('CREATE TABLE IF NOT EXISTS urls (short TEXT PRIMARY KEY, long TEXT)')

init_db()  # ✅ This now runs even on Render (outside __main__)

def generate_code(length=6):
    return ''.join(random.choices(string.ascii_letters + string.digits, k=length))

@app.route('/', methods=['GET', 'POST'])
def index():
    short_code = None
    if request.method == 'POST':
        long_url = request.form['url']
        short_code = generate_code()
        with sqlite3.connect(DB) as conn:
            conn.execute('INSERT INTO urls (short, long) VALUES (?, ?)', (short_code, long_url))
    return render_template('index.html', short_code=short_code)

@app.route('/<short>')
def redirect_url(short):
    with sqlite3.connect(DB) as conn:
        result = conn.execute('SELECT long FROM urls WHERE short = ?', (short,)).fetchone()
    if result:
        return redirect(result[0])
    return "URL not found", 404
