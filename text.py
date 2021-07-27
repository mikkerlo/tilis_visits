from aiogram import types

class RussianStrings():
    def get_start_text(message: types.Message):
        f"Привет, {message.from_user.get_mention}! Спасибо за регистрацию в боте!"
