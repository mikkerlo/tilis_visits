from typing import List
from aiogram import types
from db import Visit, Visiter
from datetime import datetime

class RussianStrings():
    @staticmethod
    def get_start_text(message: types.Message, balance: int):
        return f"Привет, {message.from_user.full_name}! Ваш текущий баланс {balance}€"

    @staticmethod
    def get_visit_text(visit: Visit):
        names = [v.name for v in visit.visiters]
        list_of_names = '\n'.join(names)
        if names:
            current_cost = f"Текущая стоимость: {visit.total_payment} или {visit.total_payment / len(names)} на чела"
        else:
            current_cost = f"Текущая стоимость: {visit.total_payment}"
        return f"Визит в Тилис {visit.date.strftime('%d.%m %H:%M')}\n{current_cost}\nУже вписались:\n{list_of_names}"
