import os
from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import ApplicationBuilder, CommandHandler, CallbackQueryHandler, ContextTypes, MessageHandler, filters

BOT_TOKEN = os.getenv('BOT_TOKEN')
SYRIATEL_NUMBER = os.getenv('SYRIATEL_NUMBER')
API_PAYMENT_URL = os.getenv('API_PAYMENT_URL')  # إن وجد

users_data = {}

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    keyboard = [
        [InlineKeyboardButton("الألعاب", callback_data='games')],
        [InlineKeyboardButton("رصيد المستخدم", callback_data='balance')],
        [InlineKeyboardButton("شحن الرصيد", callback_data='recharge')],
        [InlineKeyboardButton("الدعم", callback_data='support')],
        [InlineKeyboardButton("أرباحي", callback_data='profits')],
    ]
    reply_markup = InlineKeyboardMarkup(keyboard)
    await update.message.reply_text("مرحباً بك في بوت LiraVerse! اختر من القائمة:", reply_markup=reply_markup)

async def button_handler(update: Update, context: ContextTypes.DEFAULT_TYPE):
    query = update.callback_query
    await query.answer()

    if query.data == 'games':
        games_keyboard = [
            [InlineKeyboardButton("ببجي", callback_data='game_pubg')],
            [InlineKeyboardButton("فري فاير", callback_data='game_ff')],
            [InlineKeyboardButton("كول أوف ديوتي", callback_data='game_cod')],
            [InlineKeyboardButton("ديانا فورس", callback_data='game_diana')],
            [InlineKeyboardButton("كلاش أوف كلانس", callback_data='game_coc')],
            [InlineKeyboardButton("رجوع", callback_data='back')],
        ]
        await query.edit_message_text("اختر اللعبة:", reply_markup=InlineKeyboardMarkup(games_keyboard))

    elif query.data == 'balance':
        user_id = query.from_user.id
        balance = users_data.get(user_id, {}).get('balance', 0)
        await query.edit_message_text(f"رصيدك الحالي: {balance} ل.س\nيمكنك شحن رصيدك من خلال زر 'شحن الرصيد'.")

    elif query.data == 'recharge':
        await query.edit_message_text(
            f"لشحن رصيدك، يرجى تحويل المبلغ على رقم Syriatel: {SYRIATEL_NUMBER}\n"
            "بعد التحويل، أرسل صورة الإيصال ليتم التحقق."
        )

    elif query.data == 'support':
        await query.edit_message_text(
            "للدعم الفني يرجى التواصل مع @Daniel2592006\n"
            "نحن هنا لمساعدتك في أي مشكلة."
        )

    elif query.data == 'profits':
        user_id = query.from_user.id
        profit = users_data.get(user_id, {}).get('profit', 0)
        await query.edit_message_text(f"أرباحك من الإحالات: {profit} ل.س")

    elif query.data == 'back':
        await start(update, context)

async def handle_messages(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user_id = update.message.from_user.id
    text = update.message.text

    if "إيصال" in text or "صورة" in text:
        await update.message.reply_text("تم استلام الإيصال وسيتم التحقق منه خلال دقائق.")

async def main():
    app = ApplicationBuilder().token(BOT_TOKEN).build()

    app.add_handler(CommandHandler("start", start))
    app.add_handler(CallbackQueryHandler(button_handler))
    app.add_handler(MessageHandler(filters.TEXT & (~filters.COMMAND), handle_messages))

    await app.run_polling()

if __name__ == '__main__':
    import asyncio
    asyncio.run(main())