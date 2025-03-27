import logging
from aiogram import Bot
from aiogram.exceptions import TelegramBadRequest
from config import CHANNELS, BOT_TOKEN

bot = Bot(token=BOT_TOKEN)

async def check_subscription(user_id: int) -> bool:
    """
    Foydalanuvchini majburiy obuna bo‘lganligini tekshiradi.
    """
    for channel in CHANNELS:
        try:
            chat_member = await bot.get_chat_member(chat_id=channel, user_id=user_id)
            if chat_member.status not in ["member", "administrator", "creator"]:
                return False  # Agar hech bo‘lmaganda bitta kanalga a'zo bo‘lmasa, False qaytadi
        except TelegramBadRequest:
            logging.warning(f"Channel {channel} mavjud emas yoki bot admin emas!")
            return False  # Agar kanal topilmasa yoki bot admin bo‘lmasa, False qaytarish kerak
    return True  # Foydalanuvchi barcha kanallarga a’zo bo‘lsa, True qaytaradi
