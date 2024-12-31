from telegram import Update, WebAppInfo, KeyboardButton, ReplyKeyboardMarkup
from telegram.ext import Application, CommandHandler, ContextTypes, MessageHandler, filters
import os
import sqlite3
from datetime import datetime

# Configuration
TOKEN = os.environ.get('TELEGRAM_BOT_TOKEN')
WEBAPP_URL = os.environ.get('WEBAPP_URL')  # Your render.com webapp URL

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    # Create keyboard with Web App button
    keyboard = [[KeyboardButton(
        text="Open Airdrop App",
        web_app=WebAppInfo(url=WEBAPP_URL)
    )]]
    reply_markup = ReplyKeyboardMarkup(keyboard, resize_keyboard=True)
    
    # Store user info in database
    user = update.effective_user
    conn = sqlite3.connect('airdrop.db')
    c = conn.cursor()
    
    # Check if user exists
    c.execute('SELECT telegram_id FROM users WHERE telegram_id = ?', (str(user.id),))
    existing_user = c.fetchone()
    
    if not existing_user:
        c.execute('''
            INSERT INTO users (telegram_id, username, profile_pic, created_at)
            VALUES (?, ?, ?, ?)
        ''', (
            str(user.id),
            user.username,
            user.get_profile_photos().photos[0][0].file_id if user.get_profile_photos().photos else None,
            datetime.now()
        ))
        conn.commit()
    
    conn.close()
    
    await update.message.reply_text(
        "Welcome to Victory Airdrop! Click the button below to start:",
        reply_markup=reply_markup
    )

async def handle_webapp_data(update: Update, context: ContextTypes.DEFAULT_TYPE):
    # Handle any data sent back from the webapp
    data = update.effective_message.web_app_data.data
    # Process the data as needed
    await update.message.reply_text