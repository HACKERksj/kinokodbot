import logging
from aiogram import Bot
from aiogram.exceptions import TelegramBadRequest
from config import CHANNELS, BOT_TOKEN  # config.py dan import qilish

bot = Bot(token=BOT_TOKEN)  # Bot obyektini yaratamiz

async def check_subscription(user_id: int) -> bool:
    """
    Foydalanuvchini majburiy obuna bo‘lganligini tekshiradi.
    """
    for channel in CHANNELS:
        try:
            chat_member = await bot.get_chat_member(chat_id=channel, user_id=user_id)
            if chat_member.status in ["member", "administrator", "creator"]:
                return True  # Obuna bo‘lgan
        except TelegramBadRequest:
            logging.warning(f"Channel {channel} mavjud emas yoki bot admin emas!")
            return False  # Kanalni topib bo‘lmadi yoki bot admin emas
    return False  # Agar barcha kanallardan chiqib ketgan bo‘lsa
