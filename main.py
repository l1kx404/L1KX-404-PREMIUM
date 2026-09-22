import os, glob, asyncio, requests
from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import Application, CommandHandler, CallbackQueryHandler, ContextTypes
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
import numpy as np

TOKEN = os.getenv("BOT_TOKEN")
CHAT_ID = "-1001234567890"

def get_video_file():
    files = glob.glob("*.mp4") + glob.glob("*.MP4")
    return files[0] if files else None

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    video = get_video_file()
    keyboard = [
        [InlineKeyboardButton("💎 💰 CEK HARGA TRX", callback_data="harga")],
        [InlineKeyboardButton("📈 CHART + GAMBAR SULTAN", callback_data="chart")],
        [InlineKeyboardButton("🎯 TARGET $0.40", callback_data="target")],
        [InlineKeyboardButton("🔥 ANALISA BREAKOUT", callback_data="analisa")]
    ]
    reply_markup = InlineKeyboardMarkup(keyboard)
    text = """
✨━━━━━━━━━━━━━━━✨
💎 **TRX SULTAN PREMIUM ULTRA** 💎
✨━━━━━━━━━━━━━━━✨
💰 $0.3493 ➔ $0.40 BREAKOUT
🔥 DIAMOND HOLD SULTAN
✨━━━━━━━━━━━━━━━✨
"""
    try:
        if video:
            await update.message.reply_video(video=open(video, 'rb'), caption=text, parse_mode='Markdown', reply_markup=reply_markup)
        else:
            await update.message.reply_text(text, parse_mode='Markdown', reply_markup=reply_markup)
    except Exception as e:
        await update.message.reply_text(text, parse_mode='Markdown', reply_markup=reply_markup)

async def button(update: Update, context: ContextTypes.DEFAULT_TYPE):
    query = update.callback_query
    await query.answer()
    if query.data == "harga":
        r = requests.get("https://api.binance.com/api/v3/ticker/price?symbol=TRXUSDT").json()
        price = r.get('price','0.3493')
        await query.message.reply_text(f"💎 **TRX HARGA SULTAN:** ${price}\n🎯 TARGET: $0.40\n💰 POTENSI: +15%", parse_mode='Markdown')
    elif query.data == "chart":
        x = np.linspace(0, 10, 100)
        y = 0.32 + 0.02*np.sin(x) + 0.01*x
        plt.figure(figsize=(10,5), facecolor='black')
        plt.plot(x, y, color='gold', linewidth=3)
        plt.title('TRX SULTAN CHART TO $0.40', color='gold', fontsize=16)
        plt.gca().set_facecolor('black')
        plt.savefig('chart.png', facecolor='black')
        plt.close()
        await query.message.reply_photo(photo=open('chart.png','rb'), caption="📈 CHART SULTAN TRX $0.3493 -> $0.40 GOLD PREMIUM")
    elif query.data == "target":
        await query.message.reply_text("🎯 **TARGET SULTAN:**\n$0.3493 -> $0.36 -> $0.38 -> $0.40\nSTOP LOSS: $0.33\nHOLD SULTAN!", parse_mode='Markdown')
    elif query.data == "analisa":
        await query.message.reply_text("🔥 **BREAKOUT ANALISA:**\nTRX siap breakout $0.40\nVolume naik 200%\nWhale akumulasi\nSULTAN BUY!", parse_mode='Markdown')

app = Application.builder().token(TOKEN).build()
app.add_handler(CommandHandler("start", start))
app.add_handler(CallbackQueryHandler(button))
app.run_polling()
