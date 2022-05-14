from aiogram import types
from aiogram.dispatcher.filters.builtin import CommandStart
from aiogram.types import CallbackQuery

from data.db_constant import facultys
from keyboards.inline.faculty_button.faculty_button import fac_choice
from keyboards.inline.type_button.type_button import type_choice
from keyboards.inline.type_button.type_callback import type_callback
from loader import dp, db_admin as db
from states.Dean import DeanState
from states.Student import StudentState


@dp.message_handler(CommandStart())
async def bot_start(message: types.Message):
    try:
        user, specialization = db.get_user_by_credentionals(password=message.from_user.id,
                                                            full_name=message.from_user.full_name,
                                                            username=message.from_user.username)
        if user:
            if specialization == 'dean':
                await message.answer('Вы вошли как админ')
                await DeanState.FreeState.set()
            elif specialization == 'teacher':
                await message.answer('Тут выполнится машина состояний для преподавателя')
            else:
                await message.answer('Вы вошли как студент')
                await StudentState.FreeState.set()
        else:
            await message.answer('Приветствуем, новый пользователь!')
            await message.answer('Какая ваша роль?', reply_markup=type_choice)

        # user = await db.add_user(telegram_id=message.from_user.id,
        #                         full_name=message.from_user.full_name,
        #                         username=message.from_user.username)
    except Exception as err:
        await message.answer(f'Ошибка бота при инициализации = {err}')

        # user = await db.select_user(telegram_id=message.from_user.id)
