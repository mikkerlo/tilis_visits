from aiogram import types
from db import Visiter

class RussianStrings():
    @staticmethod
    def get_start_text(message: types.Message, balance: int):
        return f"Привет, {message.from_user.full_name}! Ваш текущий баланс {balance}€"
