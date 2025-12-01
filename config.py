import os
from typing import Final
from dotenv import load_dotenv


load_dotenv()


class Config:
    TOKEN: Final = os.getenv('BOT_TOKEN', 'Enter bot token to the .env!')
    ADMIN_IDS: Final = tuple(int(i) for i in str(os.getenv('BOT_ADMIN_IDS')).split(','))


    DEBUG: Final = bool(os.getenv('DEBUG'))
