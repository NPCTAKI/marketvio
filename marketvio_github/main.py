import os
import threading
import logging
import asyncio
from flask import Flask
from telegram import Update
from telegram.ext import (
    ApplicationBuilder,
    CommandHandler,
    MessageHandler,
    ContextTypes,
    filters
)

# ===========================
# 🔧 Basic setup
# ===========================
logging.basicConfig(
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s",
    level=logging.INFO
)
logger = logging.getLogger(__name__)

BOT_TOKEN = os.getenv("BOT_TOKEN")
WEBAPP_ORIGIN = os.getenv("WEBAPP_ORIGIN", "https://marketvio.onrender.com")
HOST = "0.0.0.0"
PORT = int(os.getenv("PORT", 8080))

app = Flask(__name__)

@app.route('/')
def home():
    return "✅ Marketvio Mini App is running!"


# ===========================
# 🤖 Telegram bot handlers
# ===========================
async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text("👋 Hello! Marketvio mini app is active!")

async def help_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text("/start - welcome\n/help - command list")

async def echo(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text(f"You said: {update.message.text}")


# ===========================
# 🚀 Main function
# ===========================
async def run_bot():
    if not BOT_TOKEN:
        logger.error("❌ BOT_TOKEN is missing in environment variables.")
        return

    logger.info("Starting Telegram bot...")
    app_builder = ApplicationBuilder().token(BOT_TOKEN).build()

    app_builder.add_handler(CommandHandler("start", start))
    app_builder.add_handler(CommandHandler("help", help_command))
    app_builder.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, echo))

    await app_builder.run_polling(close_loop=False)


def run_flask():
    app.run(host=HOST, port=PORT)


if __name__ == "__main__":
    # Run Flask in background
    threading.Thread(target=run_flask, daemon=True).start()

    # Run Telegram bot (async)
    asyncio.run(run_bot())
