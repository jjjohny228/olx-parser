import asyncio
import re

from aiogram import Dispatcher
from aiogram.dispatcher import FSMContext
from aiogram.dispatcher.filters import CommandStart
from aiogram.types import CallbackQuery, Message
from aiogram.utils import exceptions
from aiogram.utils.exceptions import ChatNotFound, BotBlocked

from src.database.user import create_user_if_not_exist
from src.utils import send_typing_action
# from src.misc import UserDataInputting
from .messages import Messages
from src.filters.filter_func import check_is_admin
from src.handlers.admin.admin import send_admin_menu
# from .kb import Keyboards
from config import Config
from src.utils import logger
from src.create_bot import bot


async def __handle_start_command(message: Message, state: FSMContext) -> None:
    await state.finish()
    if await check_is_admin(message):
        await send_admin_menu(message)
    else:
        # await send_typing_action(message)
        #
        # create_user_if_not_exist(
        #     telegram_id=message.from_id,
        #     name=message.from_user.username or message.from_user.full_name,
        #     reflink=message.get_full_command()[1]
        # )
        #
        # await message.answer_photo(
        #     photo=Messages.get_welcome_photo_url(),
        #     caption=Messages.get_welcome(),
        #     reply_markup=Keyboards.get_welcome_menu()
        # )
        pass
# async def __handle_next_signal_callback(callback: CallbackQuery):
#     # Удаляем сообщение
#     menu_owner = callback.data.split('_')[0]
#     await callback.answer(text=MinesMessages.get_loading())
#     await callback.message.delete()
#     msg = await callback.message.answer('⌛️ Waiting...')
#     delay_seconds = random.uniform(2, 3)
#
#     await asyncio.sleep(delay_seconds)
#     await msg.delete()
#
#     if get_user_1win_id(callback.message.chat.id):
#         new_photo = MinesMessages.get_random_signal()
#
#         await callback.message.answer_photo(photo=new_photo,
#                                             caption=MinesMessages.get_signal_text(),
#                                             reply_markup=MinesKeyboards.get_signal_markup())
#     else:
#         await callback.message.answer_photo(
#             caption=CommonMessages.get_registration_text(callback.message.chat.first_name),
#             photo=CommonMessages.get_registration_explanation_photo(),
#             reply_markup=CommonKeyboards.get_registration_menu(menu_owner)
#         )
#     await callback.answer()
#
#
# async def __handle_menu_callback(callback: CallbackQuery):
#     await callback.message.delete()
#     await callback.message.answer_photo(photo=MinesMessages.get_menu_photo(),
#                                         caption=MinesMessages.get_menu_text(),
#                                         reply_markup=MinesKeyboards.get_menu_markup())
#     await callback.answer()
#
#
# async def __handle_instruction_callback(callback: CallbackQuery):
#     menu_owner = callback.data.split('_')[0]
#     await callback.message.delete()
#
#     await callback.message.answer_video(
#         video=MinesMessages.get_instruction_video(),
#         caption=MinesMessages.get_instruction_text(),
#         reply_markup=CommonKeyboards.get_instruction_menu(menu_owner)
#     )



def register_user_handlers(dp: Dispatcher) -> None:
    dp.register_message_handler(__handle_start_command, CommandStart())
    # dp.register_callback_query_handler(__handle_next_signal_callback, text='mines_next_signal')
    # dp.register_callback_query_handler(__handle_menu_callback, text='mines_menu')
    # dp.register_callback_query_handler(__handle_instruction_callback, text='mines_instruction_menu')
