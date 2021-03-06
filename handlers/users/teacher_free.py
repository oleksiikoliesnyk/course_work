import logging
from datetime import datetime

from aiogram import types
from aiogram.dispatcher import FSMContext
from aiogram.dispatcher.filters.builtin import CommandStart, Command, CommandHelp
from aiogram.types import CallbackQuery

from data.db_constant import facultys
from data.global_conf import my_global_dict
from data.controller import Faculty, Speciality, Student, Teacher, Bell, Admin, Subject, TimeTable, Homework, Task, \
    SolvingHomework
from keyboards.inline.faculty_button.faculty_button import fac_choice
from keyboards.inline.type_button.type_button import type_choice
from keyboards.inline.type_button.type_callback import type_callback
from loader import dp, db_admin as db
from states.Dean import DeanState
from states.Student import StudentState
from states.Teacher import TeacherState
from utils.db_api.test_postgtes import query_results


@dp.message_handler(CommandHelp(), state=TeacherState.FreeState)
async def first_dean_free_function(message: types.Message, state: FSMContext):
    text = [
        'Список команд: ',
        '/help - Получить справку',
        '/see_bells - Просмотреть расписание звонков',
        '/see_admins - Просмотреть список админов',
        '/see_faculty - Просмотреть список факультетов',
        '/see_homework - Просмотреть все домашние задания',
        '/see_speciality - Просмотреть все специальности',
        '/see_timetable - Просмотреть расписание',
        '/see_student - Просмотреть список всех студентов',
        '/see_subject - Просмотреть список всех предметов',
        '/see_teacher - Просмотреть список всех преподавателей',
        '/see_specific_bell - Просмотреть время начала и конца конкретной пары',
        '/see_faculty_by_speciality - Посмотреть, к какому факультету относится какая специальность',
        '/see_homework_by_student - Посмотреть домашнее задание конкретного студента',
        '/rate_homework - поставить оценку за домашнее задание студенту',
        '/logout'

    ]
    await message.answer('\n'.join(text))


@dp.message_handler(Command('rate_homework'), state=TeacherState.FreeState)
async def logout_tacher(message: types.Message, state: FSMContext):
    logging.warning('Начало функции logout_admin')
    await message.answer('Вот список заданий, который вы должны проверить')
    my_solving = SolvingHomework()
    res = my_solving.read(name_of_teacher=message.from_user.full_name)
    for i in res:
        await message.answer(i)
    await message.answer('Какое задание вы хотите проверить?')
    await TeacherState.CheckHomework.set()


@dp.message_handler(state=TeacherState.CheckHomework)
async def logout_tacher(message: types.Message, state: FSMContext):
    logging.warning('Начало функции logout_admin')
    await message.answer('Какого студента?')
    my_global_dict['homework_to_rate'] = message.text
    await TeacherState.SecondCheckHomework.set()


@dp.message_handler(state=TeacherState.SecondCheckHomework)
async def logout_tacher(message: types.Message, state: FSMContext):
    my_global_dict['student_to_rate'] = message.text
    await message.answer('Какую оценку вы хотите поставить?')
    await TeacherState.ThirdCheckHomework.set()


@dp.message_handler(state=TeacherState.ThirdCheckHomework)
async def logout_tacher(message: types.Message, state: FSMContext):
    logging.warning('Начало функции logout_admin')
    rating = message.text
    if rating not in ('1', '2', '3', '4', '5'):
        await message.answer('Неверные данные. Оценка от 1 до 5')
    my_homework = Homework()
    data = {'homework_to_rate': my_global_dict['homework_to_rate'],
            'student_to_rate': my_global_dict['student_to_rate'],
            'rating': rating}
    res = my_homework.rate_homework(data)
    if res:
        await message.answer('Оценка поставлена')
        data = {'status': 'done',
                'name_of_homework': my_global_dict['homework_to_rate'],
                'name_of_student': my_global_dict['student_to_rate']
                }

        res = my_homework.update_status(data)
        if res:
            await message.answer('Статус дз изменен')
    await TeacherState.FreeState.set()


@dp.message_handler(Command('logout'), state=TeacherState.FreeState)
async def logout_tacher(message: types.Message, state: FSMContext):
    logging.warning('Начало функции logout_admin')
    my_teacher = Teacher()
    result = my_teacher.delete(name=message.from_user.full_name)
    if result:
        await message.answer('Вы успешно логаутнулись')
        await message.answer('Чтобы снова зарегестрироваться, пропишите команду /start')
        await state.reset_state()
    else:
        await message.answer('Произошла ошибка при логауте')


@dp.message_handler(Command('see_bells'), state=TeacherState.FreeState)
async def see_bells(message: types.Message, state: FSMContext):
    logging.warning('Начало функции see_bells')
    await message.answer('Выводим список звонков...')
    my_bell = Bell()
    list_of_bells = my_bell.read()
    logging.warning(f'Получен ответ от модуля Bells. list_of_bells = {list_of_bells}')
    for bell in list_of_bells:
        await message.answer(bell)
    logging.warning('Конец функции see_bells')


@dp.message_handler(Command('see_admins'), state=TeacherState.FreeState)
async def see_admins(message: types.Message, state: FSMContext):
    logging.warning('Начало функции see_admins')
    await message.answer('Выводим список админов...')
    my_admin = Admin()
    admins = my_admin.read()
    logging.warning(f'Получен ответ от модуля Admins. admins = {admins}')
    for admin in admins:
        await message.answer(admin)
    logging.warning('Конец функции see_admins')


@dp.message_handler(Command('see_faculty'), state=TeacherState.FreeState)
async def see_faculty(message: types.Message, state: FSMContext):
    logging.warning('Начало функции see_faculty')
    await message.answer('Выводим список факультетов...')
    my_faculty = Faculty()
    list_of_facultyes = my_faculty.read()
    logging.warning(f'Получен ответ от модуля Faculty. res = {list_of_facultyes}')
    for fac in list_of_facultyes:
        await message.answer(fac)


@dp.message_handler(Command('see_homework'), state=TeacherState.FreeState)
async def see_homework(message: types.Message, state: FSMContext):
    logging.warning('Начало функции see_homework')
    await message.answer('Выводим все домашние задания...')
    my_homework = Homework()
    list_of_homework = my_homework.read()
    for homework in list_of_homework:
        await message.answer(homework)
    # logging.warning(f'Получен ответ от модуля db. res = {res}')
    # await message.answer(res)
    # await message.answer("Тут будет выдача домашнего задания с предметом, фамилией студента, преподавателю")
    logging.warning('Конец функции see_homework')


@dp.message_handler(Command('see_speciality'), state=TeacherState.FreeState)
async def see_speciality(message: types.Message, state: FSMContext):
    logging.warning('Начало функции see_speciality')
    await message.answer('Выводим все специальности...')
    my_speciality = Speciality()
    list_of_speciality = my_speciality.read()
    if list_of_speciality == 'Empty':
        await message.answer('Список специальностей пуст')
    else:
        logging.warning(f'Получен ответ от модуля Speciality. list_of_speciality = {list_of_speciality}')
        for spec in list_of_speciality:
            await message.answer(spec)
        logging.warning('Конец функции see_speciality')


@dp.message_handler(Command('see_speciality'), state=TeacherState.FreeState)
async def see_speciality(message: types.Message, state: FSMContext):
    logging.warning('Начало функции see_speciality')
    await message.answer('Выводим все специальности...')
    my_speciality = Speciality()
    list_of_speciality = my_speciality.read()
    if list_of_speciality == 'Empty':
        await message.answer('Список специальностей пуст')
    else:
        logging.warning(f'Получен ответ от модуля Speciality. list_of_speciality = {list_of_speciality}')
        for spec in list_of_speciality:
            await message.answer(spec)
        logging.warning('Конец функции see_speciality')


@dp.message_handler(Command('see_timetable'), state=TeacherState.FreeState)
async def see_timetable_first(message: types.Message, state: FSMContext):
    logging.warning('Началась функция показа расписания')
    await see_speciality(message, state)
    await message.answer('Введите специальность, расписание которой вы хотите посмотреть')
    await TeacherState.SelectTimetable.set()


@dp.message_handler(state=TeacherState.SelectTimetable)
async def see_timetable_second(message: types.Message, state: FSMContext):
    name_of_speciality = message.text
    logging.warning(f'Название специальности, введенная пользователем: {name_of_speciality}')
    my_timetable = TimeTable()
    timetable_list = my_timetable.read(name_of_speciality)
    if timetable_list == 'Empty':
        await message.answer('Расписания по вашей  специальности нет')
    else:
        for timetable in timetable_list:
            await message.answer(timetable)
    await TeacherState.FreeState.set()


@dp.message_handler(Command('see_student'), state=TeacherState.FreeState)
async def see_student(message: types.Message, state: FSMContext):
    logging.warning('Начало функции see_student')
    await message.answer('Выводим всех студентов...')
    my_student = Student()
    list_of_student = my_student.read()
    res = db.get_students()
    logging.warning(f'Получен ответ от модуля Student. list_of_student = {list_of_student}')
    for student in list_of_student:
        await message.answer(student)
    logging.warning('Конец функции see_student')


@dp.message_handler(Command('see_subject'), state=TeacherState.FreeState)
async def see_subject(message: types.Message, state: FSMContext):
    logging.warning('Начало функции see_subject')
    await message.answer('Выводим все предметы...')
    my_subject = Subject()
    subjects = my_subject.read()
    logging.warning(f'Получен ответ от модуля db. res = {subjects}')
    for sub in subjects:
        await message.answer(sub)
    logging.warning('Конец функции see_subject')


@dp.message_handler(Command('see_teacher'), state=TeacherState.FreeState)
async def see_teacher(message: types.Message, state: FSMContext):
    logging.warning('Начало функции see_teacher')
    await message.answer('Выводим всех преподавателей...')
    my_teacher = Teacher()
    list_of_teacher = my_teacher.read()
    logging.warning(f'Получен ответ от модуля Teacher. res = {list_of_teacher}')
    for teacher in list_of_teacher:
        await message.answer(teacher)
    logging.warning('Конец функции see_teacher')


@dp.message_handler(Command('see_specific_bell'), state=TeacherState.FreeState)
async def select_custom_bell_first(message: types.Message, state: FSMContext):
    logging.warning('Начало функции see_specific_bell')
    await message.answer('Время какой пары вы хотите увидеть?')
    logging.warning('Пошел запрос пользователю на номер пары')
    await TeacherState.SelectBell.set()


@dp.message_handler(state=TeacherState.SelectBell)
async def select_custom_bell_second(message: types.Message, state: FSMContext):
    my_id = message.text
    logging.warning(f'Получен ответ от пользователя. Номер пары = {my_id}')
    try:
        my_bell = Bell()
        res = my_bell.read_by_id(my_id)
        logging.warning(f'Получен ответ от модуля Bell. res = {res}')
        await message.answer(res)
    except Exception as err:
        await message.answer(f'Ошибка = {err}')
    await TeacherState.FreeState.set()
    logging.warning('Конец функции see_specific_bell')


@dp.message_handler(Command('see_faculty_by_speciality'), state=TeacherState.FreeState)
async def get_faculty_by_spec_first(message: types.Message, state: FSMContext):
    logging.warning('Начало функции see_faculty_by_speciality')
    await see_speciality(message, state)
    await message.answer('Введите специальность, факультет которой вы хотите узнать')
    logging.warning('Пошел запрос пользователю на специальность, факультет которой вы хотите узнать')
    await TeacherState.FacBySpec.set()


@dp.message_handler(state=TeacherState.FacBySpec)
async def get_faculty_by_spec_first(message: types.Message, state: FSMContext):
    my_spec = message.text
    logging.warning(f'Получен ответ от пользователя. Специальность = {my_spec}')
    my_faculty = Faculty()
    res = my_faculty.read_by_speciality(my_spec)
    # res = db.get_facultyes_by_spec(my_spec)
    logging.warning(f'Получен ответ от модуля db. res = {res}')
    await message.answer(res)
    await TeacherState.FreeState.set()
    logging.warning('Конец функции see_faculty_by_speciality')


@dp.message_handler(Command('see_homework_by_student'), state=TeacherState.FreeState)
async def get_homework_by_student_first(message: types.Message, state: FSMContext):
    logging.warning('Начало функции see_homework_by_student')
    await see_student(message, state)
    await message.answer('Напишите имя студента, дз которого вы хотите получить')
    logging.warning('Пошел запрос пользователю на имя студента, дз которого вы хотите получить')
    await TeacherState.HomeworkByStudent.set()


@dp.message_handler(state=TeacherState.HomeworkByStudent)
async def get_homework_by_student_second(message: types.Message, state: FSMContext):
    my_student = message.text
    logging.warning(f'Получен ответ от пользователя. Студент = {my_student}')
    my_homework = Homework()
    res = my_homework.read_by_student(my_student)
    logging.warning(f'Получен ответ от модуля Homework. res = {res}')
    if not res:
        await message.answer('У заданного студента нет дз')
    for i in res:
        await message.answer(i)
    await TeacherState.FreeState.set()
    logging.warning('Конец функции see_homework_by_student')
