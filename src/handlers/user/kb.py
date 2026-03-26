from typing import Optional

from aiogram import types
from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton, KeyboardButton, ReplyKeyboardMarkup

from src.database.user import get_user_targets, get_locale
from src.handlers.user.messages import Messages
from src.utils import logger


class Keyboards:
    PAIRS_PER_PAGE = 4

    @staticmethod
    def get_main_menu_markup(message: types.Message) -> ReplyKeyboardMarkup:
        language_code = get_locale(message.from_user.id)
        keyboard = ReplyKeyboardMarkup(resize_keyboard=True, row_width=2)
        keyboard.add(
            KeyboardButton(Messages.get_button('targets_menu', language_code)),
            KeyboardButton(Messages.get_button('language_menu', language_code)),
        )
        return keyboard

    @staticmethod
    def get_targets_menu(language_code: str | None) -> ReplyKeyboardMarkup:
        my_targets_button = KeyboardButton(Messages.get_button('my_targets', language_code))
        add_target_button = KeyboardButton(Messages.get_button('add_target', language_code))
        back_button = KeyboardButton(Messages.get_button('main_menu', language_code))
        return ReplyKeyboardMarkup(resize_keyboard=True, row_width=2).row(my_targets_button, add_target_button).add(back_button)

    @staticmethod
    def get_cancel_target_markup(language_code: str | None) -> ReplyKeyboardMarkup:
        return ReplyKeyboardMarkup(resize_keyboard=True, row_width=1).add(
            KeyboardButton(Messages.get_button('cancel_target', language_code))
        )

    @staticmethod
    def get_language_menu() -> InlineKeyboardMarkup:
        keyboard = InlineKeyboardMarkup(row_width=2)
        keyboard.add(
            InlineKeyboardButton(text=Messages.get_language_button('ru'), callback_data='language_ru'),
            InlineKeyboardButton(text=Messages.get_language_button('uk'), callback_data='language_uk'),
        )
        keyboard.add(InlineKeyboardButton(text=Messages.get_language_button('en'), callback_data='language_en'))
        return keyboard

    @classmethod
    def get_my_targets_markup(cls, user_telegram_id: int, page: int = 0) -> Optional[InlineKeyboardMarkup]:
        user_targets = list(get_user_targets(user_telegram_id) or [])
        keyboard = InlineKeyboardMarkup(row_width=2)
        start_idx = page * cls.PAIRS_PER_PAGE
        end_idx = start_idx + cls.PAIRS_PER_PAGE
        if not user_targets:
            logger.error("User doesnt have any targets")
            return None

        current_targets = user_targets[start_idx:end_idx]

        for target in current_targets:
            status_emoji = '🟢' if target.active else '⚪'
            keyboard.insert(
                InlineKeyboardButton(text=f"{status_emoji} {target.name}", callback_data=f"target_{target.id}_{page}")
            )

        total_pages = (len(user_targets) - 1) // cls.PAIRS_PER_PAGE + 1
        pagination_buttons = []

        if page > 0:
            pagination_buttons.append(InlineKeyboardButton(text="⬅️", callback_data=f"page_{page - 1}_target"))

        pagination_buttons.append(InlineKeyboardButton(text=f"{page + 1}/{total_pages}", callback_data="none"))

        if end_idx < len(user_targets):
            pagination_buttons.append(InlineKeyboardButton(text="➡️", callback_data=f"page_{page + 1}_target"))

        keyboard.row(*pagination_buttons)
        return keyboard

    @staticmethod
    def get_target_actions_markup(target_id: int, language_code: str | None, page: int = 0,
                                  is_active: bool = True) -> InlineKeyboardMarkup:
        normalized_code = Messages.normalize_language(language_code)
        toggle_text = Messages.get_text('disable_target', normalized_code) if is_active else Messages.get_text('enable_target', normalized_code)

        keyboard = InlineKeyboardMarkup(row_width=1)
        keyboard.add(
            InlineKeyboardButton(
                text=f"{Messages.get_text('field_name', normalized_code)} ✏️",
                callback_data=f"target_edit_{target_id}_name_{page}",
            ),
            InlineKeyboardButton(
                text=f"{Messages.get_text('field_url', normalized_code)} ✏️",
                callback_data=f"target_edit_{target_id}_url_{page}",
            ),
            InlineKeyboardButton(
                text=f"{Messages.get_text('field_chat_id', normalized_code)} ✏️",
                callback_data=f"target_edit_{target_id}_chat_id_{page}",
            ),
            InlineKeyboardButton(text=toggle_text, callback_data=f"target_toggle_{target_id}_{page}"),
        )
        return keyboard

    @staticmethod
    def get_url_keyboard(url: str, language_code: str | None) -> InlineKeyboardMarkup:
        keyboard = InlineKeyboardMarkup(row_width=1)
        url_button = InlineKeyboardButton(text=Messages.get_text('ad_button', language_code), url=url)
        keyboard.add(url_button)
        return keyboard
