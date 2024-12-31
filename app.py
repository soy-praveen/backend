from flask import Flask, request, jsonify
import sqlite3
from flask_cors import CORS
import telegram
from flask import Flask, send_from_directory
import os

app = Flask(__name__, static_folder='static')

@app.route('/')
def index():
    return send_from_directory(app.static_folder, 'index.html')

if __name__ == "__main__":
    app.run(host='0.0.0.0', port=int(os.environ.get("PORT", 5000)))

# Telegram Bot Token
BOT_TOKEN = os.environ.get('TELEGRAM_BOT_TOKEN')

bot = telegram.Bot(BOT_TOKEN)

app = Flask(__name__)
CORS(app)

# SQLite Database Setup
conn = sqlite3.connect('airdrop.db', check_same_thread=False)
cursor = conn.cursor()
cursor.execute('''
    CREATE TABLE IF NOT EXISTS logs (
        id INTEGER PRIMARY KEY,
        user_id TEXT,
        username TEXT,
        email TEXT,
        solana_address TEXT,
        task_id INTEGER,
        completed INTEGER DEFAULT 0,
        ip_address TEXT,
        timestamp DATETIME DEFAULT CURRENT_TIMESTAMP
    )
''')
conn.commit()

# Get User Profile
@app.route('/api/profile', methods=['GET'])
def profile():
    # Simulating Telegram User Info
    user_id = request.headers.get('X-Telegram-User-Id')  # Pass Telegram headers
    username = 'VictoryUser'  # Replace with actual fetch
    profile_pic = 'https://via.placeholder.com/100'
    solana_address = None
    cursor.execute('SELECT solana_address FROM logs WHERE user_id=? AND solana_address IS NOT NULL', (user_id,))
    data = cursor.fetchone()
    if data:
        solana_address = data[0]
    return jsonify({
        'username': username,
        'profilePic': profile_pic,
        'solanaAddress': solana_address
    })

# Check Task
@app.route('/api/check-task/<int:task_id>', methods=['GET'])
def check_task(task_id):
    user_id = request.headers.get('X-Telegram-User-Id')  # Pass Telegram headers
    # Replace with real Telegram Bot API Calls
    if task_id in [1, 2]:  # Simulated Check
        joined = True  # Use actual API check
        if joined:
            cursor.execute('UPDATE logs SET completed=1 WHERE user_id=? AND task_id=?', (user_id, task_id))
            conn.commit()
            return jsonify({'success': True})
    return jsonify({'success': False})

# Share Email
@app.route('/api/share-email', methods=['POST'])
def share_email():
    data = request.json
    email = data['email']
    user_id = request.headers.get('X-Telegram-User-Id')  # Pass Telegram headers
    cursor.execute('INSERT INTO logs (user_id, email, task_id, completed) VALUES (?, ?, 3, 1)', (user_id, email))
    conn.commit()
    return jsonify({'success': True})

# Share Solana Address
@app.route('/api/share-solana', methods=['POST'])
def share_solana():
    data = request.json
    solana = data['solana']
    user_id = request.headers.get('X-Telegram-User-Id')  # Pass Telegram headers
    cursor.execute('INSERT INTO logs (user_id, solana_address, task_id, completed) VALUES (?, ?, 4, 1)', (user_id, solana))
    conn.commit()
    return jsonify({'success': True})

if __name__ == '__main__':
    app.run(debug=True)
