import os
import threading
import logging
import asyncio
from flask import Flask
from telegram import Update
from telegram.ext import Application, CommandHandler, MessageHandler, ContextTypes, filters

BOT_TOKEN = os.getenv("BOT_TOKEN")
HOST = "0.0.0.0"
PORT = int(os.getenv("PORT", 10000))

app = Flask(__name__)

@app.route("/")
def index():
    return "✅ Marketvio Mini App running!"

def run_flask():
    app.run(host=HOST, port=PORT)

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text("👋 Hello from Marketvio!")

async def echo(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text(update.message.text)

async def run_bot():
    if not BOT_TOKEN:
        print("❌ Missing BOT_TOKEN")
        return

    bot_app = Application.builder().token(BOT_TOKEN).build()
    bot_app.add_handler(CommandHandler("start", start))
    bot_app.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, echo))

    print("✅ Bot running via polling...")
    await bot_app.run_polling()

if __name__ == "__main__":
    threading.Thread(target=run_flask, daemon=True).start()
    asyncio.run(run_bot())
