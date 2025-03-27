import asyncio
import json
import logging
import os
from aiogram import Bot, Dispatcher, types, F
from aiogram.filters import Command
from aiogram.types import Message
from config import BOT_TOKEN, ADMIN_IDS, CHANNELS, MOVIE_CHANNEL
from check_subscription import check_subscription
from dotenv import load_dotenv

# Logging sozlamalari
logging.basicConfig(level=logging.INFO)

# Bot va Dispatcher obyektlari
bot = Bot(token=BOT_TOKEN)
dp = Dispatcher()

MOVIE_DB_FILE = "movies.json"
USERS_DB_FILE = "users.json"

# .env faylini yuklash
load_dotenv()

# **Kinolarni faylga saqlash funksiyasi**
def save_movie(movie_code, movie_file_id):
    movies = load_movies()
    movies[movie_code] = movie_file_id
    with open(MOVIE_DB_FILE, "w", encoding="utf-8") as f:
        json.dump(movies, f, ensure_ascii=False, indent=4)

# **Kino yuklab olish funksiyasi**
def load_movies():
    try:
        with open(MOVIE_DB_FILE, "r", encoding="utf-8") as f:
            return json.load(f)
    except (FileNotFoundError, json.JSONDecodeError):
        return {}

# **Kinoni o‘chirish funksiyasi**
def remove_movie(movie_code):
    movies = load_movies()
    if movie_code in movies:
        del movies[movie_code]
        with open(MOVIE_DB_FILE, "w", encoding="utf-8") as f:
            json.dump(movies, f, ensure_ascii=False, indent=4)
        return True
    return False

# **Foydalanuvchilarni saqlash funksiyasi**
def save_user(user_id):
    users = load_users()
    if user_id not in users:
        users.append(user_id)
        with open(USERS_DB_FILE, "w", encoding="utf-8") as f:
            json.dump(users, f, ensure_ascii=False, indent=4)

# **Foydalanuvchilarni yuklash funksiyasi**
def load_users():
    try:
        with open(USERS_DB_FILE, "r", encoding="utf-8") as f:
            return json.load(f)
    except (FileNotFoundError, json.JSONDecodeError):
        return []

# **Admin tekshirish funksiyasi**
def is_admin(user_id):
    return str(user_id) in ADMIN_IDS

# **/start buyrug‘i**
@dp.message(Command("start"))
async def start(message: Message):
    user_id = message.from_user.id

    # Majburiy obunani tekshirish
    if not await check_subscription(user_id):
        buttons = [
            types.InlineKeyboardButton(text="📢 Kanalga a‘zo bo‘lish", url=f"https://t.me/{CHANNELS[0][1:]}")
        ]
        keyboard = types.InlineKeyboardMarkup(inline_keyboard=[buttons])
        await message.answer("🚫 Botdan foydalanish uchun kanalga a'zo bo‘lishingiz kerak!", reply_markup=keyboard)
        return

    save_user(str(user_id))
    await message.answer("👋 Salom! Kino kodini kiriting:")

# **/help buyrug‘i**
@dp.message(Command("help"))
async def help_command(message: Message):
    help_text = """
🆘 **Yordam bo‘limi**:

✅ **/start** - Botni ishga tushirish
🎬 **/addmovie <kod>** - Kino qo‘shish (Admin)
🗑 **/removemovie <kod>** - Kino o‘chirish (Admin)
📊 **/stats** - Statistika
👥 **/members** - Foydalanuvchilar soni (Admin)
🎥 **/kinolar** - Saqlangan kinolar ro‘yxati (Admin)
"""
    await message.answer(help_text, parse_mode="Markdown")

# **Kino qidirish**
@dp.message(F.text.regexp(r"^\d+$"))
async def search_movie(message: Message):
    movie_code = message.text.strip()
    movies = load_movies()
    if movie_code in movies:
        movie_file_id = movies[movie_code]
        await message.answer_video(video=movie_file_id, caption=f"🎬 Marhamat, kinongiz!\n📌 Kod: `{movie_code}`", parse_mode="Markdown")
    else:
        await message.answer("❌ Bunday kino topilmadi.")

# **Kino qo‘shish (faqat admin)**
@dp.message(Command("addmovie"))
async def add_movie(message: Message):
    if not is_admin(message.from_user.id):
        await message.answer("🚫 Sizda kinolarni qo‘shish huquqi yo‘q!")
        return
    if message.reply_to_message and message.reply_to_message.video:
        args = message.text.split(maxsplit=1)
        if len(args) < 2:
            await message.answer("❌ Kino kodini ham yozing: `/addmovie <kino_kodi>`")
            return
        movie_code = args[1]
        movie_file_id = message.reply_to_message.video.file_id
        save_movie(movie_code, movie_file_id)
        await message.answer(f"✅ Kino saqlandi:\n🎬 Kod: `{movie_code}`", parse_mode="Markdown")
    else:
        await message.answer("❌ Noto‘g‘ri format! Reply qilingan videoga `/addmovie <kino_kodi>` deb yozing.")

# **Kino o‘chirish (faqat admin)**
@dp.message(Command("removemovie"))
async def removemovie(message: Message):
    if not is_admin(message.from_user.id):
        await message.answer("🚫 Sizda bu buyruqdan foydalanish huquqi yo‘q!")
        return
    args = message.text.split()
    if len(args) < 2:
        await message.answer("❌ Kino kodini ham yozing: `/removemovie <kino_kodi>`")
        return
    movie_code = args[1]
    if remove_movie(movie_code):
        await message.answer(f"✅ Kino o‘chirildi:\n🎬 Kod: `{movie_code}`", parse_mode="Markdown")
    else:
        await message.answer("❌ Bunday kino topilmadi.")

# **/stats - statistikani chiqarish**
@dp.message(Command("stats"))
async def stats(message: Message):
    movies = load_movies()
    users = load_users()
    movie_count = len(movies)
    user_count = len(users)
    await message.answer(f"📊 Statistika:\n🎥 Kinolar soni: {movie_count}\n👥 Foydalanuvchilar soni: {user_count}")

# **/members - foydalanuvchilar soni (faqat admin)**
@dp.message(Command("members"))
async def members(message: Message):
    if not is_admin(message.from_user.id):
        await message.answer("🚫 Bu buyruq faqat adminlar uchun!")
        return
    users = load_users()
    await message.answer(f"👥 Botdagi foydalanuvchilar soni: {len(users)}")

# **/kinolar - kinolar ro‘yxati (faqat admin)**
@dp.message(Command("kinolar"))
async def kinolar(message: Message):
    if not is_admin(message.from_user.id):
        await message.answer("🚫 Bu buyruq faqat adminlar uchun!")
        return
    movies = load_movies()
    if not movies:
        await message.answer("📭 Hech qanday kino yo‘q!")
        return
    movie_list = "\n".join([f"🎬 {code}" for code in movies.keys()])
    await message.answer(f"🎥 Saqlangan kinolar:\n{movie_list}")

# **Asosiy ishga tushirish funksiyasi**
async def main():
    print("Bot ishga tushdi... 🚀")
    await dp.start_polling(bot)

if __name__ == "__main__":
    asyncio.run(main())
