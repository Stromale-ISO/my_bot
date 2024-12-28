import os
from dotenv import load_dotenv
load_dotenv()
BOT_TOKEN = os.getenv("BOT_TOKEN")
AUTHORIZED_USERS = os.getenv("AUTHORIZED_USERS", "").split(",")
AUTHORIZED_USERS = [int(user_id.strip()) for user_id in AUTHORIZED_USERS if user_id.strip().isdigit()]
