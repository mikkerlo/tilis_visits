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
        'level': log_level,
        'format': '%(asctime)s\t%(levelname)s\t%(message)s',
        'datefmt': '%Y-%m-%d %H:%M:%S',
    }

    logging.basicConfig(**log_config)

configure_logging()
TG_BOT_ENVIRON_VARIABLE_NAME = "TG_TILIS_BOT"
TG_BOT_API_TOKEN = os.environ.get(TG_BOT_ENVIRON_VARIABLE_NAME, None)
logger = logging.getLogger()
strings = RussianStrings()

if TG_BOT_API_TOKEN is None:
    logger.error(f"{TG_BOT_ENVIRON_VARIABLE_NAME} is not found in enviroment. Please set it and try again")
    exit(0)

bot = Bot(token=TG_BOT_API_TOKEN)
dp = Dispatcher(bot)

@dp.message_handler(commands='start')
async def start_start_handler(message: types.Message):
    logger.info(f'{message.from_user.full_name} has started the bot.')
    db_session = Session()
    
    visiter_query = db_session.query(Visiter).filter_by(tg_id=message.from_user.id).first()
    if visiter_query:
        visiter = visiter_query
    else:
        visiter = Visiter(tg_id=message.from_user.id, name=message.from_user.full_name, donate_sum=0)
        db_session.add(visiter)
    
    visiter_balance = visiter.donate_sum
    for visit in visiter.visits:
        visiter_balance -= visit.total_payment
    
    db_session.commit()
    
    await message.reply(strings.get_start_text(message, visiter_balance), parse_mode=types.ParseMode.MARKDOWN)


@dp.message_handler(commands='visit')
async def start_visit_handler(message: types.Message):
    logger.info(f'{message.from_user.full_name} added new visit')
    visit = Visit(date=datetime.now())

if __name__ == '__main__':
    executor.start_polling(dp, skip_updates=True)
