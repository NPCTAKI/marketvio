import os
import threading
import logging
from flask import Flask
from telegram import Update
from telegram.ext import (
    ApplicationBuilder,
    CommandHandler,
    MessageHandler,
    filters,
    ContextTypes
)

# ==============================
# 🔧 Basic Setup
# ==============================
logging.basicConfig(
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    level=logging.INFO
)
logger = logging.getLogger(__name__)

TOKEN = os.getenv("BOT_TOKEN")  # Set in Render → Environment → BOT_TOKEN

# Flask web server
app = Flask(__name__)

@app.route('/')
def home():
    return "Bot is running!"

def run_flask():
    app.run(host="0.0.0.0", port=8080)

# ==============================
# 🤖 Telegram Bot Handlers
# ==============================
async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text("Hello 👋! I'm your UC service bot.")

async def help_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text("Available commands:\n/start - start the bot\n/help - show this message")

async def echo(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text(f"You said: {update.message.text}")

# ==============================
# 🚀 Main Runner
# ==============================
async def main():
    if not TOKEN:
        logger.error("❌ BOT_TOKEN environment variable is missing.")
        return

    logger.info("Initializing bot...")
    application = ApplicationBuilder().token(TOKEN).build()

    # Handlers
    application.add_handler(CommandHandler("start", start))
    application.add_handler(CommandHandler("help", help_command))
    application.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, echo))

    # Run Flask in background thread
    logger.info("Starting Flask + Telegram bot...")
    t = threading.Thread(target=run_flask, daemon=True)
    t.start()


