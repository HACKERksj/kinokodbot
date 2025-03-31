import os
from dotenv import load_dotenv

load_dotenv()

BOT_TOKEN = os.getenv("BOT_TOKEN")

# ADMIN_IDS ni int formatida yuklash
admin_ids_str = os.getenv("ADMIN_IDS", "").strip()
ADMIN_IDS = list(map(int, admin_ids_str.split(","))) if admin_ids_str else []

# Tekshirish uchun chiqaryapmiz
print("Adminlar ro‘yxati:", ADMIN_IDS)

CHANNELS = os.getenv("CHANNELS", "").split(",")
MOVIE_CHANNEL = os.getenv("MOVIE_CHANNEL")
