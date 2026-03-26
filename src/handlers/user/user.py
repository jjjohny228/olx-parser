from aiogram import Dispatcher
from aiogram.dispatcher import FSMContext
from aiogram.dispatcher.filters import CommandStart
from aiogram.types import CallbackQuery, Message

from src.create_bot import bot
from src.database.user import (
    create_target,
    create_user_if_not_exist,
    get_locale,
    get_user_target,
    get_user_targets,
    normalize_language_code,
    set_locale,
    update_target,
)
from src.handlers.user.kb import Keyboards
from src.handlers.user.messages import Messages
from src.misc.user_states import UserTargetInputting
from src.utils import logger, send_typing_action


class Utils:
    @staticmethod
    async def is_valid_chat_id(chat_id: int | str) -> bool:
        try:
            await bot.get_chat(chat_id)
            return True
        except Exception as error:
            logger.error(f'Some error occurred: {error}')
            return False

    @staticmethod
    def get_user_language(user_id: int, telegram_language_code: str | None = None) -> str:
        return get_locale(user_id) or normalize_language_code(telegram_language_code)

    @staticmethod
    def is_cancel_action(text: str) -> bool:
        return text in Messages.get_button_variants('cancel_target')

    @staticmethod
    def parse_target_callback(callback_data: str, prefix: str) -> tuple[int, int]:
        payload = callback_data.removeprefix(prefix)
        target_id, page = payload.rsplit('_', 1)
        return int(target_id), int(page)

    @staticmethod
    def parse_target_edit_callback(callback_data: str) -> tuple[int, str, int]:
        payload = callback_data.removeprefix('target_edit_')
        target_id, field_payload = payload.split('_', 1)
        field_name, page = field_payload.rsplit('_', 1)
        return int(target_id), field_name, int(page)


class Handlers:
    @staticmethod
    async def __handle_add_target_button(message: Message, state: FSMContext):
        language_code = Utils.get_user_language(message.from_user.id, message.from_user.language_code)
        await message.answer(
            Messages.get_text('add_target_name', language_code),
            reply_markup=Keyboards.get_cancel_target_markup(language_code),
        )
        await state.set_state(UserTargetInputting.target_name)

    @staticmethod
    async def __handle_target_name(message: Message, state: FSMContext):
        language_code = Utils.get_user_language(message.from_user.id, message.from_user.language_code)
        await state.update_data(target_name=message.text)
        await message.answer(Messages.get_text('add_target_url', language_code))
        await state.set_state(UserTargetInputting.target_url)

    @staticmethod
    async def __handle_target_url(message: Message, state: FSMContext):
        language_code = Utils.get_user_language(message.from_user.id, message.from_user.language_code)
        if not message.text.startswith("https://"):
            await message.answer(Messages.get_text('wrong_target_url', language_code))
            return

        await state.update_data(target_url=message.text)
        await message.answer(Messages.get_text('add_target_chat_id', language_code))
        await state.set_state(UserTargetInputting.target_chat_id)

    @staticmethod
    async def __handle_chat_id(message: Message, state: FSMContext):
        language_code = Utils.get_user_language(message.from_user.id, message.from_user.language_code)
        if not await Utils.is_valid_chat_id(message.text):
            await message.answer(Messages.get_text('wrong_target_chat_id', language_code))
            return

        await state.update_data(chat_id=message.text)
        data = await state.get_data()

        create_target(
            message.from_user.id,
            data.get("target_name"),
            data.get("target_url"),
            data.get("chat_id"),
        )
        await message.answer(
            Messages.get_text('target_created', language_code),
            reply_markup=Keyboards.get_targets_menu(language_code),
        )
        await state.finish()

    @staticmethod
    async def __handle_cancel_action(message: Message, state: FSMContext):
        language_code = Utils.get_user_language(message.from_user.id, message.from_user.language_code)
        await message.answer(
            Messages.get_text('cancel_target', language_code),
            reply_markup=Keyboards.get_targets_menu(language_code),
        )
        await state.finish()

    @staticmethod
    async def __handle_main_menu(message: Message, state: FSMContext):
        await state.finish()
        await message.answer('🏠', reply_markup=Keyboards.get_main_menu_markup(message))

    @staticmethod
    async def __handle_my_targets(message: Message):
        language_code = Utils.get_user_language(message.from_user.id, message.from_user.language_code)
        user_targets = list(get_user_targets(message.from_user.id) or [])
        if user_targets:
            await message.answer(
                text=Messages.get_text('choose_target_to_edit', language_code),
                reply_markup=Keyboards.get_my_targets_markup(message.from_user.id),
            )
            return

        await message.answer(Messages.get_text('no_targets', language_code))

    @staticmethod
    async def __handle_targets_menu_callback(callback: CallbackQuery):
        language_code = Utils.get_user_language(callback.from_user.id, callback.from_user.language_code)
        await callback.answer()
        await callback.message.delete()
        await callback.message.answer(
            Messages.get_text('targets_menu_text', language_code),
            reply_markup=Keyboards.get_targets_menu(language_code),
        )

    @staticmethod
    async def __handle_start_command(message: Message, state: FSMContext) -> None:
        await state.finish()
        await send_typing_action(message)

        create_user_if_not_exist(
            username=message.from_user.username,
            first_name=message.from_user.first_name,
            last_name=message.from_user.last_name,
            telegram_id=message.from_user.id,
            language_code=message.from_user.language_code,
        )

        language_code = Utils.get_user_language(message.from_user.id, message.from_user.language_code)
        await message.answer(
            text=Messages.get_text('welcome_text', language_code),
            reply_markup=Keyboards.get_main_menu_markup(message),
        )

    @staticmethod
    async def __handle_targets_menu(message: Message):
        language_code = Utils.get_user_language(message.from_user.id, message.from_user.language_code)
        await message.answer(
            text=Messages.get_text('targets_menu_text', language_code),
            reply_markup=Keyboards.get_targets_menu(language_code),
        )

    @staticmethod
    async def __change_target_page(callback_query: CallbackQuery):
        page = int(callback_query.data.split("_")[1])
        await callback_query.message.edit_reply_markup(
            reply_markup=Keyboards.get_my_targets_markup(callback_query.from_user.id, page),
        )
        await callback_query.answer()

    @staticmethod
    async def __handle_ignore_callback(callback_query: CallbackQuery):
        await callback_query.answer()

    @staticmethod
    async def __handle_target_card(callback_query: CallbackQuery):
        target_id, page = Utils.parse_target_callback(callback_query.data, 'target_')
        target = get_user_target(callback_query.from_user.id, target_id)
        language_code = Utils.get_user_language(callback_query.from_user.id, callback_query.from_user.language_code)
        if target is None:
            await callback_query.answer(Messages.get_text('target_not_found', language_code), show_alert=True)
            return

        await callback_query.message.edit_text(
            Messages.get_target_details_text(target, language_code),
            reply_markup=Keyboards.get_target_actions_markup(target.id, language_code, page, target.active),
        )
        await callback_query.answer()

    @staticmethod
    async def __handle_target_toggle(callback_query: CallbackQuery):
        target_id, page = Utils.parse_target_callback(callback_query.data, 'target_toggle_')
        target = get_user_target(callback_query.from_user.id, target_id)
        language_code = Utils.get_user_language(callback_query.from_user.id, callback_query.from_user.language_code)
        if target is None:
            await callback_query.answer(Messages.get_text('target_not_found', language_code), show_alert=True)
            return

        new_active_value = not target.active
        update_target(target.id, active=new_active_value)
        target = get_user_target(callback_query.from_user.id, target_id)

        await callback_query.message.edit_text(
            Messages.get_target_details_text(target, language_code),
            reply_markup=Keyboards.get_target_actions_markup(target.id, language_code, page, target.active),
        )
        callback_key = 'target_active_enabled' if new_active_value else 'target_active_disabled'
        await callback_query.answer(Messages.get_text(callback_key, language_code))

    @staticmethod
    async def __handle_target_edit_start(callback_query: CallbackQuery, state: FSMContext):
        target_id, field_name, page = Utils.parse_target_edit_callback(callback_query.data)
        target = get_user_target(callback_query.from_user.id, target_id)
        language_code = Utils.get_user_language(callback_query.from_user.id, callback_query.from_user.language_code)
        if target is None:
            await callback_query.answer(Messages.get_text('target_not_found', language_code), show_alert=True)
            return

        await state.update_data(
            edit_target_id=target.id,
            edit_target_field=field_name,
            edit_target_page=page,
        )
        await state.set_state(UserTargetInputting.target_edit_value)

        prompt_key = {
            'name': 'edit_name_prompt',
            'url': 'edit_url_prompt',
            'chat_id': 'edit_chat_id_prompt',
        }[field_name]
        await callback_query.message.answer(
            Messages.get_text(prompt_key, language_code),
            reply_markup=Keyboards.get_cancel_target_markup(language_code),
        )
        await callback_query.answer()

    @staticmethod
    async def __handle_target_edit_value(message: Message, state: FSMContext):
        language_code = Utils.get_user_language(message.from_user.id, message.from_user.language_code)
        data = await state.get_data()
        target = get_user_target(message.from_user.id, int(data['edit_target_id']))
        if target is None:
            await message.answer(Messages.get_text('target_not_found', language_code))
            await state.finish()
            return

        field_name = data['edit_target_field']
        new_value = message.text.strip()

        if field_name == 'url' and not new_value.startswith('https://'):
            await message.answer(Messages.get_text('wrong_target_url', language_code))
            return

        if field_name == 'chat_id' and not await Utils.is_valid_chat_id(new_value):
            await message.answer(Messages.get_text('wrong_target_chat_id', language_code))
            return

        update_target(target.id, **{field_name: new_value})
        updated_target = get_user_target(message.from_user.id, target.id)
        await message.answer(
            Messages.get_text('target_updated', language_code),
            reply_markup=Keyboards.get_targets_menu(language_code),
        )
        await message.answer(
            Messages.get_target_details_text(updated_target, language_code),
            reply_markup=Keyboards.get_target_actions_markup(
                updated_target.id,
                language_code,
                data['edit_target_page'],
                updated_target.active,
            ),
        )
        await state.finish()

    @staticmethod
    async def __handle_language_menu(message: Message):
        language_code = Utils.get_user_language(message.from_user.id, message.from_user.language_code)
        await message.answer(
            Messages.get_text('language_prompt', language_code),
            reply_markup=Keyboards.get_language_menu(),
        )

    @staticmethod
    async def __handle_language_change(callback_query: CallbackQuery):
        selected_language = callback_query.data.removeprefix('language_')
        set_locale(callback_query.from_user.id, selected_language)
        await callback_query.answer(Messages.get_text('language_updated', selected_language))
        await callback_query.message.edit_text(Messages.get_text('language_updated', selected_language))
        await callback_query.message.answer(
            Messages.get_text('welcome_text', selected_language),
            reply_markup=Keyboards.get_main_menu_markup(callback_query.message),
        )

    @classmethod
    def register_user_handlers(cls, dp: Dispatcher) -> None:
        dp.register_message_handler(cls.__handle_start_command, CommandStart(), state='*')
        dp.register_message_handler(
            cls.__handle_cancel_action,
            lambda message: Utils.is_cancel_action(message.text),
            state='*',
        )
        dp.register_message_handler(
            cls.__handle_add_target_button,
            lambda message: message.text in Messages.get_button_variants('add_target'),
            state=None,
        )
        dp.register_message_handler(cls.__handle_target_name, state=UserTargetInputting.target_name)
        dp.register_message_handler(cls.__handle_target_url, state=UserTargetInputting.target_url)
        dp.register_message_handler(cls.__handle_chat_id, state=UserTargetInputting.target_chat_id)
        dp.register_message_handler(cls.__handle_target_edit_value, state=UserTargetInputting.target_edit_value)
        dp.register_message_handler(
            cls.__handle_targets_menu,
            lambda message: message.text in Messages.get_button_variants('targets_menu'),
            state=None,
        )
        dp.register_message_handler(
            cls.__handle_language_menu,
            lambda message: message.text in Messages.get_button_variants('language_menu'),
            state=None,
        )
        dp.register_message_handler(
            cls.__handle_main_menu,
            lambda message: message.text in Messages.get_button_variants('main_menu'),
            state='*',
        )
        dp.register_callback_query_handler(
            cls.__handle_target_edit_start,
            lambda callback: callback.data.startswith('target_edit_'),
            state='*',
        )
        dp.register_callback_query_handler(
            cls.__handle_target_toggle,
            lambda callback: callback.data.startswith('target_toggle_'),
            state='*',
        )
        dp.register_callback_query_handler(
            cls.__change_target_page,
            lambda callback: callback.data.startswith("page_") and callback.data.endswith("target"),
        )
        dp.register_callback_query_handler(
            cls.__handle_ignore_callback,
            lambda callback: callback.data == 'none',
        )
        dp.register_callback_query_handler(
            cls.__handle_target_card,
            lambda callback: callback.data.startswith('target_') and callback.data.count('_') == 2,
        )
        dp.register_callback_query_handler(
            cls.__handle_targets_menu_callback,
            lambda callback: callback.data == 'my_targets_menu',
        )
        dp.register_callback_query_handler(
            cls.__handle_language_change,
            lambda callback: callback.data.startswith('language_'),
            state='*',
        )
        dp.register_message_handler(
            cls.__handle_my_targets,
            lambda message: message.text in Messages.get_button_variants('my_targets'),
            state=None,
        )


def register_user_handlers(dp: Dispatcher):
    Handlers.register_user_handlers(dp)
