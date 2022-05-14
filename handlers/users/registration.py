from aiogram import types
from aiogram.dispatcher import FSMContext
from aiogram.dispatcher.filters.builtin import CommandStart
from aiogram.types import CallbackQuery

from data.controller import Student
from data.db_constant import facultys
from data.global_conf import my_global_dict
from handlers.users.admin_free import see_speciality
from keyboards.inline.faculty_button.faculty_button import fac_choice
from keyboards.inline.type_button.type_button import type_choice
from keyboards.inline.type_button.type_callback import type_callback
from loader import dp, db_admin as db, db_admin
from states.Dean import DeanState
from states.Student import StudentState
from utils.db_api.test_postgtes import query_results



@dp.callback_query_handler(type_callback.filter(type='Student'))
async def register_student(call: CallbackQuery, callback_data: dict):
    await call.answer(cache_time=60)
    # my_facultys = db.get_facultyes()
    await call.message.answer('Ваш профиль будет сохранен как профиль студент! (напишите что угодно)')
    await StudentState.WhichCourse.set()
    # res_string = f'Вот список факультетов: {my_facultys}\n Напишите, с какого вы?'
    # await call.message.answer(res_string, reply_markup=fac_choice)


@dp.message_handler(state=StudentState.WhichCourse)
async def register_student_2(message: types.Message):
    await message.answer('Какой курс?')
    await StudentState.WhichSpec.set()


@dp.message_handler(state=StudentState.WhichSpec)
async def register_student_3(message: types.Message):
    my_global_dict['register_student_course'] = message.text
    await see_speciality(message, None)
    await message.answer('Какая специальность?')
    await StudentState.FinalReg.set()


@dp.message_handler(state=StudentState.FinalReg)
async def register_student_3(message: types.Message):
    name_spec = message.text
    id_spec = db_admin.get_speciality_id_by_name(name_spec)
    #id_spec = db.get_speciality_id_by_name(name_spec)
    my_student = Student()
    data_to_write = {'password': message.from_user.id,
                     'full_name': message.from_user.full_name,
                     'name': message.from_user.username,
                     'course': my_global_dict['register_student_course'],
                     'id_spec': id_spec[0]}
    my_student.write(data_to_write)
    #db.save_student(password=message.from_user.id,
    #                full_name=message.from_user.full_name,
    #                name=message.from_user.username,
    #                id_spec=id_spec,
    #                course=my_global_dict['register_student_course'])
    await StudentState.FreeState.set()


@dp.callback_query_handler(type_callback.filter(type='Teacher'))
async def register_teacher(call: CallbackQuery, callback_data: dict):
    await call.answer(cache_time=60)
    await call.message.answer('Вы будете сохранены как преподаватель')
    db.save_teacher(password=call.from_user.id,
                    full_name=call.from_user.full_name,
                    name=call.from_user.username)

@dp.callback_query_handler(type_callback.filter(type='Dean'))
async def register_dean(call: CallbackQuery, callback_data: dict):
    await call.answer(cache_time=60)
    await call.message.answer('Ваш профиль будет сохранен как профиль админа!')
    print(callback_data)
    db.save_admin(password=call.from_user.id,
                 full_name=call.from_user.full_name,
                 name=call.from_user.username)
    await call.message.answer('Чтобы узнать, какие команды вам доступны, вбейте команду "/help"')
    await DeanState.FreeState.set()

