import telebot
import random

TOKEN = "8950980879:AAEGljX35NmNnlgemeQahZhtnb46Pu10a88"

bot = telebot.TeleBot(TOKEN)

games = {}

PERSONAJLAR = [
    "Lionel Messi",
    "Cristiano Ronaldo",
    "Neymar",
    "Kylian Mbappe",
    "MrBeast",
    "Jackie Chan",
    "Spider-Man",
    "Batman",
    "Superman",
    "Harry Potter",
    "Shrek",
    "SpongeBob",
    "Pikachu",
    "Elon Musk",
    "Tom Cruise",
    "Free Fire",
    "PUBG",
    "iPhone",
    "Samsung",
    "Spider-Man"
]


@bot.message_handler(commands=["start"])
def start(message):
    bot.reply_to(
        message,
        "🎮 KIMMAN MEN? BOTIGA XUSH KELIBSIZ!\n\n"
        "Botni guruhga qo‘shing va /oyin buyrug‘ini yuboring."
    )


@bot.message_handler(commands=["oyin"])
def oyin(message):
    chat_id = message.chat.id

    if message.chat.type == "private":
        bot.reply_to(message, "❌ O‘yinni guruhda boshlang.")
        return

    if chat_id in games:
        bot.reply_to(message, "⚠️ Bu guruhda o‘yin allaqachon bor.")
        return

    games[chat_id] = {
        "players": {},
        "started": False
    }

    bot.reply_to(
        message,
        "🎮 KIMMAN MEN?\n\n"
        "O‘yinga qo‘shilish uchun:\n"
        "👉 /qoshilaman\n\n"
        "👥 3–20 kishi o‘ynashi mumkin.\n\n"
        "O‘yinchilar yig‘ilgach:\n"
        "👉 /boshlash"
    )


@bot.message_handler(commands=["qoshilaman"])
def qoshilish(message):
    chat_id = message.chat.id

    if chat_id not in games:
        bot.reply_to(message, "❌ Avval /oyin ni bosing.")
        return

    game = games[chat_id]

    if game["started"]:
        bot.reply_to(message, "❌ O‘yin allaqachon boshlangan.")
        return

    if len(game["players"]) >= 20:
        bot.reply_to(message, "❌ Maksimum 20 kishi.")
        return

    user_id = message.from_user.id
    name = message.from_user.first_name

    if user_id in game["players"]:
        bot.reply_to(message, "😄 Siz allaqachon o‘yindasiz.")
        return

    game["players"][user_id] = {
        "name": name
    }

    bot.reply_to(
        message,
        f"✅ {name} qo‘shildi!\n"
        f"👥 O‘yinchilar: {len(game['players'])}"
    )


@bot.message_handler(commands=["boshlash"])
def boshlash(message):
    chat_id = message.chat.id

    if chat_id not in games:
        bot.reply_to(message, "❌ Avval /oyin ni bosing.")
        return

    game = games[chat_id]
    players = list(game["players"].keys())

    if len(players) < 3:
        bot.reply_to(
            message,
            f"❌ Kamida 3 kishi kerak.\n"
            f"Hozir {len(players)} kishi bor."
        )
        return

    if len(players) > 20:
        bot.reply_to(message, "❌ Maksimum 20 kishi.")
        return

    random.shuffle(players)

    for i, user_id in enumerate(players):
        personaj = PERSONAJLAR[i]

        try:
            bot.send_message(
                user_id,
                "🤫 SIZNING PERSONAJINGIZ:\n\n"
                f"👤 {personaj}\n\n"
                "⚠️ Buni boshqa o‘yinchilarga aytmang!"
            )
        except Exception:
            pass

    game["started"] = True

    bot.send_message(
        chat_id,
        "🔥 O‘YIN BOSHLANDI!\n\n"
        "📩 Har bir o‘yinchiga personaji shaxsiy xabarda yuborildi.\n\n"
        "❓ Navbat bilan savol bering va o‘zingiz kimligingizni toping!"
    )


@bot.message_handler(commands=["tugatish"])
def tugatish(message):
    chat_id = message.chat.id

    if chat_id in games:
        del games[chat_id]
        bot.reply_to(message, "🏁 O‘yin tugatildi!")
    else:
        bot.reply_to(message, "❌ Hozir o‘yin yo‘q.")


print("🤖 BOT ISHLAYAPTI...")

bot.infinity_polling()