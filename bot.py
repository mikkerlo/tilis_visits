import logging
import os
from aiogram import Bot, Dispatcher, executor, types
from db import Visit, Visiter
from sqlalchemy import create_engine
from text import RussianStrings

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
engine = create_engine("sqlite:///:memory:", echo=True)
logger = logging.getLogger()
strings = RussianStrings()

if TG_BOT_API_TOKEN is None:
    logger.error(f"{TG_BOT_ENVIRON_VARIABLE_NAME} is not found in enviroment. Please set it and try again")
    exit(0)

bot = Bot(token=TG_BOT_API_TOKEN)
dp = Dispatcher(bot)

@dp.message_handler(commands='start')
async def start_start_handler(message: types.Message):
    message.reply(strings.get_start_text(message))
