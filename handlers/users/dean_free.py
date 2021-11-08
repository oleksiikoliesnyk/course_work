import logging
from datetime import datetime

from aiogram import types
from aiogram.dispatcher import FSMContext
from aiogram.dispatcher.filters.builtin import CommandStart, Command, CommandHelp
from aiogram.types import CallbackQuery

from data.db_constant import facultys
from data.global_conf import my_global_dict
from data.model import Faculty, Speciality, Student, Teacher, Bell, Admin, Subject, TimeTable
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
        '/add_speciality_for_teacher - Добавить преподавателя на новую специальность',
        '/set_bells - Изменить расписание звонков',
        '/help - Получить справку',
        '/delete_teacher - Удалить преподавателя',
        '/delete_student - Удалить студента',
        '/delete_admin - Удалить админа',
        '/delete_fac - Удалить факультет',
        '/delete_subject - Удалить предмет',
        '/delete_speciality - Удалить специальность',
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
        '/set_new_admin - Добавить нового админа',
        '/set_new_fac - Добавить новый факультет',
        '/set_new_spec - Добавить новую специальность',
        '/set_student - Добавить нового студента',
        '/set_teacher - Добавить нового преподавателя',
        '/set_admin - Добавить нового админа'

    ]
    await message.answer('\n'.join(text))


@dp.message_handler(Command('add_subject'), state=DeanState.FreeState)
async def add_subject(message: types.Message, state: FSMContext):
    logging.warning('Начало функции add_subject')
    try:
        teacher, subject = message.get_args().split(' ')
        logging.warning(f'Получили аргументы. Учитель - {teacher}, предмет - {subject}')
        await message.answer(f'Добаляю преподавателю {teacher} предмет {subject}')
        data_to_save = {'teacher': teacher,
                        'subject': subject}
        my_subject = Subject()
        res = my_subject.write(data_to_save)
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


@dp.message_handler(Command('see_timetable'), state=DeanState.FreeState)
async def see_timetable_first(message: types.Message, state: FSMContext):
    logging.warning('Началась функция показа расписания')
    await message.answer('Введите специальность, расписание которой вы хотите посмотреть')
    await DeanState.SelectTimetable.set()


@dp.message_handler(state=DeanState.SelectTimetable)
async def see_timetable_first(message: types.Message, state: FSMContext):
    name_of_speciality = message.text
    logging.warning(f'Название специальности, введенная пользователем: {name_of_speciality}')
    my_timetable = TimeTable()
    timetable_list = my_timetable.read(name_of_speciality)
    for timetable in timetable_list:
        await message.answer(timetable)
    await DeanState.FreeState.set()


@dp.message_handler(Command('delete_subject'), state=DeanState.FreeState)
async def delete_subject(message: types.Message, state: FSMContext):
    logging.warning('Началась функция удаления предмета')
    await message.answer('Введите имя предмета, которого вы хотите удалить')
    await DeanState.DeleteSubject.set()


@dp.message_handler(state=DeanState.DeleteSubject)
async def delete_subject_second(message: types.Message, state: FSMContext):
    name = message.text
    logging.warning(f'Название предмета = {name}')
    my_subject = Subject()
    res = my_subject.delete(name)
    if res:
        await message.answer('Предмет был успешно удален')
    else:
        await message.answer('Предмет не был удален')
    logging.warning('Закончилась функция удаления предмета')
    await DeanState.FreeState.set()


@dp.message_handler(Command('delete_speciality'), state=DeanState.FreeState)
async def delete_speciality_first(message: types.Message, state: FSMContext):
    logging.warning('Началась функция удаления специальности')
    await message.answer('Введите имя специальности, которую вы хотите удалить')
    await DeanState.DeleteSpeciality.set()


@dp.message_handler(state=DeanState.DeleteSpeciality)
async def delete_subject_second(message: types.Message, state: FSMContext):
    name = message.text
    logging.warning(f'Название предмета = {name}')
    my_speciality = Speciality()
    res = my_speciality.delete(name)
    if res:
        await message.answer('Предмет был успешно удален')
    else:
        await message.answer('Предмет не был удален')
    logging.warning('Закончилась функция удаления предмета')
    await DeanState.FreeState.set()


@dp.message_handler(Command('delete_admin'), state=DeanState.FreeState)
async def delete_admin_first(message: types.Message, state: FSMContext):
    logging.warning('Началась функция удаления админа')
    await message.answer('Введите имя админа, которого вы хотите удалить')
    await DeanState.DeleteAdminFirst.set()


@dp.message_handler(state=DeanState.DeleteAdminFirst)
async def delete_admin_second(message: types.Message, state: FSMContext):
    admin_name = message.text
    my_admin = Admin()
    try:
        res = my_admin.delete(name=admin_name)
        if res:
            await message.answer('Админ был успешно удален!')
        else:
            await message.answer('Админ не был удален!')
    except Exception as err:
        await message.answer('Не удалось удалить админа!')
        await message.answer(f'Ошибка = {err}')
    await DeanState.FreeState.set()


@dp.message_handler(Command('set_admin'), state=DeanState.FreeState)
async def set_admin_first(message: types.Message, state: FSMContext):
    logging.warning('Начало функции set_admin')
    await message.answer('Введите имя админа: ')
    await DeanState.SetAdminFirst.set()


@dp.message_handler(state=DeanState.SetAdminFirst)
async def set_admin_second(message: types.Message, state: FSMContext):
    logging.warning(f'Получили имя админа от пользователя. Это - {message.text}')
    my_global_dict['new_admin_name'] = message.text
    await message.answer('Введите полное имя админа')
    await DeanState.SetAdminSecond.set()


@dp.message_handler(state=DeanState.SetAdminSecond)
async def set_admin_third(message: types.Message, state: FSMContext):
    logging.warning(f'Получили полное имя админа от пользователя. Это - {message.text}')
    my_global_dict['new_admin_fullname'] = message.text
    await message.answer('Введите пароль админа')
    await DeanState.SetAdminThird.set()


@dp.message_handler(state=DeanState.SetAdminThird)
async def set_admin_third(message: types.Message, state: FSMContext):
    logging.warning(f'Получили пароль админа от пользователя')
    data_to_save = {'name': my_global_dict['new_admin_name'],
                    'full_name': my_global_dict['new_admin_fullname'],
                    'password': message.text}
    my_admin = Admin()
    try:
        res = my_admin.write(data_to_save)
        if res:
            await message.answer('Админ успешно сохранен! ')
            logging.warning('Админ успешно сохранен!')
        else:
            await message.answer('Админ не был сохранен!')
    except Exception as err:
        await message.answer('Не удалось зарегестировать нового админа!\n'
                             f'Ошибка = {err}')
    logging.warning('Конец функции сохранения админа!')
    await DeanState.FreeState.set()


@dp.message_handler(Command('delete_fac'), state=DeanState.FreeState)
async def delete_fac_first(message: types.Message, state: FSMContext):
    logging.warning('Начало функции delete_fac')
    await message.answer('Введите имя факультета, которого вы хотите удалить')
    await DeanState.DeleteFaculty.set()


@dp.message_handler(state=DeanState.DeleteFaculty)
async def delete_fac_second(message: types.Message, state: FSMContext):
    name_faculty = message.text
    my_faculty = Faculty()
    try:
        res = my_faculty.delete(name_faculty)
        if res:
            await message.answer('Факультет удален успешно')
        else:
            await message.answer('Факультет не был удален')
    except Exception as err:
        await message.answer(f'Ошибка - {err}')
    await DeanState.FreeState.set()


@dp.message_handler(Command('delete_student'), state=DeanState.FreeState)
async def delete_student_first(message: types.Message, state: FSMContext):
    logging.warning('Начало функции delete_student')
    await message.answer('Введите имя студента, которого вы хотите удалить')
    await DeanState.DeleteStudent.set()


@dp.message_handler(state=DeanState.DeleteStudent)
async def delete_student_second(message: types.Message, state: FSMContext):
    try:
        student_name = message.text
        logging.warning(f'Имя студента = {student_name}')
        logging.warning(f'Получаю id по имени')
        my_student = Student()
        res = my_student.delete(student_name)
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
    try:
        first_time, second_time = message.text.split(' ')
        logging.warning(f'Получено время от пользователя. First_time = {first_time}, second_time = {second_time}')
        first_time = datetime.strptime(first_time, '%H:%M').time()
        second_time = datetime.strptime(second_time, '%H:%M').time()
        my_bell = Bell()
        data_to_save = {'id': my_global_dict['id_bell'],
                        'first_time': first_time,
                        'second_time': second_time}
        logging.warning(f'Время сконвертировано. First_time = {first_time}, second_time = {second_time}')
        res = my_bell.write(data_to_save)
        logging.warning(f'Получен ответ от модуля db. res = {res}')
        if res:
            await message.answer(f'Время на {my_global_dict["id_bell"]}-ой паре успешно выставлено')
            await message.answer(f'Время начала = {first_time}, время конца = {second_time}', )
            await DeanState.FreeState.set()
        logging.warning('Конец функции set_bells')
    except Exception as err:
        await message.answer(err)


@dp.message_handler(Command('delete_teacher'), state=DeanState.FreeState)
async def delete_teacher_first_step(message: types.Message, state: FSMContext):
    logging.warning('Начало функции delete_teacher')
    await message.answer('Какого преподавателя вы хотите удалить?')
    logging.warning('Запрос на имя преподавателя отправлен')
    await DeanState.DeleteTeacher.set()


@dp.message_handler(state=DeanState.DeleteTeacher)
async def delete_teacher_second_step(message: types.Message, state: FSMContext):
    teacher_name = message.text
    my_teacher = Teacher()
    logging.warning(f'Получено имя преподавателя от пользователя. Имя = {teacher_name}')
    res = my_teacher.delete(name=teacher_name)
    logging.warning(f'Получен ответ от модуля Teacher. res = {res}')
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
    my_bell = Bell()
    list_of_bells = my_bell.read()
    logging.warning(f'Получен ответ от модуля Bells. list_of_bells = {list_of_bells}')
    for bell in list_of_bells:
        await message.answer(bell)
    logging.warning('Конец функции see_bells')


@dp.message_handler(Command('see_admins'), state=DeanState.FreeState)
async def see_bells(message: types.Message, state: FSMContext):
    logging.warning('Начало функции see_admins')
    await message.answer('Выводим список деканов...')
    my_admin = Admin()
    admins = my_admin.read()
    logging.warning(f'Получен ответ от модуля Admins. admins = {admins}')
    for admin in admins:
        await message.answer(admin)
    logging.warning('Конец функции see_admins')


@dp.message_handler(Command('see_faculty'), state=DeanState.FreeState)
async def see_bells(message: types.Message, state: FSMContext):
    logging.warning('Начало функции see_faculty')
    await message.answer('Выводим список факультетов...')
    my_faculty = Faculty()
    list_of_facultyes = my_faculty.read()
    logging.warning(f'Получен ответ от модуля Faculty. res = {list_of_facultyes}')
    for fac in list_of_facultyes:
        await message.answer(fac)


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
    my_speciality = Speciality()
    list_of_speciality = my_speciality.read()
    logging.warning(f'Получен ответ от модуля Speciality. list_of_speciality = {list_of_speciality}')
    for spec in list_of_speciality:
        await message.answer(spec)
    logging.warning('Конец функции see_speciality')


@dp.message_handler(Command('see_student'), state=DeanState.FreeState)
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


@dp.message_handler(Command('see_subject'), state=DeanState.FreeState)
async def see_subject(message: types.Message, state: FSMContext):
    logging.warning('Начало функции see_subject')
    await message.answer('Выводим все предметы...')
    my_subject = Subject()
    subjects = my_subject.read()
    logging.warning(f'Получен ответ от модуля db. res = {subjects}')
    for sub in subjects:
        await message.answer(sub)
    logging.warning('Конец функции see_subject')


@dp.message_handler(Command('see_teacher'), state=DeanState.FreeState)
async def see_teacher(message: types.Message, state: FSMContext):
    logging.warning('Начало функции see_teacher')
    await message.answer('Выводим всех преподавателей...')
    my_teacher = Teacher()
    list_of_teacher = my_teacher.read()
    logging.warning(f'Получен ответ от модуля Teacher. res = {list_of_teacher}')
    for teacher in list_of_teacher:
        await message.answer(teacher)
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
    my_faculty = Faculty()
    res = my_faculty.write(name)
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
    my_speciality = Speciality()
    try:
        data_to_save = {'spec_name': my_global_dict['name_new_spec'],
                        'fac_name': my_global_dict['name_fac_for_new_spec']}
        res = my_speciality.write(data_to_save)
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
    my_student = Student()
    student_data = {"name": my_global_dict['name_new_student'],
                    "full_name": full_name,
                    "password": my_global_dict['password_new_student'],
                    "course": my_global_dict['course_new_student'],
                    "id_spec": my_global_dict['spec_new_student'] }
    try:
        logger_message = f"name = {my_global_dict['name_new_student']}, \n" \
                       f" 'full_name = {full_name}, \n" \
                       f" password = {my_global_dict['password_new_student']},\n " \
                       f" course = {my_global_dict['course_new_student']},\n " \
                       f" id_spec = {my_global_dict['spec_new_student']}' \n"
        logging.warning(logger_message)
        res = my_student.write(student_data)
        if res:
            await message.answer('Студент успешно создан')
        else:
            await message.answer('Не удалось создать студента')
    except Exception as err:
        await message.answer('Не удалось создать студента')
        await message.answer(f'Ошибка = {err}')
    await DeanState.FreeState.set()


@dp.message_handler(Command('set_teacher'), state=DeanState.FreeState)
async def set_new_teacher_first(message: types.Message, state: FSMContext):
    await message.answer('Введите имя преподавателя')
    await DeanState.SetTeacherFirst.set()


@dp.message_handler(state=DeanState.SetTeacherFirst)
async def set_new_teacher_second(message: types.Message, state: FSMContext):
    my_global_dict['name_new_teacher'] = message.text
    await message.answer('Введите пароль нового преподавателя')
    await DeanState.SetTeacherSecond.set()


@dp.message_handler(state=DeanState.SetTeacherSecond)
async def set_new_teacher_third(message: types.Message, state: FSMContext):
    my_global_dict['password_new_teacher'] = message.text
    await message.answer('Введите полное имя нового преподавателя')
    await DeanState.SetTeacherThird.set()


@dp.message_handler(state=DeanState.SetTeacherThird)
async def set_new_teacher_third(message: types.Message, state: FSMContext):
    full_name = message.text
    data_to_save_teacher = {'name': my_global_dict['name_new_teacher'],
                            'password': my_global_dict['password_new_teacher'],
                            'full_name': full_name}
    my_teacher = Teacher()
    try:
        res = my_teacher.write(data_to_save_teacher)
        if res:
            await message.answer('Преподаватель создан успешно')
        else:
            await message.answer('Преподаватель не был создан')
    except Exception as err:
        await message.answer('Ошибка! Преподаватель не создан')
        await message.answer(f'Ошибка = {err}')
    await DeanState.FreeState.set()
