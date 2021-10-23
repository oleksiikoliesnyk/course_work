import logging
from datetime import datetime

from aiogram import types
from aiogram.dispatcher import FSMContext
from aiogram.dispatcher.filters.builtin import CommandStart, Command, CommandHelp
from aiogram.types import CallbackQuery

from data.db_constant import facultys
from data.global_conf import my_global_dict
from keyboards.inline.faculty_button.faculty_button import fac_choice
from keyboards.inline.type_button.type_button import type_choice
from keyboards.inline.type_button.type_callback import type_callback
from loader import dp, db_admin as db
from states.Dean import DeanState
from utils.db_api.test_postgtes import query_results


@dp.message_handler(CommandHelp(), state=DeanState.FreeState)
async def first_dean_free_function(message: types.Message, state: FSMContext):
    text = [
        'Список команд: ',
        '/add_subject {ИмяПреподавателя} {НазваниеПредмета} - Добавить преподавателю новый предмет',
        '/set_bells - Изменить расписание звонков',
        '/help - Получить справку',
        '/delete_teacher - Удалить преподавателя',
        '/delete_student - Удалить студента'
        '/see_bells - Просмотреть расписание звонков',
        '/see_deans - Просмотреть список деканов',
        '/see_faculty - Просмотреть список факультетов',
        '/see_homework - Просмотреть все домашние задания',
        '/see_speciality - Просмотреть все специальности',
        '/see_student - Просмотреть список всех студентов',
        '/see_subject - Просмотреть список всех предметов',
        '/see_teacher - Просмотреть список всех преподавателей',
        '/see_specific_bell - Просмотреть время начала и конца конкретной пары',
        '/see_faculty_by_speciality - Посмотреть, к какому факультету относится какая специальность',
        '/see_homework_by_student - Посмотреть домашнее задание конкретного студента',
        '/set_new_dean - Добавить нового декана',
        '/set_new_fac - Добавить новый факультет',
        '/set_new_spec - Добавить новую специальность',
        '/set_student - Добавить нового студента',
        '/set_teacher - Добавить нового преподавателя'

    ]
    await message.answer('\n'.join(text))


@dp.message_handler(Command('add_subject'), state=DeanState.FreeState)
async def add_subject(message: types.Message, state: FSMContext):
    logging.warning('Начало функции add_subject')
    try:
        teacher, subject = message.get_args().split(' ')
        logging.warning(f'Получили аргументы. Учитель - {teacher}, предмет - {subject}')
        await message.answer(f'Добаляю преподавателю {teacher} предмет {subject}')
        res = db.set_subject(teacher=teacher,
                             subject=subject)
        logging.warning(f'Пришет ответ от модуля db. res = {res}')
        if isinstance(res, dict):  # если пришел в ответ словарь, значит какая-то ошибка
            await message.answer(f'Возникла проблема. А именно: {res["message"]}')
        elif res:
            await message.answer(f'Преподавателю {teacher} успешно добавлен предмет {subject}!')
    except ValueError as err:
        await message.answer(f'Ошибка - {err}')
        await message.answer('Вероятнее всего вы не указали аргументы - имя преподавателя и название предмета'
                             'через пробел')
    logging.warning('Конец функции add_subject')


@dp.message_handler(Command('delete_student'), state=DeanState.FreeState)
async def delete_student_first(message: types.Message, state: FSMContext):
    logging.warning('Начало функции delete_student')
    await message.answer('Введите имя студента, которого вы хотите удалить')
    await DeanState.DeleteStudent.set()


@dp.message_handler(state=DeanState.DeleteStudent)
async def delete_student_second(message: types.Message, state: FSMContext):
    student_name = message.text
    logging.warning(f'Имя студента = {student_name}')
    logging.warning(f'Получаю id по имени')
    try:
        id_student = db.get_student_id_by_name(name=student_name)
        if not id_student:
            await message.answer('Имя студента задано неправильно, введите команду еще раз')
            await DeanState.FreeState.set()
            raise ValueError('Неверно задано имя')
        logging.warning(f'id получено = {id_student}')
        logging.warning(f'Начинаем удалять...')
        res = db.delete_student(id=id_student)
        logging.warning(f'Функция базы отработала. Результат = {res}')
        if res:
            await message.answer('Студент успешно удален.')
            await DeanState.FreeState.set()
        else:
            await message.answer('Не удалось удалить студента.')
    except Exception as err:
        await message.answer('Не удалось удалить студента.')
        await message.answer(f'Ошибка = {err}.')
    logging.warning('Конец функции delete_student')


@dp.message_handler(Command('set_bells'), state=DeanState.FreeState)
async def change_bells(message: types.Message, state: FSMContext):
    logging.warning('Начало функции set_bells')
    await message.answer('Начинаем изменять расписание звонков!')
    await message.answer('К какой паре будем менять звонок?')
    logging.warning('Отправлен запрос на номер пары')
    await DeanState.ChangeBellFirst.set()


@dp.message_handler(state=DeanState.ChangeBellFirst)
async def true_change_bells_first(message: types.Message, state: FSMContext):
    id_bell = message.text
    logging.warning(f'Получен номер пары = {id_bell}')
    my_global_dict['id_bell'] = id_bell
    logging.warning(f'{id_bell} добавлена в словарь')
    await message.answer('Введите время начала и конца пары через пробел')
    logging.warning('Отправлен запрос на время начала и конца пары')
    await DeanState.ChangeBellSecond.set()


@dp.message_handler(state=DeanState.ChangeBellSecond)
async def true_change_bells_second(message: types.Message, state: FSMContext):
    first_time, second_time = message.text.split(' ')
    logging.warning(f'Получено время от пользователя. First_time = {first_time}, second_time = {second_time}')
    first_time = datetime.strptime(first_time, '%H:%M').time()
    second_time = datetime.strptime(second_time, '%H:%M').time()
    logging.warning(f'Время сконвертировано. First_time = {first_time}, second_time = {second_time}')
    res = db.set_bells(id=my_global_dict['id_bell'],
                       first_time=first_time,
                       second_time=second_time)
    logging.warning(f'Получен ответ от модуля db. res = {res}')
    if res:
        await message.answer(f'Время на {my_global_dict["id_bell"]}-ой паре успешно выставлено')
        await message.answer(f'Время начала = {first_time}, время конца = {second_time}', )
        await DeanState.FreeState.set()
    logging.warning('Конец функции set_bells')


@dp.message_handler(Command('delete_teacher'), state=DeanState.FreeState)
async def delete_teacher_first_step(message: types.Message, state: FSMContext):
    logging.warning('Начало функции delete_teacher')
    await message.answer('Какого преподавателя вы хотите удалить?')
    logging.warning('Запрос на имя преподавателя отправлен')
    await DeanState.DeleteTeacher.set()


@dp.message_handler(state=DeanState.DeleteTeacher)
async def delete_teacher_second_step(message: types.Message, state: FSMContext):
    teacher_name = message.text
    logging.warning(f'Получено имя преподавателя от пользователя. Имя = {teacher_name}')
    res = db.delete_teacher(name=teacher_name)
    logging.warning(f'Получен ответ от модуля db. res = {res}')
    if res:
        await message.answer('Преподаватель успешно удален!')
    else:
        await message.answer('Ошибка удаления! Имя преподавателя задано неверно')
    await DeanState.FreeState.set()
    logging.warning('Конец функции delete_teacher')


@dp.message_handler(Command('see_bells'), state=DeanState.FreeState)
async def see_bells(message: types.Message, state: FSMContext):
    logging.warning('Начало функции see_bells')
    await message.answer('Выводим список звонков...')
    res = db.get_bells()
    index_list = list(res.keys())
    index_list.sort()
    logging.warning(f'Получен ответ от модуля db. res = {res}')
    for i in index_list:
        await message.answer(f'{i}-ая пара. Начинается в {res[i][0]}. Заканчивается в {res[i][1]}')
    logging.warning('Конец функции see_bells')


@dp.message_handler(Command('see_deans'), state=DeanState.FreeState)
async def see_bells(message: types.Message, state: FSMContext):
    logging.warning('Начало функции see_deans')
    await message.answer('Выводим список деканов...')
    dict_deans = db.get_deans()
    logging.warning(f'Получен ответ от модуля db. dict_deans = {dict_deans}')
    for i in dict_deans:
        await message.answer(f'Имя декана: {dict_deans[i][0]}. Полное имя декана: {dict_deans[i][1]}')
    logging.warning('Конец функции see_deans')


@dp.message_handler(Command('see_faculty'), state=DeanState.FreeState)
async def see_bells(message: types.Message, state: FSMContext):
    logging.warning('Начало функции see_faculty')
    await message.answer('Выводим список факультетов...')
    res = db.get_facultyes()
    logging.warning(f'Получен ответ от модуля db. res = {res}')
    await message.answer(res)


@dp.message_handler(Command('see_homework'), state=DeanState.FreeState)
async def see_homework(message: types.Message, state: FSMContext):
    logging.warning('Начало функции see_homework')
    await message.answer('Выводим все домашние задания...')
    res = db.get_homework()
    logging.warning(f'Получен ответ от модуля db. res = {res}')
    await message.answer(res)
    await message.answer("Тут будет выдача домашнего задания с предметом, фамилией студента, преподавателю")
    logging.warning('Конец функции see_homework')


@dp.message_handler(Command('see_speciality'), state=DeanState.FreeState)
async def see_speciality(message: types.Message, state: FSMContext):
    logging.warning('Начало функции see_speciality')
    await message.answer('Выводим все специальности...')
    res = db.get_speciality()
    logging.warning(f'Получен ответ от модуля db. res = {res}')
    await message.answer(res)
    logging.warning('Конец функции see_speciality')


@dp.message_handler(Command('see_student'), state=DeanState.FreeState)
async def see_student(message: types.Message, state: FSMContext):
    logging.warning('Начало функции see_student')
    await message.answer('Выводим всех студентов...')
    res = db.get_students()
    logging.warning(f'Получен ответ от модуля db. res = {res}')
    for r in res:
        await message.answer(r)
    logging.warning('Конец функции see_student')


@dp.message_handler(Command('see_subject'), state=DeanState.FreeState)
async def see_subject(message: types.Message, state: FSMContext):
    logging.warning('Начало функции see_subject')
    await message.answer('Выводим все предметы...')
    res = db.get_subjects()
    logging.warning(f'Получен ответ от модуля db. res = {res}')
    await message.answer(res)
    logging.warning('Конец функции see_subject')


@dp.message_handler(Command('see_teacher'), state=DeanState.FreeState)
async def see_teacher(message: types.Message, state: FSMContext):
    logging.warning('Начало функции see_teacher')
    await message.answer('Выводим всех преподавателей...')
    res = db.get_teachers()
    logging.warning(f'Получен ответ от модуля db. res = {res}')
    for r in res:
        await message.answer(r)
    logging.warning('Конец функции see_teacher')


@dp.message_handler(Command('see_specific_bell'), state=DeanState.FreeState)
async def select_custom_bell_first(message: types.Message, state: FSMContext):
    logging.warning('Начало функции see_specific_bell')
    await message.answer('Время какой пары вы хотите увидеть?')
    logging.warning('Пошел запрос пользователю на номер пары')
    await DeanState.SelectBell.set()


@dp.message_handler(state=DeanState.SelectBell)
async def select_custom_bell_second(message: types.Message, state: FSMContext):
    my_id = message.text
    logging.warning(f'Получен ответ от пользователя. Номер пары = {my_id}')
    res = db.get_bells_by_id(my_id)
    logging.warning(f'Получен ответ от модуля db. res = {res}')
    await message.answer(f'Время начала {my_id}-ой пары: {res[0][1]}. Время конца: {res[0][2]}')
    await DeanState.FreeState.set()
    logging.warning('Конец функции see_specific_bell')


@dp.message_handler(Command('see_faculty_by_speciality'), state=DeanState.FreeState)
async def get_faculty_by_spec_first(message: types.Message, state: FSMContext):
    logging.warning('Начало функции see_faculty_by_speciality')
    await message.answer('Введите специальность, факультет которой вы хотите узнать')
    logging.warning('Пошел запрос пользователю на специальность, факультет которой вы хотите узнать')
    await DeanState.FacBySpec.set()


@dp.message_handler(state=DeanState.FacBySpec)
async def get_faculty_by_spec_first(message: types.Message, state: FSMContext):
    my_spec = message.text
    logging.warning(f'Получен ответ от пользователя. Специальность = {my_spec}')
    res = db.get_facultyes_by_spec(my_spec)
    logging.warning(f'Получен ответ от модуля db. res = {res}')
    await message.answer(res)
    await DeanState.FreeState.set()
    logging.warning('Конец функции see_faculty_by_speciality')


@dp.message_handler(Command('see_homework_by_student'), state=DeanState.FreeState)
async def get_homework_by_student_first(message: types.Message, state: FSMContext):
    logging.warning('Начало функции see_homework_by_student')
    await message.answer('Напишите имя студента, дз которого вы хотите получить')
    logging.warning('Пошел запрос пользователю на имя студента, дз которого вы хотите получить')
    await DeanState.HomeworkByStudent.set()


@dp.message_handler(state=DeanState.HomeworkByStudent)
async def get_homework_by_student_second(message: types.Message, state: FSMContext):
    my_student = message.text
    logging.warning(f'Получен ответ от пользователя. Студент = {my_student}')
    res = db.get_homework_by_student(my_student)
    logging.warning(f'Получен ответ от модуля db. res = {res}')
    await message.answer(res)
    await DeanState.FreeState.set()
    logging.warning('Конец функции see_homework_by_student')


@dp.message_handler(Command('set_new_dean'), state=DeanState.FreeState)
async def set_dean_first(message: types.Message, state: FSMContext):
    logging.warning('Начало функции set_new_dean')
    await message.answer('Введите имя нового декана')
    logging.warning('Пошел запрос пользователю на имя нового декана')
    await DeanState.SetDeanName.set()


@dp.message_handler(state=DeanState.SetDeanName)
async def set_dean_second(message: types.Message, state: FSMContext):
    my_global_dict['dean_name'] = message.text
    logging.warning(f'Получен ответ от пользователя. Декан = {my_global_dict["dean_name"]}')
    await message.answer('Введите пароль нового декана')
    logging.warning('Пошел запрос пользователю на пароль нового декана')
    await DeanState.SetDeanPassword.set()


@dp.message_handler(state=DeanState.SetDeanPassword)
async def set_dean_finally(message: types.Message, state: FSMContext):
    my_global_dict['dean_password'] = message.text
    logging.warning(f'Получен ответ от пользователя. Пароль = {my_global_dict["dean_password"]}')
    res = db.set_dean(name=my_global_dict['dean_name'],
                      password=my_global_dict['dean_password'])
    if res:
        await message.answer('Декан успешно задан')
    else:
        await message.answer('Возникла проблема, декан не задан')
    await DeanState.FreeState.set()


@dp.message_handler(Command('set_new_fac'), state=DeanState.FreeState)
async def set_fac_first(message: types.Message, state: FSMContext):
    await message.answer('Введите название факультета')
    await DeanState.SetFac.set()


@dp.message_handler(state=DeanState.SetFac)
async def set_fac_finally(message: types.Message, state: FSMContext):
    name = message.text
    res = db.create_fac(name)
    if res:
        await message.answer('Факультет успешно создан')
    else:
        await message.answer('Факультет не создан, возникла ошибка')
    await DeanState.FreeState.set()


@dp.message_handler(Command('set_new_spec'), state=DeanState.FreeState)
async def set_spec_first(message: types.Message, state: FSMContext):
    await message.answer('Введите название специальности')
    await DeanState.SetSpecFirst.set()


@dp.message_handler(state=DeanState.SetSpecFirst)
async def set_spec_second(message: types.Message, state: FSMContext):
    my_global_dict['name_new_spec'] = message.text
    await message.answer('Введите название факультета, к которому относится специальность')
    await DeanState.SetSpecSecond.set()


@dp.message_handler(state=DeanState.SetSpecSecond)
async def set_spec_third(message: types.Message, state: FSMContext):
    my_global_dict['name_fac_for_new_spec'] = message.text
    try:
        id_fac = db.get_id_fac_by_name(my_global_dict['name_fac_for_new_spec'])
        res = db.set_spec(name=my_global_dict['name_new_spec'],
                          id_fac=id_fac)
        if res:
            await message.answer('Специальность задана успешно')
        else:
            await message.answer('Специальность не была добавлена')
        await DeanState.FreeState.set()
    except Exception as err:
        await message.answer('Введено неправильное название факультета, операция завершена')
        await DeanState.FreeState.set()


@dp.message_handler(Command('set_student'), state=DeanState.FreeState)
async def set_new_student_first(message: types.Message, state: FSMContext):
    await message.answer('Введите имя студента')
    await DeanState.SetStudentFirst.set()


@dp.message_handler(state=DeanState.SetStudentFirst)
async def set_new_student_second(message: types.Message, state: FSMContext):
    my_global_dict['name_new_student'] = message.text
    await message.answer('Введите пароль студента')
    await DeanState.SetStudentSecond.set()


@dp.message_handler(state=DeanState.SetStudentSecond)
async def set_new_student_third(message: types.Message, state: FSMContext):
    my_global_dict['password_new_student'] = message.text
    await message.answer('Введите курс студента')
    await DeanState.SetStudentThird.set()


@dp.message_handler(state=DeanState.SetStudentThird)
async def set_new_student_third(message: types.Message, state: FSMContext):
    my_global_dict['course_new_student'] = message.text
    await message.answer('Введите специальность студента')
    await DeanState.SetStudentFourth.set()


@dp.message_handler(state=DeanState.SetStudentFourth)
async def set_full_name_of_student(message: types.Message, state: FSMContext):
    my_global_dict['name_spec_student'] = message.text

    try:
        id_spec = db.get_specialization_by_name(my_global_dict['name_spec_student'])
        my_global_dict['spec_new_student'] = id_spec
    except Exception as err:
        await message.answer(f'Ошибка - {err}')
        await message.answer('Скорее всего, вы неверно ввели название специальности')

    await message.answer('Введите полное имя студента')
    await DeanState.SetStudentFifth.set()


@dp.message_handler(state=DeanState.SetStudentFifth)
async def set_new_student_third(message: types.Message, state: FSMContext):
    full_name = message.text
    try:
        print_string = f"name = {my_global_dict['name_new_student']}, " \
                       f" 'full_name = {full_name}, " \
                       f" password = {my_global_dict['password_new_student']}, " \
                       f" course = {my_global_dict['course_new_student']}, " \
                       f" id_spec = {my_global_dict['spec_new_student']}' "
        print(print_string)

        res = db.save_student(name=my_global_dict['name_new_student'],
                              full_name=full_name,
                              password=my_global_dict['password_new_student'],
                              course=my_global_dict['course_new_student'],
                              id_spec=my_global_dict['spec_new_student'])
        if res:
            await message.answer('Студент успешно создан')
        else:
            await message.answer('Не удалось создать студента')
    except Exception as err:
        await message.answer('Не удалось создать студента')
        await message.answer(f'Ошибка = {err}')
    await DeanState.FreeState.set()


@dp.message_handler(Command('set_teacher'), state=DeanState.FreeState)
async def set_new_student_first(message: types.Message, state: FSMContext):
    await message.answer('Введите имя преподавателя')
    await DeanState.SetTeacherFirst.set()


@dp.message_handler(state=DeanState.SetTeacherFirst)
async def set_new_student_third(message: types.Message, state: FSMContext):
    my_global_dict['name_new_teacher'] = message.text
    await message.answer('Введите пароль нового преподавателя')
    await DeanState.SetTeacherSecond.set()


@dp.message_handler(state=DeanState.SetTeacherSecond)
async def set_new_student_third(message: types.Message, state: FSMContext):
    password = message.text
    try:
        res = db.set_new_teacher(name=my_global_dict['name_new_teacher'],
                                 password=password)
        if res:
            await message.answer('Преподаватель создан успешно')
        else:
            await message.answer('Преподаватель не был создан')
    except Exception as err:
        await message.answer('Ошибка! Преподаватель не создан')
        await message.answer(f'Ошибка = {err}')
