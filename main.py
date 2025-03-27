import logging
import asyncio
import os
from aiogram import Bot, Dispatcher, types
from aiogram.filters import Command
from aiogram.types import Message
from config import ADMIN_IDS
from dotenv import load_dotenv

load_dotenv()

TOKEN = os.getenv("BOT_TOKEN")
bot = Bot(token=TOKEN)
dp = Dispatcher()

# ADMIN TEKSHIRUV FUNKSIYASI
def is_admin(user_id):
    return int(user_id) in ADMIN_IDS

# /start - Botni ishga tushirish
@dp.message(Command("start"))
async def start(message: Message):
    await message.answer("🎬 Salom! Kino va kanal qo‘shish botiga xush kelibsiz!\n/help - Buyruqlar ro‘yxati.")

# /help - Buyruqlar ro‘yxati
@dp.message(Command("help"))
async def help_command(message: Message):
    help_text = (
        "🆘 Yordam bo‘limi:\n\n"
        "✅ /start - Botni ishga tushirish\n"
        "🎬 /addmovie <kod> - Kino qo‘shish (Admin)\n"
        "🗑 /removemovie <kod> - Kino o‘chirish (Admin)\n"
        "📡 /addchannel <username> - Kanal qo‘shish (Admin)\n"
        "❌ /removechannel <username> - Kanal o‘chirish (Admin)\n"
        "📜 /channels - Saqlangan kanallar ro‘yxati (Admin)\n"
        "📊 /stats - Statistika\n"
        "👥 /members - Foydalanuvchilar soni (Admin)\n"
        "🎥 /kinolar - Saqlangan kinolar ro‘yxati (Admin)\n"
    )
    await message.answer(help_text)

# /addmovie - Kino qo‘shish (Faqat admin uchun)
@dp.message(Command("addmovie"))
async def add_movie(message: Message):
    if not is_admin(message.from_user.id):
        await message.answer("🚫 Sizda bu buyruqdan foydalanish huquqi yo‘q!")
        return

    args = message.text.split(maxsplit=1)
    if len(args) < 2:
        await message.answer("❌ Noto‘g‘ri format! Kino kodini kiriting: `/addmovie <kino_kodi>`")
        return

    movie_code = args[1]
    with open("movies.txt", "a") as file:
        file.write(movie_code + "\n")

    await message.answer(f"✅ Kino qo‘shildi! Kod: `{movie_code}`", parse_mode="Markdown")

# /removemovie - Kino o‘chirish (Faqat admin uchun)
@dp.message(Command("removemovie"))
async def remove_movie(message: Message):
    if not is_admin(message.from_user.id):
        await message.answer("🚫 Sizda bu buyruqdan foydalanish huquqi yo‘q!")
        return

    args = message.text.split(maxsplit=1)
    if len(args) < 2:
        await message.answer("❌ Noto‘g‘ri format! Kino kodini kiriting: `/removemovie <kino_kodi>`")
        return

    movie_code = args[1]
    if not os.path.exists("movies.txt"):
        await message.answer("🚫 Kino bazasi bo‘sh!")
        return

    with open("movies.txt", "r") as file:
        movies = file.readlines()

    new_movies = [movie.strip() for movie in movies if movie.strip() != movie_code]

    with open("movies.txt", "w") as file:
        file.write("\n".join(new_movies) + "\n")

    await message.answer(f"🗑 Kino o‘chirildi! Kod: `{movie_code}`", parse_mode="Markdown")

# /addchannel - Kanal qo‘shish (Faqat admin uchun)
@dp.message(Command("addchannel"))
async def add_channel(message: Message):
    if not is_admin(message.from_user.id):
        await message.answer("🚫 Sizda bu buyruqdan foydalanish huquqi yo‘q!")
        return

    args = message.text.split(maxsplit=1)
    if len(args) < 2:
        await message.answer("❌ Noto‘g‘ri format! Kanal username kiriting: `/addchannel @username`")
        return

    channel_username = args[1]
    with open("channels.txt", "a") as file:
        file.write(channel_username + "\n")

    await message.answer(f"✅ Kanal qo‘shildi! Username: `{channel_username}`", parse_mode="Markdown")

# /removechannel - Kanal o‘chirish (Faqat admin uchun)
@dp.message(Command("removechannel"))
async def remove_channel(message: Message):
    if not is_admin(message.from_user.id):
        await message.answer("🚫 Sizda bu buyruqdan foydalanish huquqi yo‘q!")
        return

    args = message.text.split(maxsplit=1)
    if len(args) < 2:
        await message.answer("❌ Noto‘g‘ri format! Kanal username kiriting: `/removechannel @username`")
        return

    channel_username = args[1]
    if not os.path.exists("channels.txt"):
        await message.answer("🚫 Kanal bazasi bo‘sh!")
        return

    with open("channels.txt", "r") as file:
        channels = file.readlines()

    new_channels = [ch.strip() for ch in channels if ch.strip() != channel_username]

    with open("channels.txt", "w") as file:
        file.write("\n".join(new_channels) + "\n")

    await message.answer(f"❌ Kanal o‘chirildi! Username: `{channel_username}`", parse_mode="Markdown")

# /channels - Saqlangan kanallar ro‘yxati (Faqat admin uchun)
@dp.message(Command("channels"))
async def channels_list(message: Message):
    if not is_admin(message.from_user.id):
        await message.answer("🚫 Bu buyruq faqat adminlar uchun!")
        return

    if not os.path.exists("channels.txt"):
        await message.answer("📂 Kanal bazasi bo‘sh!")
        return

    with open("channels.txt", "r") as file:
        channels = file.readlines()

    if not channels:
        await message.answer("📂 Kanal bazasi bo‘sh!")
        return

    channel_list = "\n".join([f"📡 {ch.strip()}" for ch in channels])
    await message.answer(f"📜 Saqlangan kanallar:\n\n{channel_list}")

# /stats - Statistika
@dp.message(Command("stats"))
async def stats(message: Message):
    users_count = 0
    movies_count = 0
    channels_count = 0

    if os.path.exists("users.txt"):
        with open("users.txt", "r") as file:
            users_count = len(file.readlines())

    if os.path.exists("movies.txt"):
        with open("movies.txt", "r") as file:
            movies_count = len(file.readlines())

    if os.path.exists("channels.txt"):
        with open("channels.txt", "r") as file:
            channels_count = len(file.readlines())

    await message.answer(f"📊 Statistika:\n🎥 Kinolar soni: {movies_count}\n📡 Kanallar soni: {channels_count}\n👥 Foydalanuvchilar soni: {users_count}")

# Yangi foydalanuvchini ro‘yxatga olish
@dp.message()
async def register_user(message: Message):
    user_id = str(message.from_user.id)
    if not os.path.exists("users.txt"):
        with open("users.txt", "w") as file:
            file.write(user_id + "\n")
    else:
        with open("users.txt", "r") as file:
            users = file.readlines()

        if user_id + "\n" not in users:
            with open("users.txt", "a") as file:
                file.write(user_id + "\n")

async def main():
    logging.basicConfig(level=logging.INFO)
    await dp.start_polling(bot)

if __name__ == "__main__":
    asyncio.run(main())
