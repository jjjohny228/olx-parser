import os

from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton, \
    KeyboardButton, ReplyKeyboardMarkup, ReplyKeyboardRemove
from aiogram.utils.callback_data import CallbackData


class MinesKeyboards:
    @staticmethod
    def get_signal_markup() -> InlineKeyboardMarkup:
        next_signal = InlineKeyboardButton('🔻 GET SIGNAL 🔻', callback_data='mines_next_signal')
        main_menu = InlineKeyboardButton('Choose another game 🔄', callback_data='client_menu')
        return InlineKeyboardMarkup(row_width=1).add(next_signal).add(main_menu)

    @staticmethod
    def get_menu_markup() -> InlineKeyboardMarkup:
        registration_button = InlineKeyboardButton('Registration📱', callback_data='mines_registration_menu')
        instruction_button = InlineKeyboardButton('Instruction📖', callback_data='mines_instruction_menu')
        get_signal_button = InlineKeyboardButton('🔻 GET SIGNAL 🔻', callback_data='mines_next_signal')
        return InlineKeyboardMarkup(row_width=2).add(registration_button, instruction_button).add(get_signal_button)



