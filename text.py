from aiogram import types

class RussianStrings():
    @staticmethod
    def get_start_text(message: types.Message):
        return f"Привет, {message.from_user.full_name}! Спасибо за регистрацию в боте!"
