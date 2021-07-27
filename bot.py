from functools import total_ordering
import logging
import os
from aiogram import Bot, Dispatcher, executor, types
from db import Visit, Visiter
from sqlalchemy.sql import func
from text import RussianStrings
from db import Session
from datetime import datetime


def configure_logging():
    log_level = logging.INFO
    if os.environ.get("LOG_LEVEL", "") == "DEBUG":
        log_level = logging.DEBUG
    log_config = {
        "level": log_level,
        "format": "%(asctime)s\t%(levelname)s\t%(message)s",
        "datefmt": "%Y-%m-%d %H:%M:%S",
    }

    logging.basicConfig(**log_config)


configure_logging()
TG_BOT_ENVIRON_VARIABLE_NAME = "TG_TILIS_BOT"
TG_BOT_API_TOKEN = os.environ.get(TG_BOT_ENVIRON_VARIABLE_NAME, None)
logger = logging.getLogger()
strings = RussianStrings()

if TG_BOT_API_TOKEN is None:
    logger.error(
        f"{TG_BOT_ENVIRON_VARIABLE_NAME} is not found in enviroment. Please set it and try again"
    )
    exit(0)

bot = Bot(token=TG_BOT_API_TOKEN)
dp = Dispatcher(bot)


def find_user_by_id(db_session, tg_id):
    visiter_query = db_session.query(Visiter).filter_by(tg_id=tg_id).first()
    return visiter_query


@dp.message_handler(commands="start")
async def start_start_handler(message: types.Message):
    logger.info(f"{message.from_user.full_name} has started the bot.")
    db_session = Session()

    visiter = find_user_by_id(db_session, message.from_user.id)
    if visiter is None:
        visiter = Visiter(
            tg_id=message.from_user.id, name=message.from_user.full_name, donate_sum=0
        )
        db_session.add(visiter)

    visiter_balance = visiter.donate_sum
    for visit in visiter.visits:
        visiter_balance -= visit.total_payment

    db_session.commit()

    await message.reply(
        strings.get_start_text(message, visiter_balance),
        parse_mode=types.ParseMode.MARKDOWN,
    )


@dp.message_handler(commands="visit")
async def start_visit_handler(message: types.Message):
    logger.info(f"{message.from_user.full_name} added new visit")
    db_session = Session()
    visit = Visit(date=datetime.now(), total_payment=0)
    visiter = find_user_by_id(db_session, message.from_user.id)
    if visiter is None:
        return await message.reply("Пожалуйста сначала зарегестрируйтесь в боте")

    visit.visiters.append(visiter)
    logger.info(f"Created new visit with id {visit.visit_id}")

    keyboard_markup = types.InlineKeyboardMarkup(row_width=3)
    btns_and_data = (("Я туть", f"visit|1"), ("Я не туть", f"visit|0"))
    keyboard_markup.row(*(types.InlineKeyboardButton(text, callback_data=data) for text, data in btns_and_data))
    
    visit_message = await message.reply(strings.get_visit_text(visit), reply_markup=keyboard_markup)
    visit.tg_message_id = visit_message.message_id
    
    db_session.add(visit)
    db_session.commit()

    return 


@dp.callback_query_handler(lambda query: query.data.startswith('visit|'))
async def inline_kb_visit_handler(query: types.CallbackQuery):
    status = query.data.split('|')[1]
    db_session = Session()
    visit = db_session.query(Visit).filter_by(tg_message_id=query.message.message_id).first()
    if visit is None:
        logger.error("Unexpected code")
        return

    visiter = find_user_by_id(db_session, query.from_user.id)
    if visiter is None:
        return
    
    smth_changed = False
    if status == '1':
        if visiter not in visit.visiters:
            visit.visiters.append(visiter)
            smth_changed = True
        else:
            await query.answer('Слышь, ты уже туть!')
    
    elif status == '0':
        if visiter in visit.visiters:
            visit.visiters.remove(visiter)
            smth_changed = True
        else:
            await query.answer('Эй! Ты уже не туть!')
    
    print(list(visit.visiters))
    db_session.commit()

    if smth_changed:
        await query.message.edit_text(strings.get_visit_text(visit), reply_markup=query.message.reply_markup)

    return 


if __name__ == "__main__":
    executor.start_polling(dp, skip_updates=True)
