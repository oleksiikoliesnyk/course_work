from aiogram import Bot, Dispatcher, types
from aiogram.contrib.fsm_storage.memory import MemoryStorage

from data import config
from utils.db_api.postgresql import DatabaseForAdmin, DatabaseForStudent, DatabaseForTeacher

bot = Bot(token=config.BOT_TOKEN, parse_mode=types.ParseMode.HTML)
storage = MemoryStorage()
dp = Dispatcher(bot, storage=storage)
db_admin = DatabaseForAdmin()
db_student = DatabaseForStudent()
db_teacher = DatabaseForTeacher()
