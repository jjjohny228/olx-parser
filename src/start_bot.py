from aiogram import executor

from src.middlewares.throttling import setup_middleware
from src.handlers import register_all_handlers
from src.filters import register_all_filters
from src.database.models import register_models
from src.create_bot import dp, bot
from src.utils import logger


async def on_startup(_):
    # Throttling registration
    setup_middleware(dp)

    # Filter registration
    register_all_filters(dp)

    # Handler registration
    register_all_handlers(dp)

    # Registering database models
    register_models()

    logger.info('The bot is up and running!')


async def on_shutdown(_):
    await (await bot.get_session()).close()


def start_bot():
    try:
        executor.start_polling(dp, on_startup=on_startup, on_shutdown=on_shutdown, skip_updates=True)
    except Exception as e:
        logger.error(e)
