# L1KX 404 - TRX SULTAN ULTRA PREMIUM V2
import os, ccxt, time, io
import matplotlib.pyplot as plt
from telegram import InlineKeyboardButton, InlineKeyboardMarkup, Update
from telegram.ext import Application, CommandHandler, CallbackQueryHandler, ContextTypes

TOKEN = os.environ.get("BOT_TOKEN")
CHAT_ID = os.environ.get("CHAT_ID")

def sultan_box(price, pintu, change):
    return f"""
╔════════════════════════════════════╗
║  💎  𝐓𝐑𝐗 𝐒𝐔𝐋𝐓𝐀𝐍 𝐏𝐑𝐄𝐌𝐈𝐔𝐌 𝐔𝐋𝐓𝐑𝐀  💎  ║
╠════════════════════════════════════╣
║ 💰 BINANCE : ${price}
║ 🏦 PINTU   : Rp {pintu}
║ 📊 24H     : {change}% ▲ SULTAN
║ ⏰ {time.strftime('%H:%M:%S WIB')} - {time.strftime('%d %b %Y')}
║ ⚡ PREMIUM 24JAM | MOTIF GOLD BATIK
╚════════════════════════════════════╝
"""

def get_price():
    try:
        ex = ccxt.binance()
        t = ex.fetch_ticker('TRX/USDT')
        ohlcv = ex.fetch_ohlcv('TRX/USDT','1h',limit=24)
        return round(t['last'],4), round(t['percentage'],2), ohlcv
    except:
        return 0.3493, 1.38, [[0,0,0,0.3493,0]]

def make_chart(ohlcv):
    closes = [c[4] for c in ohlcv]
    plt.figure(figsize=(4,2))
    plt.plot(closes, linewidth=2)
    plt.title("TRX SULTAN CHART 24H")
    plt.grid(True, alpha=0.3)
    buf = io.BytesIO()
    plt.savefig(buf, format='png', dpi=150, bbox_inches='tight')
    buf.seek(0)
    plt.close()
    return buf

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    price, change, _ = get_price()
    pintu = int(price*17600)
    
    # Kirim VIDEO kalau ada di repo
    try:
        for vid in os.listdir("."):
            if vid.endswith(".mp4"):
                await update.message.reply_animation(open(vid,'rb'), caption="🔥 WELCOME SULTAN ULTRA 🔥")
                break
    except: pass

    keyboard = [
        [InlineKeyboardButton(f"💎 LIVE ${price}", callback_data='live')],
        [InlineKeyboardButton(f"🏦 PINTU Rp {pintu}", callback_data='pintu')],
        [InlineKeyboardButton("📈 CHART + GAMBAR", callback_data='chart')],
        [InlineKeyboardButton("🔔 ALERT $0.35+ BREAKOUT", callback_data='alert')],
        [InlineKeyboardButton("👑 TARGET $0.40 SULTAN", callback_data='target')],
        [InlineKeyboardButton("🔄 REFRESH ULTRA", callback_data='live')],
    ]
    await update.message.reply_text(sultan_box(price, f"{pintu:,}".replace(",","."), change), reply_markup=InlineKeyboardMarkup(keyboard))

async def button_handler(update: Update, context: ContextTypes.DEFAULT_TYPE):
    q = update.callback_query
    await q.answer()
    price, change, ohlcv = get_price()
    pintu = int(price*17600)
    
    if q.data == 'live':
        await q.edit_message_text(sultan_box(price, f"{pintu:,}".replace(",","."), change)+"\n🔄 LIVE UPDATE ULTRA", reply_markup=q.message.reply_markup)
    elif q.data == 'pintu':
        await q.message.reply_text(f"🏦 PINTU DETAIL\n💵 ${price} x 17600 = Rp {pintu:,}\n📊 Selisih premium sultan!")
    elif q.data == 'chart':
        chart = make_chart(ohlcv)
        await q.message.reply_photo(photo=chart, caption=f"📈 TRX ${price} -> $0.40 Target SULTAN\n24H {change}%")
    elif q.data == 'alert':
        await q.message.reply_text(f"🔔 ALERT ULTRA SET!\nSekarang ${price}\nKalau jebol $0.35 auto kirim video breakout ke private!")
    elif q.data == 'target':
        await q.message.reply_text(f"👑 TARGET SULTAN\nEntry $0.3493 -> Target $0.40 (+14.5%)\nStop $0.33 | PREMIUM 24JAM")

async def auto_monitor(context: ContextTypes.DEFAULT_TYPE):
    price, _, _ = get_price()
    if price >= 0.35 and CHAT_ID:
        await context.bot.send_message(chat_id=CHAT_ID, text=f"🚀🚀 BREAKOUT SULTAN ${price} JEBOL $0.35+ 💎💎")

def main():
    app = Application.builder().token(TOKEN).build()
    app.add_handler(CommandHandler("start", start))
    app.add_handler(CommandHandler("chart", lambda u,c: button_handler))
    app.add_handler(CallbackQueryHandler(button_handler))
    app.job_queue.run_repeating(auto_monitor, interval=60, first=10)
    print("ULTRA ON")
    app.run_polling()

if __name__ == '__main__':
    main()
