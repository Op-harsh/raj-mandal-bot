import random
from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import ApplicationBuilder, CommandHandler, CallbackQueryHandler, ContextTypes

TOKEN = "8706097694:AAFsrvzwTkcJE-"

games = {}

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text("🏏 Cricket Bot Ready!\nType /match")

async def match(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user_id = update.effective_user.id
    games[user_id] = {"score":0, "balls":0, "wickets":0}

    keyboard = [[
        InlineKeyboardButton("Start Game 🎮", callback_data="startgame")
    ]]

    await update.message.reply_text(
        "Click to start match",
        reply_markup=InlineKeyboardMarkup(keyboard)
    )

async def start_game(update: Update, context: ContextTypes.DEFAULT_TYPE):
    query = update.callback_query
    await query.answer()

    await query.edit_message_text(
        "Play your shot:",
        reply_markup=get_buttons()
    )

def get_buttons():
    return InlineKeyboardMarkup([
        [InlineKeyboardButton("1", callback_data="1"),
         InlineKeyboardButton("2", callback_data="2")],
        [InlineKeyboardButton("4", callback_data="4"),
         InlineKeyboardButton("6", callback_data="6")]
    ])

async def game(update: Update, context: ContextTypes.DEFAULT_TYPE):
    query = update.callback_query
    await query.answer()

    user_id = query.from_user.id
    game = games[user_id]

    user = int(query.data)
    bot = random.choice([1,2,3,4,6])

    if user == bot:
        game["wickets"] += 1
        msg = "❌ OUT!"
    else:
        game["score"] += user
        msg = f"✅ {user} runs"

    game["balls"] += 1

    if game["balls"] >= 6:
        final = f"🏁 Match Over\nScore: {game['score']}/{game['wickets']}"
        del games[user_id]
        await query.edit_message_text(final)
        return

    await query.edit_message_text(
        f"{msg}\nScore: {game['score']}/{game['wickets']}\n\nNext ball:",
        reply_markup=get_buttons()
    )

app = ApplicationBuilder().token(TOKEN).build()

app.add_handler(CommandHandler("start", start))
app.add_handler(CommandHandler("match", match))
app.add_handler(CallbackQueryHandler(start_game, pattern="startgame"))
app.add_handler(CallbackQueryHandler(game, pattern="^[1-6]$"))

print("Bot running...")
app.run_polling()
