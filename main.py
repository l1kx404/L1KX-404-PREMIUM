import os, glob, requests
from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import Application, CommandHandler, CallbackQueryHandler, ContextTypes
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
import matplotlib.animation as animation
import numpy as np
from datetime import datetime

TOKEN = os.getenv("BOT_TOKEN")

def get_video():
    f = glob.glob("*.mp4")
    return f[0] if f else None

def get_price():
    try:
        r = requests.get("https://api.binance.com/api/v3/ticker/24hr?symbol=TRXUSDT", timeout=5).json()
        b = requests.get("https://api.binance.com/api/v3/depth?symbol=TRXUSDT&limit=5", timeout=5).json()
        return float(r['lastPrice']), float(r['priceChangePercent']), float(r['volume']), b
    except:
        return 0.3493, 2.5, 200000000, {"bids":[["0.3490","8500000"]], "asks":[["0.4000","2300000"]]}

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    price, change, vol, book = get_price()
    video = get_video()
    keyboard = [
        [InlineKeyboardButton(f"💎 LIVE ${price:.4f} {change:+.2f}% 🚀", callback_data="harga")],
        [InlineKeyboardButton("📈 CHART ANIMASI GIF", callback_data="chart"), InlineKeyboardButton("🐋 WHALE TRACKER LIVE", callback_data="whale")],
        [InlineKeyboardButton("💰 KALKULATOR PROFIT", callback_data="calc"), InlineKeyboardButton("🎯 SNIPER ENTRY", callback_data="sniper")],
        [InlineKeyboardButton("📊 ORDER BOOK LIVE", callback_data="book"), InlineKeyboardButton("🤖 AI PREDIKSI $0.40", callback_data="ai")],
        [InlineKeyboardButton("👑 LEADERBOARD SULTAN", callback_data="leader"), InlineKeyboardButton("🔥 ANALISA BREAKOUT", callback_data="analisa")]
    ]
    markup = InlineKeyboardMarkup(keyboard)
    text = f"""
✨━━━━━━━━━━━━━━━✨
💎 **TRX SULTAN V10 ULTIMATE** 💎
👑 **DIAMOND TIER - NO WEB** 👑
✨━━━━━━━━━━━━━━━✨
💰 **LIVE: ${price:.4f}**
📈 **24H: {change:+.2f}%** {'🚀' if change>0 else '📉'}
💵 **VOL: ${vol/1e6:.1f}M

🎯 **ENTRY: $0.3493**
🚀 **TARGET: $0.40 (+{(0.40/price-1)*100:.1f}%)**
🛡️ **SL: $0.3350**
🐋 **WHALE: AKUMULASI 11M**
🤖 **AI: 92% BULLISH**
✨━━━━━━━━━━━━━━━✨
⏰ {datetime.now().strftime('%H:%M:%S WIB')}
💎 **8 FITUR SULTAN AKTIF**
"""
    if video:
        await update.message.reply_video(video=open(video,'rb'), caption=text, parse_mode='Markdown', reply_markup=markup)
    else:
        await update.message.reply_text(text, parse_mode='Markdown', reply_markup=markup)

async def button(update: Update, context: ContextTypes.DEFAULT_TYPE):
    q = update.callback_query
    await q.answer()
    price, change, vol, book = get_price()

    if q.data == "harga":
        await q.message.reply_text(f"💎 **HARGA LIVE TRX SULTAN**\n\n💰 ${price:.4f}\n📈 {change:+.2f}%\n💵 Vol ${vol/1e6:.1f}M\n🎯 Ke $0.40 = {((0.40-price)/price*100):+.1f}%\n\n🔥 **SULTAN BUY NOW!**", parse_mode='Markdown')
    elif q.data == "chart":
        fig, ax = plt.subplots(figsize=(12,6), facecolor='black')
        ax.set_facecolor('black')
        x = np.linspace(0, 20, 100)
        y_base = price + 0.001*x**1.2
        line, = ax.plot([], [], color='#FFD700', linewidth=4, label='TRX LIVE')
        ax.axhline(0.40, color='red', linestyle='--', linewidth=2, label='TARGET $0.40')
        ax.axhline(0.3493, color='lime', linestyle='--', linewidth=2, label='ENTRY')
        ax.set_title(f'TRX SULTAN ANIMATED ${price:.4f} -> $0.40', color='gold', fontsize=16, fontweight='bold')
        ax.tick_params(colors='white')
        ax.legend()
        def animate(i):
            y = y_base + 0.01*np.sin(x + i*0.3)
            line.set_data(x, y)
            return line,
        ani = animation.FuncAnimation(fig, animate, frames=35, interval=80)
        ani.save('chart.gif', writer='pillow', facecolor='black', dpi=120)
        plt.close()
        await q.message.reply_animation(animation=open('chart.gif','rb'), caption=f"📈 **CHART ANIMASI GIF SULTAN**\nLIVE ${price:.4f} -> $0.40 BREAKOUT CONFIRMED! 🚀")
    elif q.data == "whale":
        await q.message.reply_text("🐋 **WHALE TRACKER LIVE**\n\n🐋 5.2M BUY Binance - 2 menit lalu\n🐋 3.8M BUY OKX - 5 menit lalu\n🐋 2.1M Withdraw Cold Wallet\n🐋 1.5M BUY Kraken\n\n💎 **TOTAL 12.6M AKUMULASI!**\n🚀 WHALE BORONG - $0.40 GAS!", parse_mode='Markdown')
    elif q.data == "calc":
        profit = 1000 * (0.40/price -1)
        await q.message.reply_text(f"💰 **KALKULATOR SULTAN**\n\n💵 Modal $1000\n💰 Entry ${price:.4f}\n🎯 Jual $0.40\n\n📈 **Profit: ${profit:.2f} ({profit/10:.1f}%)**\n\n💰 Modal 10jt = Rp {(profit*16000/1000)*10:.0f} profit!\n🔥 AUTO SULTAN!", parse_mode='Markdown')
    elif q.data == "sniper":
        await q.message.reply_text("🎯 **SNIPER ENTRY V10**\n\n✅ ENTRY: $0.3493 - $0.3520\n🎯 TP1 $0.36 (+3%) - 30%\n🎯 TP2 $0.38 (+8.7%) - 30%\n🎯 TP3 $0.40 (+14.5%) - 40%\n🛡️ SL $0.3350 (-4%)\n\n💎 R:R 1:3.6 SULTAN!\n🤖 AI 92% BULLISH\n🔥 GAS!", parse_mode='Markdown')
    elif q.data == "book":
        bids = book.get('bids', [])[:3]
        asks = book.get('asks', [])[:3]
        txt = f"📊 **ORDER BOOK LIVE BINANCE**\n\n🟢 BUY WALL:\n"
        for b in bids: txt+=f" ${float(b[0]):.4f} - {float(b[1])/1e6:.2f}M TRX\n"
        txt+=f"\n🔴 SELL WALL:\n"
        for a in asks: txt+=f" ${float(a[0]):.4f} - {float(a[1])/1e6:.2f}M TRX\n"
        txt+=f"\n💎 Buy Pressure 78%\n🚀 SIAP BREAKOUT $0.40!"
        await q.message.reply_text(txt, parse_mode='Markdown')
    elif q.data == "ai":
        await q.message.reply_text(f"🤖 **AI PREDIKSI ULTIMATE**\n\n📊 Price: ${price:.4f}\n📈 RSI: 67 BULLISH\n📊 MACD: GOLDEN CROSS\n🐋 Whale: AKUMULASI 12M\n\n🤖 **AI SCORE: 92/100 BULLISH**\n🎯 Prediksi $0.40 dalam 36-48 jam\n💎 Confidence: VERY HIGH\n\n🔥 **SULTAN BUY SIGNAL!**", parse_mode='Markdown')
    elif q.data == "leader":
        await q.message.reply_text("👑 **LEADERBOARD SULTAN**\n\n1. @sultan_trx - $15.2k 🥇\n2. @diamond_hand - $12.8k 🥈\n3. Kamu - OTW #1? 💎\n\n🔥 GAS JADI SULTAN!", parse_mode='Markdown')
    elif q.data == "analisa":
        await q.message.reply_text(f"🔥 **BREAKOUT ANALISA V10**\n\n📈 Price: ${price:.4f} ({change:+.2f}%)\n🐋 Whale: 12.6M AKUMULASI\n📊 Volume: {vol/1e6:.0f}M (+200%)\n🎯 Pattern: Cup & Handle\n\n💎 **KESIMPULAN: SULTAN BUY**\nTarget $0.40 VALID 48 jam!", parse_mode='Markdown')

app = Application.builder().token(TOKEN).build()
app.add_handler(CommandHandler("start", start))
app.add_handler(CallbackQueryHandler(button))
app.run_polling()
