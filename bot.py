import logging
import requests
from telegram import Update
from telegram.ext import ApplicationBuilder, ContextTypes, CommandHandler, MessageHandler, filters

# --- SOZLAMALAR ---
# Telegram bot tokeningiz
TELEGRAM_TOKEN = '8086105357:AAG22rrDaVmoqQPeAU0v72EuL5-1QAGZ0wM'

# Google AI Studio'dan olingan API kalit (QO'SHTIRNOQ ICHIDA!)
GEMINI_API_KEY = 'AIzaSyCun9eyTA-Elf4mLQ1Q5R0VaxAsp9d1Uv4'

# Loglarni sozlash
logging.basicConfig(format='%(asctime)s - %(name)s - %(levelname)s - %(message)s', level=logging.INFO)

def get_gemini_response(user_text):
    # Model nomini 'gemini-1.5-flash-latest' ga o'zgartirdik
    url = f"https://generativelanguage.googleapis.com/v1beta/models/gemini-pro:generateContent?key={GEMINI_API_KEY}"

    # ... qolgan qismlar o'zgarmaydi ...
    headers = {'Content-Type': 'application/json'}
    payload = {
        "contents": [{
            "parts": [{"text": user_text}]
        }]
    }

    try:
        response = requests.post(url, json=payload, headers=headers)
        if response.status_code == 200:
            data = response.json()
            # Javobni xavfsiz ajratib olish
            return data['candidates'][0]['content']['parts'][0]['text']
        else:
            return f"Xatolik yuz berdi: {response.status_code}\n{response.text}"
    except Exception as e:
        return f"Ulanishda xato: {str(e)}"

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """/start buyrug'i kelganda ishlaydi"""
    await update.message.reply_text("Salom! Men endi 100% to'g'ri ishlayapman. Savolingizni yuboring!")

async def handle_message(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Xabarlarni qabul qilish va javob qaytarish"""
    user_input = update.message.text

    # Bot "typing..." holatida turishi uchun
    await context.bot.send_chat_action(chat_id=update.effective_chat.id, action="typing")

    # Gemini'dan javobni olish
    answer = get_gemini_response(user_input)

    # Telegramga yuborish
    await update.message.reply_text(answer)

if __name__ == '__main__':
    # Botni ishga tushirish (ApplicationBuilder)
    application = ApplicationBuilder().token(TELEGRAM_TOKEN).build()

    # Handlerlarni qo'shish
    application.add_handler(CommandHandler('start', start))
    application.add_handler(MessageHandler(filters.TEXT & (~filters.COMMAND), handle_message))

    print("Bot muvaffaqiyatli ishga tushdi...")
    application.run_polling()