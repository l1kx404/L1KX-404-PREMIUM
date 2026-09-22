# TRX SULTAN PREMIUM - RAILWAY FULL
import os, ccxt, time
from telegram import InlineKeyboardButton, InlineKeyboardMarkup, Update
from telegram.ext import Application, CommandHandler, CallbackQueryHandler, ContextTypes

TOKEN = os.environ.get("BOT_TOKEN")
CHAT_ID = os.environ.get("CHAT_ID")

def sultan_header():
    return "╔════════════════════════════╗\n║  💎 𝐓𝐑𝐗 𝐒𝐔𝐋𝐓𝐀𝐍 𝐏𝐑𝐄𝐌𝐈𝐔𝐌  ║\n╚════════════════════════════╝"

def format_premium(price, pintu, change):
    return f"{sultan_header()}\n💰 BINANCE: ${price}\n🏦 PINTU: Rp {pintu}\n📊 24H: {change}% ▲\n⏰ {time.strftime('%H:%M:%S WIB')}\n⚡ PREMIUM ACTIVE 24JAM"

def get_price():
    try:
        ex = ccxt.binance()
        t = ex.fetch_ticker('TRX/USDT')
        return round(t['last'],4), round(t['percentage'],2)
    except:
        return 0.3493, 1.38

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    price, change = get_price()
    keyboard = [
        [InlineKeyboardButton("💎 LIVE $0.3493", callback_data='live')],
        [InlineKeyboardButton("🏦 PINTU Rp 6.159", callback_data='pintu')],
        [InlineKeyboardButton("📈 CHART SULTAN", callback_data='chart')],
        [InlineKeyboardButton("🔔 ALERT $0.35+", callback_data='alert')],
    ]
    await update.message.reply_text(format_premium(price, "6.159", change), reply_markup=InlineKeyboardMarkup(keyboard))

async def button_handler(update: Update, context: ContextTypes.DEFAULT_TYPE):
    q = update.callback_query
    await q.answer()
    price, change = get_price()
    if q.data == 'live':
        await q.edit_message_text(format_premium(price, "6.159", change)+"\n🔄 LIVE NOW", reply_markup=q.message.reply_markup)
    elif q.data == 'pintu':
        await q.message.reply_text(f"🏦 PINTU: Rp {price*17600:.0f}\nBinance ${price}")
    elif q.data == 'chart':
        await q.message.reply_text(f"📈 TRX ${price} -> Target $0.40 SULTAN!")
    elif q.data == 'alert':
        await q.message.reply_text(f"🔔 ALERT SET $0.35+\nSekarang ${price}")

async def auto_monitor(context: ContextTypes.DEFAULT_TYPE):
    price, _ = get_price()
    if price >= 0.35 and CHAT_ID:
        await context.bot.send_message(chat_id=CHAT_ID, text=f"🚀 BREAKOUT ${price} - $0.35+ JEBOL! 💎")

def main():
    app = Application.builder().token(TOKEN).build()
    app.add_handler(CommandHandler("start", start))
    app.add_handler(CallbackQueryHandler(button_handler))
    app.job_queue.run_repeating(auto_monitor, interval=60, first=10)
    print("💎 SULTAN PREMIUM ON")
    app.run_polling()

if __name__ == '__main__':
    main()
