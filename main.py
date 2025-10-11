import cv2
from PIL import Image
from telegram import Update, ReplyKeyboardMarkup
from telegram.ext import ApplicationBuilder, CommandHandler, MessageHandler, ContextTypes, filters
import os
import random

TOKEN = " "

balances = {}

SECRET_LINK = "https://youtu.be/xvFZjo5PgG0?si=P5GWnsTtTKoml0SF"


async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    keyboard = [["тап тап тап", "хто ти такий"],
                ["Відкрити коробку...", "Надішли мені котика НЕГАЙНО!!!!!!!"],
                ["Відправити свого монстрика 👹📸", "депнути в казік 🎰"]]
    reply_markup = ReplyKeyboardMarkup(keyboard, resize_keyboard=True)
    await update.message.reply_text(
        f"Welcome, honoroued guest... {update.effective_user.first_name}..."
        f" I cant do anything useful, atleast i can give you coins, or i can make your cat shiny with glasses!!!"
        f"Press 'Send your cat', To send your photo of your cat lol. да вот ткий я кЛутий виз инглеш",
        reply_markup=reply_markup
    )

async def handle_text(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user_id = update.effective_user.id
    text = update.message.text.lower()

    if text == "хто ти такий":
        await update.message.reply_text(
            "Я той, хто постійно сидить над тобою ;) Тицяй тап тап тап)"
        )

    elif text == "тап тап тап":
        balances[user_id] = balances.get(user_id, 0) + 5
        await update.message.reply_text(
            f"Ти отримав золоті монети! 🤑 Баланс: {balances[user_id]} монет."
        )

    elif text == "відкрити коробку...":
        await update.message.reply_text(
            f"Ось що тобі випало...: {SECRET_LINK}",
            disable_web_page_preview=True
        )

    elif text == "Надішли мені котика НЕГАЙНО!!!!!!!":
        try:
            create_cat_with_glasses("caaat.jpeg")
            with open("cat_with_glasses.png", "rb") as photo:
                await update.message.reply_photo(photo, caption="ОООО ееееее")
        except Exception as e:
            await update.message.reply_text(f"Щось не так...:")

    elif text == "відправити свого монстрика 👹":
        await update.message.reply_text("Відправ мені фото кота, а я налиплю йому круті окуляри (бажано в повний ріст)")

    elif text == "депнути в казік 🎰":
        await casino(update, context)

    else:
        await update.message.reply_text(
            f"{update.effective_user.first_name}! У мене нема такого!"
        )


async def handle_photo(update: Update, context: ContextTypes.DEFAULT_TYPE):
    try:
        photo_file = await update.message.photo[-1].get_file()
        photo_path = f"user_cat_{update.effective_user.id}.jpg"
        await photo_file.download_to_drive(photo_path)

        create_cat_with_glasses(photo_path)

        with open("cat_with_glasses.png", "rb") as photo:
            await update.message.reply_photo(photo, caption="Крутишка тепер")

        os.remove(photo_path)

    except Exception as e:
        await update.message.reply_text(f"Повірив що це кіт, ноу фото фор ю")


def create_cat_with_glasses(image_path):
    glasses_path = 'glasses.png'
    cascade_path = 'haarcascade_frontalcatface_extended.xml'

    cat_face_cascade = cv2.CascadeClassifier(cascade_path)
    img_cv = cv2.imread(image_path)
    cat_faces = cat_face_cascade.detectMultiScale(img_cv)

    if len(cat_faces) == 0:
        raise ValueError("Переробляй!")

    cat = Image.open(image_path).convert("RGBA")
    glasses = Image.open(glasses_path).convert("RGBA")

    for (x, y, w, h) in cat_faces:
        g = glasses.resize((w * 5, h * 3))
        cat.paste(g, (int(x - 110), int(y - 90)), g)

    cat.save("cat_with_glasses.png")


async def casino(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user_id = update.effective_user.id
    balance = balances.get(user_id, 0)

    if balance < 3:
        await update.message.reply_text("Занадто бідний.)")
        return

    await update.message.reply_text("🎰 Кручу верчу...🎰")

    result = random.choice(["win2x", "win1.1x", "lose2x"])

    if result == "win2x":
        balances[user_id] = int(balance * 2)
        await update.message.reply_text(f"Любитель азартних ігор.... На: {balances[user_id]} монет.")
    elif result == "win1.1x":
        balances[user_id] = int(balance * 1.1)
        await update.message.reply_text(f"Більше ніж нічого! {balances[user_id]} монет!")
    else:
        balances[user_id] = max(0, balance / 6)
        await update.message.reply_text("Ти програв!")
        with open("tf2everyonelaugh.mp4", "rb") as gif:
             await update.message.reply_animation(gif, caption="📸")

async def hello(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text(
        f"Хело май френд, {update.effective_user.first_name} 👋"
    )


async def stop(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text(
        "I cant stop\n"
        "Micheal, dont leave me here!"
    )


app = ApplicationBuilder().token(TOKEN).build()

app.add_handler(CommandHandler("start", start))
app.add_handler(CommandHandler("hello", hello))
app.add_handler(CommandHandler("stop", stop))
app.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, handle_text))
app.add_handler(MessageHandler(filters.PHOTO, handle_photo))

print("Бот запущений!")
app.run_polling()
