import os
from dotenv import load_dotenv

# .env faylini yuklash
load_dotenv()

# Bot tokeni va admin IDlar
BOT_TOKEN = os.getenv("BOT_TOKEN")
ADMIN_IDS = list(map(int, os.getenv("ADMIN_IDS", "").split(",")))

# Kanallar ro‘yxati
CHANNELS = os.getenv("CHANNELS", "").split(",")

# Kinolar kanali
MOVIE_CHANNEL = os.getenv("MOVIE_CHANNEL")
