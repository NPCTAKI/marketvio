import os
import threading
import logging
import asyncio
from flask import Flask
from telegram import Update
from telegram.ext import Application, CommandHandler, MessageHandler, ContextTypes, filters

# ==============================
# 🔧 Configuration
# ==============================
BOT_TOKEN = os.getenv("BOT_TOKEN")
WEBAPP_ORIGIN = os.getenv("WEBAPP_ORIGIN", "https://marketvio.onrender.com")
HOST = "0.0.0.0"
PORT = int(os.getenv("PORT", 10000))

# ==============================
# 🌐 Flask app
# ==============================
app = Flask(__name__)

@app.route("/")
def index():
    return "✅ Marketvio Mini App is running!"

def run_flask():
    app.run(host=HOST, port=PORT)

# ==============================
# 🤖 Telegram Handlers
# ==============================
async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text("👋 Hello! Welcome to Marketvio mini app bot!")

async def help_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text("Available commands:\n/start - Start bot\n/help - Show help")

async def echo(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text(update.message.text)

# ==============================
# 🚀 Telegram Bot Runner
# ==============================
async def run_bot():
    if not BOT_TOKEN:
        print("❌ BOT_TOKEN is missing. Set it in Render environment variables.")
        return

    app_telegram = Application.builder().token(BOT_TOKEN).build()

    app_telegram.add_handler(CommandHandler("start", start))
    app_telegram.add_handler(CommandHandler("help", help_command))
    app_telegram.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, echo))

    print("✅ Telegram bot started successfully.")
    await app_telegram.run_polling()

# ==============================
# 🏁 Entry point
# ==============================
if __name__ == "__main__":
    threading.Thread(target=run_flask, daemon=True).start()

    print("🚀 Flask server running, launching Telegram bot...")
    asyncio.run(run_bot())
