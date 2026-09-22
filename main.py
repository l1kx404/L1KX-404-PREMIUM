import os
from telegram import Update
from telegram.ext import Application, CommandHandler, ContextTypes

TOKEN = os.getenv("BOT_TOKEN")

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text("🔥 L1KX 404 BOT SULTAN ON! Siap cuan TRX premium ko! 💰\nKetik /trx buat cek harga TRX")

async def trx(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text("💎 TRX Sultan: $0.32 -> Sinyal BUY! Target +15%")

app = Application.builder().token(TOKEN).build()
app.add_handler(CommandHandler("start", start))
app.add_handler(CommandHandler("trx", trx))
app.run_polling()
