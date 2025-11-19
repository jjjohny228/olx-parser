import os
import datetime
import random

from aiogram.types import InputFile

from config import Config


class Messages:
    @staticmethod
    def get_loading() -> str:
        return '♻ Loading...'

    @staticmethod
    def get_menu_photo() -> str:
        return 'https://telegra.ph/file/074593e0294e1ffcc538e.jpg'

    @staticmethod
    def get_instruction_text() -> str:
        return (
            "The bot is based on and trained using OpenAI's neural network cluster 🖥[ChatGPT-v4].\n\n"
            "For training, the bot played 🎰over 8000 games.\nCurrently, bot users successfully make 20-30% of their 💸 capital daily!\n\n"
            "The bot is still learning, and its accuracy is at 87%!\n\n "
            "Follow these instructions for maximum profit: \n\n"
            "🔸 1.  Register at the 1WIN. If it doesn’t open - use a VPN (Sweden). I use VPN Super Unlimited Proxy\n\n"
            "🔸 2. Deposit funds into your account.\n\n"
            "🔸 3. Go to the 1win games section and select the 💣'MINES' game.\n\n"
            "🔸 4. Set the number of traps to three. This is important!\n\n"
            "🔸 5. Request a signal from the bot and place bets based on the bot’s signals.\n\n"
            "🔸 6. In case of a losing signal, we advise you to double (X2) your bet to fully cover the loss in the next signal."
        )

    @staticmethod
    def get_instruction_video() -> InputFile:
        return InputFile('resources/mines/instruction.mp4')

    @staticmethod
    def get_throttled_error() -> str:
        return 'Пожалуйста, не так часто 🙏'
