from aiogram import types
from aiogram.dispatcher.filters.builtin import CommandStart
from aiogram.types import CallbackQuery

from data.db_constant import facultys
from keyboards.inline.faculty_button.faculty_button import fac_choice
from keyboards.inline.type_button.type_button import type_choice
from keyboards.inline.type_button.type_callback import type_callback
from loader import dp, db_admin as db
from utils.db_api.test_postgtes import query_results


@dp.message_handler(CommandStart())
async def bot_start(message: types.Message):
    await message.answer('Вы студент или преподаватель?', reply_markup=type_choice)


@dp.callback_query_handler(type_callback.filter(type='Student'))
async def what_faculty(call: CallbackQuery, callback_data: dict):
    await call.answer(cache_time=60)
    my_facultys = db.get_faculty()
    res_string = f'Вот список факультетов: {my_facultys}\n Напишите, с какого вы?'
    await call.message.answer(res_string, reply_markup=fac_choice)


@dp.message_handler()
async def what_specialization(message: types.Message):
    my_facultys = facultys.split(', ')
    if message.text in my_facultys:
        await message.answer(f'Ага! Ты учишься в {my_facultys}')


@dp.callback_query_handler(type_callback.filter(type='Student'))
async def bot_student_login(message: types.Message):
    await message.answer('Привет, студент! Как тебя зовут?')
    # try:
    #    user = await db.add_user(telegram_id=message.from_user.id,
    #                             full_name=message.from_user.full_name,
    #                             username=message.from_user.username)
    # except asyncpg.exceptions.UniqueViolationError:
    #    user = await db.select_user(telegram_id=message.from_user.id)

    # count = await db.count_users()

    # Забираем как список или как словарь
    # user_data = list(user)
    # user_data_dict = dict(user)

    # Забираем напрямую как из списка или словаря
    # username = user.get("username")
    # full_name = user[2]

    # await message.answer(
    #    "\n".join(
    #        [
    #            f'Привет, {message.from_user.full_name}!',
    #            f'Ты был занесен в базу',
    #            f'В базе <b>{count}</b> пользователей',
    #            "",
    #            f"<code>User: {username} - {full_name}",
    #            f"{user_data=}",
    #            f"{user_data_dict=}</code>"
    #        ]))
