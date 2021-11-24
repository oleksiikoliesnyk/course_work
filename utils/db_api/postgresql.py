import logging
from pprint import pprint

import psycopg2

from data.global_conf import COUNT_OF_COURSES


class BaseDatabase:
    def __init__(self):
        self.low_db = BaseLowDatabase()

    def get_homework_by_student(self, my_student):
        res = self.low_db.select_homework_by_student(my_student)
        res_list = list()
        for i in res:
            res_string = f'Текст домашнего задания = {i[0]},\n' \
                         f'Дополнение к домашнему заданию = {i[1]},\n' \
                         f'Текущий статус задачи = {i[2]}'
            res_list.append(res_string)
        return res_list

    def get_students(self):
        students = self.low_db.select_student()
        res = []
        for student in students:
            res_string = f'Ник студента: {student[0]}, \n' \
                         f'Полное имя студента: {student[1]}, \n' \
                         f'Курс студента: {student[2]}, \n' \
                         f'Специальность студента: {student[3]}, \n'
            res.append(res_string)
        return res

    def get_teachers(self):
        teachers = self.low_db.select_teachers()
        res = list()
        for teacher in teachers:
            print(teacher[0])
            print(teacher[1])
            print(teacher[2])
            if teacher[2]:
                res_string = f'Ник преподавателя: {teacher[0]} \n' \
                             f'Полное имя преподавателя: {teacher[1]} \n' \
                             f'Специальности, на которых читает: {teacher[2]}'
            else:
                res_string = f'Ник преподавателя: {teacher[0]} \n' \
                             f'Полное имя преподавателя: {teacher[1]} \n' \
                             f'Не читает ни на каких специальностях'
            res.append(res_string)
        return res

    def get_admins(self):
        res = list()
        admins = self.low_db.select_admins()
        for admin in admins:
            if admin[1] !='None':
                res_string = f'Полное имя админа: {admin[1]} \n' \
                             f'Ник админа: {admin[2]}'
            else:
                res_string = f'Ник админа: {admin[2]} \n' \
                             f'Полное имя отсутствует'
            res.append(res_string)
        return res

    def get_bells(self):
        bells = self.low_db.select_bells()
        res = list()
        for bell in bells:
            res_string = f'Пара номер {bell[0]},\n' \
                         f'Время начала пары: {bell[1]},\n' \
                         f'Время конца пары: {bell[2]}'
            res.append(res_string)
        return res

    def get_timetable(self, speciality):
        all_timetable = self.low_db.select_timetable(speciality)
        if not all_timetable:
            return 'Empty'
        res = list()
        for timetable in all_timetable:
            res_string = f'День недели = {timetable[0]},\n' \
                         f'Курс = {timetable[1]},\n' \
                         f'Номер пары = {timetable[2]}, \n' \
                         f'Специальность = {timetable[3]},\n' \
                         f'Название предмета = {timetable[4]}'
            res.append(res_string)
        return res

    def get_faculty(self):
        raw_res = self.low_db.select_facultyes()
        res = raw_res  # Тут будет обработка
        return '1, 2, 3'

    def get_speciality(self):
        specialityes = self.low_db.select_specialization()
        if not specialityes:
            return 'Empty'
        res = list()
        for spec in specialityes:
            res_string = f'Специальность:  {spec[0]} \n' \
                         f'Факультет:  {spec[1]}'
            res.append(res_string)
        return res

    def get_homework(self):
        raw_res = self.low_db.select_homework()
        res = raw_res
        return res

    def get_id_teacher_by_name(self, name):
        first_id = self.low_db.select_id_teacher_by_name(name)[0][0]
        return first_id

    def exist_bell_by_id(self, id):
        res = self.low_db.get_bell_by_id(id)
        if res:
            return True
        else:
            return False

    def get_subject(self):
        result = list()
        subjects = self.low_db.select_subject()
        for sub in subjects:
            res_string = f'Предмет: {sub[0]},\n' \
                         f'Преподаватель, который ведет: {sub[1]}'
            result.append(res_string)
        return result

        res = raw_res
        return res

    def get_student_names(self):
        # raw_res = self.low_db.select_student(names=True)
        # res = [i[1] for i in raw_res]
        # res = ', '.join(res)
        return 1

    def get_specialization_by_name(self, name):
        print(f'name = {name}')
        res_id = self.low_db.select_id_spec_by_name(name)
        print(res_id)
        res_id = res_id[0][0]
        print(res_id)
        return res_id

    def get_student_id_by_name(self, name):
        res = self.low_db.select_id_student_by_name(name)
        print(res)
        if res:
            id_res = res[0][0]
            print(id_res)
            return id_res
        else:
            return False

    def get_facultyes(self):
        res = list()
        facultyes = self.low_db.select_facultyes()
        for fac in facultyes:
            res_string = f'{fac[0]}'
            res.append(res_string)
        print(res)
        # print(raw_res[0][1])
        # res = [i[1] for i in raw_res]
        # res = ', '.join(res)
        return res

    def get_user_by_credentionals(self, password, full_name, username):
        students = self.low_db.select_student_by_cred(password=password,
                                                      full_name=full_name,
                                                      name=username)
        deans = self.low_db.select_admin_by_cred(password=password,
                                                 full_name=full_name,
                                                 name=username)
        teacher = self.low_db.select_teacher_by_cred(password=password,
                                                     full_name=full_name,
                                                     name=username)
        print(students)
        print(deans)
        print(teacher)
        if students:
            return list(students[0]), 'student'
        elif deans:
            return list(deans[0]), 'dean'
        elif teacher:
            return list(teacher[0]), 'teacher'
        else:
            return False, False

    def get_id_fac_by_name(self, name):
        res = self.low_db.select_id_fac_by_name(name)
        if res:
            return res[0][0]

    def get_id_timetable_by_cred(self, speciality, day, bell_id):
        res = self.low_db.select_id_timetable(speciality, day, bell_id)[0][0]
        return res

    def get_bells_by_id(self, my_id):
        res = self.low_db.select_bells_by_id(my_id)[0]
        res_string = f'Пара номер = {res[0]},\n' \
                     f'Время начала = {res[1]},\n' \
                     f'Время конца = {res[2]}'
        return res_string

    def get_facultyes_by_spec(self, my_spec):
        my_fac = self.low_db.select_fac_by_spec(my_spec)
        res_string = f'Факультет по специальности {my_spec} = {my_fac[0][0]}'
        return res_string


class DatabaseForAdmin(BaseDatabase):

    def __init__(self):
        self.low_db = LowDatabaseForAdmin()

    def save_teacher(self, full_name, name, password):
        res = self.low_db.insert_teacher(full_name=full_name,
                                         name=name,
                                         password=password)
        return res

    def save_student(self, full_name, password, name, id_spec, course):
        res = self.low_db.insert_student(full_name=full_name,
                                         password=password,
                                         name=name,
                                         id_spec=id_spec,
                                         course=course)
        return res

    def save_admin(self, name, password, full_name):
        res = self.low_db.insert_admin(name=name,
                                       password=password,
                                       full_name=full_name)
        return res

    def _check_for_update_timetable(self, bell, subject, specialization, day_of_week, course):
        old_timetables = self.low_db.select_timetable(specialization)
        my_dict = dict()
        my_dict['day'] = list()
        my_dict['course'] = list()
        my_dict['bell'] = list()
        my_dict['speciality'] = list()
        my_dict['subject'] = list()
        for timetable in old_timetables:
            my_dict['day'].append(timetable[0])
            my_dict['course'].append(timetable[1])
            my_dict['bell'].append(timetable[2])
            my_dict['speciality'].append(timetable[3])
            my_dict['subject'].append(timetable[4])
        print(f'SPECIALIZATION = {specialization}')
        pprint(f'MY_DICT SPECIALIZATION = {my_dict["speciality"]}')
        print(f"specialization in my_dict['speciality'] = {specialization in my_dict['speciality']}")
        print('*******************************************************************************************')
        print(f'BELL = {bell}')
        pprint(f'MY_DICT BELL = {my_dict["bell"]}')
        print(f"BELL in my_dict['bell'] = {bell in my_dict['bell']}")
        print('*******************************************************************************************')
        print(f'subject  = {subject }')
        pprint(f'my_dict["subject"] = {my_dict["subject"]}')
        print(f"subject in my_dict['subject'] = {subject in my_dict['subject']}")
        print('*******************************************************************************************')
        print(f'day_of_week  = {day_of_week}')
        pprint(f'my_dict["day"] = {my_dict["day"]}')
        print(f"day_of_week in my_dict['day'] = {day_of_week in my_dict['day']}")
        print('*******************************************************************************************')
        print(f'course  = {course}')
        print(f'type(course) = {type(course)}')
        print(f'type(my_dict["course"][0] = {type(my_dict["course"][0])}')
        pprint(f'my_dict["course"] = {my_dict["course"]}')
        print(f"course in my_dict['course'] = {course in my_dict['course']}")
        if specialization in my_dict['speciality'] and bell in my_dict['bell'] and subject in my_dict['subject'] and day_of_week in my_dict['day'] and int(course) in my_dict['course']:
            if my_dict['speciality'].index(specialization)==my_dict['bell'].index(bell)==my_dict['subject'].index(subject)==my_dict['day'].index(day_of_week)==my_dict['course'].index(course):
                return True
        else:
            return False

    def save_timetable(self, bell, subject, specialization, day_of_week, course):
        subject_id = self.low_db.select_subjectid_by_name(subject)[0][0]
        specialization_id = self.low_db.select_specializationid_by_name(specialization)[0][0]
        #is_update = self._check_for_update_timetable(bell, subject, specialization, day_of_week, course)
        #todo: сделать проверку,  что может он не добавляет, а изменяет расписание!
        #if is_update:
        res = self.low_db.insert_timetable(bell, subject_id, specialization_id, day_of_week, course)
        #else:
        #    timetable_id = self.get_id_timetable_by_cred(speciality=specialization_id,
        #                                                 bell_id=bell,
        #                                                 day=day_of_week)
        #    res = self.low_db.update_timetable(timetable_id, bell, subject_id, specialization_id, day_of_week, course)
        return res

    def save_subject(self, subject, teacher):
        my_id = self.get_id_teacher_by_name(name=teacher)
        if my_id:
            self.low_db.insert_subject(subject=subject,
                                       teacher=my_id)
            return True
        else:
            return {'message': 'Преподаватель введен некорректно'}

    def save_bell(self, id, first_time, second_time):
        flag = self.exist_bell_by_id(id)
        if flag:
            self.low_db.update_bell(id=id,
                                    first_time=first_time,
                                    second_time=second_time)
        else:
            self.low_db.insert_bell(first_time=first_time,
                                    second_time=second_time)
        return True

    def save_faculty(self, name):
        res = self.low_db.insert_faculty(name)
        return res

    def save_specialization(self, name, fac_id):
        res = self.low_db.insert_specialization(name=name,
                                                id=fac_id)
        if res:
            id = self.low_db.select_specializationid_by_name(name)[0][0]
            for i in range(COUNT_OF_COURSES):
                res &= self.low_db.insert_course_spec(id, course=i+1)
        return res

    def delete_student(self, id):
        res = self.low_db.delete_student(id)
        return res

    def delete_subject(self, name):
        res = self.low_db.delete_subject(name)
        return res

    def delete_admin(self, name):
        res = self.low_db.delete_admin(name)
        return res

    def delete_teacher(self, name):
        res = self.low_db.delete_teacher_by_name(name)
        return res

    def delete_faculty(self, name):
        res = self.low_db.delete_fac_by_name(name)
        return res

    def delete_speciality(self, id):
        id_spec = self.low_db.select_id_spec_by_name(id)[0][0]
        res = self.low_db.delete_speciality(id)
        res &= self.low_db.delete_course_spec(id_spec)
        return res

    def delete_timetable(self, speciality, day, bell_id):
        spec_id = self.low_db.select_id_spec_by_name(speciality)[-1][0]
        timetable_id = self.get_id_timetable_by_cred(speciality=spec_id,
                                                    day=day,
                                                    bell_id=bell_id)
        res = self.low_db.delete_timetable(timetable_id)
        return res


class DatabaseForTeacher(BaseDatabase):
    def __init__(self):
        self.low_db = LowDatabaseForTeacher()


class DatabaseForStudent(BaseDatabase):
    def __init__(self):
        self.low_db = LowDatabaseForStudent()


class BaseLowDatabase:
    def __init__(self):
        self.conn = psycopg2.connect(host="localhost",  # Стандартный вход под дефолтным пользователем постгреса
                                     port=5432,
                                     database="University",
                                     user="postgres",
                                     password="i183")

    def select_teachers(self):
        with self.conn.cursor() as cur:
            sql = "Select t.name, t.full_name, string_agg(spc.name, ', ') " \
                  'from teacher t ' \
                  'left join specialitytoteacher stt on stt.id_teacher = t.id ' \
                  'left join speciality spc on spc.id = stt.id_speciality ' \
                  'where t.is_delete <>TRUE ' \
                  'group by t.name, t.full_name;'
            cur.execute(sql)
            query_results = cur.fetchall()
            print(query_results)
            return query_results

    def select_admins(self):
        with self.conn.cursor() as cur:
            sql = 'Select * ' \
                  'from admin a ' \
                  'where a.is_delete <> TRUE;'
            cur.execute(sql)
            query_results = cur.fetchall()
            return query_results

    def select_bells(self):
        with self.conn.cursor() as cur:
            sql = 'Select * from bell;'
            cur.execute(sql)
            query_results = cur.fetchall()
            return query_results

    def select_facultyes(self):
        with self.conn.cursor() as cur:
            sql = 'Select f.name ' \
                  'from faculty f ' \
                  'where f.is_delete <> TRUE '
            cur.execute(sql)
            query_results = cur.fetchall()
            return query_results

    def select_specialization(self):
        with self.conn.cursor() as cur:
            sql = 'select s.name, f.name ' \
                  'from speciality s ' \
                  'inner join faculty f on f.id = s.id_fac ' \
                  'where s.is_delete <> TRUE ; '
            cur.execute(sql)
            query_results = cur.fetchall()
            return query_results

    def select_student(self, names=None):
        with self.conn.cursor() as cur:
            if names:
                sql = 'Select * from student'
            else:
                sql = 'select s.name, s.full_name, s.course, spc.name ' \
                      'from student s ' \
                      'inner join speciality spc on spc.id = s.id_spec ' \
                      'where s.is_delete<>TRUE'
            cur.execute(sql)
            query_results = cur.fetchall()
            return query_results

    def select_homework(self):
        with self.conn.cursor() as cur:
            sql = 'select h.status as "Статус задания", s.name as "Название предмета", std.username as "Имя студента", ' \
                  't.task as "Название задачи", t.addition as "Условие задачи" ' \
                  'from homework h ' \
                  'inner join subject s on s.id = h.id_subject ' \
                  'inner join student std on std.id = h.id_student ' \
                  'inner join task t on t.id = h.task_id;'
            cur.execute(sql)
            query_results = cur.fetchall()
            return query_results

    def select_id_teacher_by_name(self, name):
        with self.conn.cursor() as cur:
            sql = 'Select * from teacher ' \
                  f"where name = '{name}' or full_name = '{name}'"
            cur.execute(sql)
            query_results = cur.fetchall()
            return query_results

    def select_bell_by_id(self, id):
        with self.conn.cursor() as cur:
            sql = 'Select * from bell ' \
                  f"where id = {id}"
            cur.execute(sql)
            query_results = cur.fetchall()
            return query_results

    def select_subject(self):
        with self.conn.cursor() as cur:
            sql = 'Select s.name, t.full_name ' \
                  'from subject s ' \
                  'inner join teacher t on t.id = s.teacher_id ' \
                  'where s.is_delete<>TRUE'
            cur.execute(sql)
            query_results = cur.fetchall()
            return query_results

    def select_id_fac_by_name(self, name_fac):
        with self.conn.cursor() as cur:
            sql = 'Select f.id from faculty f ' \
                  f"where f.name = '{name_fac}' and is_delete<>TRUE ;"
            cur.execute(sql)
            query_results = cur.fetchall()
            return query_results

    def select_teacher_by_cred(self, name, full_name, password):
        try:
            with self.conn.cursor() as cur:
                sql = 'Select * from teacher ' \
                      f"where name = '{name}' and full_name = '{full_name}' and password = '{password}'"
                cur.execute(sql)
                query_results = cur.fetchall()
        except Exception as err:
            logging.error('Error in select_teacher_by_cred')
            logging.error(err)
            return False
        return query_results

    def select_student_by_cred(self, name, full_name, password):
        try:
            with self.conn.cursor() as cur:
                sql = 'Select * from student ' \
                      f"where name = '{name}' and full_name = '{full_name}' and password = '{password}'"
                cur.execute(sql)
                query_results = cur.fetchall()
        except Exception as err:
            logging.error('Error in select_student_by_cred')
            logging.error(err)
            return False
        return query_results

    def select_admin_by_cred(self, name, full_name, password):
        try:
            with self.conn.cursor() as cur:
                sql = 'Select * from admin ' \
                      f"where name = '{name}' and full_name = '{full_name}' and password = '{password}'"
                cur.execute(sql)
                query_results = cur.fetchall()
        except Exception as err:
            logging.error('Error in select_admin_by_cred')
            logging.error(err)
            return False
        return query_results

    def select_id_student_by_name(self, name):
        with self.conn.cursor() as cur:
            sql = 'Select s.id from student s ' \
                  f"where name = '{name}' or full_name = '{name}'"
            cur.execute(sql)
            query_results = cur.fetchall()
            return query_results

    def select_id_spec_by_name(self, name):
        with self.conn.cursor() as cur:
            sql = 'Select s.id from speciality s ' \
                  f"where name = '{name}'"
            cur.execute(sql)
            query_results = cur.fetchall()
            return query_results

    def get_bell_by_id(self, id):
        with self.conn.cursor() as cur:
            sql = 'Select * from bell ' \
                  f"where id = '{id}'"
            cur.execute(sql)
            query_results = cur.fetchall()
            return query_results

    def select_timetable(self, speciality):
        with self.conn.cursor() as cur:
            sql = 'Select t.day_of_week, t.course, t.bell_id, s.name, sbj.name ' \
                  ' from timetable t ' \
                  'inner join speciality s on s.id = t.specialization_id ' \
                  'inner join subject sbj on sbj.id = t.id_subject ' \
                  f"where s.name = '{speciality}' and s.is_delete<>TRUE "
            cur.execute(sql)
            query_results = cur.fetchall()
            return query_results

    def select_subjectid_by_name(self, subject):
        with self.conn.cursor() as cur:
            sql = 'Select s.id ' \
                  'from subject s ' \
                  f"where s.name = '{subject}' and s.is_delete<>TRUE "
            cur.execute(sql)
            query_results = cur.fetchall()
            return query_results

    def select_specializationid_by_name(self, specialization):
        with self.conn.cursor() as cur:
            sql = 'Select s.id ' \
                  'from speciality s ' \
                  f"where s.name = '{specialization}' and s.is_delete<>TRUE "
            cur.execute(sql)
            query_results = cur.fetchall()
            return query_results

    def select_id_timetable(self, speciality, day, bell_id):
        with self.conn.cursor() as cur:
            sql = 'Select t.id ' \
                  'from timetable t ' \
                  f"where t.specialization_id = '{speciality}' and t.day_of_week = '{day}' and t.bell_id = {bell_id} and t.is_delete<>TRUE "
            cur.execute(sql)
            query_results = cur.fetchall()
            return query_results

    def select_bells_by_id(self, my_id):
        try:
            with self.conn.cursor() as cur:
                sql = 'Select * from bell b ' \
                      f"where b.id = '{my_id}';"
                cur.execute(sql)
                query_results = cur.fetchall()
        except Exception as err:
            logging.error('Error in select_teacher_by_cred')
            logging.error(err)
            return False
        return query_results

    def select_fac_by_spec(self, my_spec):
        try:
            with self.conn.cursor() as cur:
                sql = 'select f.name from speciality s ' \
                      'inner join faculty f on f.id = s.id_fac ' \
                      f"where s.name='{my_spec}' and s.is_delete <> TRUE;"
                cur.execute(sql)
                query_results = cur.fetchall()
        except Exception as err:
            logging.error('Error in select_fac_by_spec')
            logging.error(err)
            return False
        return query_results

    def select_homework_by_student(self, my_student):
        try:
            with self.conn.cursor() as cur:
                sql = 'select t.task, t.addition, h.status ' \
                      'from homework h ' \
                      'inner join task t on h.task_id=t.id ' \
                      'inner join student s on h.id_student=s.id ' \
                      f"where s.name = '{my_student}' or s.full_name = '{my_student}' "
                cur.execute(sql)
                query_results = cur.fetchall()
        except Exception as err:
            logging.error('Error in select_fac_by_spec')
            logging.error(err)
            return False
        return query_results


class LowDatabaseForAdmin(BaseLowDatabase):
    def __init__(self):
        self.conn = psycopg2.connect(host="localhost",  # Тут будет вход под пользователем "Админ"
                                     port=5432,
                                     database="University",
                                     user="postgres",
                                     password="i183")

    def insert_teacher(self, full_name, name, password, is_delete=False):
        try:
            with self.conn.cursor() as cur:
                sql = 'insert into teacher(full_name, name, password, is_delete) ' \
                      f"values('{full_name}', '{name}','{password}', '{is_delete}') "
                cur.execute(sql)
                self.conn.commit()
                return True
        except Exception as err:
            logging.error('Error into insert_teacher!')
            logging.error(err)
            return False

    def insert_student(self, full_name, password, name, id_spec, course, is_delete=False):
        try:
            with self.conn.cursor() as cur:
                sql = 'insert into student(full_name, name, password, id_spec, course, is_delete) ' \
                      f"values('{full_name}', '{name}','{password}', {id_spec}, {course}, '{is_delete}') "
                cur.execute(sql)
                self.conn.commit()
                return True
        except Exception as err:
            logging.error('Error into insert_student!')
            logging.error(err)
            return False

    def insert_admin(self, password, name, full_name, is_delete=False):
        try:
            with self.conn.cursor() as cur:
                sql = "Insert into admin(name,full_name,password, is_delete) " \
                      f"values('{name}', '{full_name}', '{password}', '{is_delete}' )"
                cur.execute(sql)
                self.conn.commit()
                return True
        except Exception as err:
            logging.error('Error into insert_admin!')
            logging.error(err)
            return False

    def insert_subject(self, subject, teacher, is_delete=False):
        try:
            with self.conn.cursor() as cur:
                sql = "Insert into subject(name, teacher_id, is_delete) " \
                      f"values('{subject}', '{teacher}', '{is_delete}')"
                cur.execute(sql)
                self.conn.commit()
                return True
        except Exception as err:
            logging.error('Error into insert_subject!')
            logging.error(err)
            return False

    def update_bell(self, id, first_time, second_time):
        try:
            with self.conn.cursor() as cur:
                sql = f"update bell set begin_time = '{first_time}' " \
                      f"where id = {id}"
                cur.execute(sql)
                self.conn.commit()

                sql = f"update bell set end_time = '{second_time}' " \
                      f"where id = {id}"
                cur.execute(sql)
                self.conn.commit()
                return True
        except Exception as err:
            logging.error('Error into update_bell!')
            logging.error(err)
            return False

    def insert_bell(self, first_time, second_time):
        try:
            with self.conn.cursor() as cur:
                sql = 'insert into bell(begin_time, end_time)' \
                      f"values('{first_time}', '{second_time}') "
                cur.execute(sql)
                self.conn.commit()
                return True
        except Exception as err:
            logging.error('Error into insert_bell!')
            logging.error(err)
            return False

    def insert_faculty(self, name, is_delete=False):
        try:
            with self.conn.cursor() as cur:
                sql = 'insert into faculty(name, is_delete)' \
                      f"values('{name}', '{is_delete}');"
                cur.execute(sql)
                self.conn.commit()
                return True
        except Exception as err:
            logging.error('Error into insert_faculty!')
            logging.error(err)
            self.conn.rollback()
            return False

    def insert_specialization(self, name, id):
        try:
            with self.conn.cursor() as cur:
                sql = "Insert into speciality(name, id_fac, is_delete) " \
                      f"values('{name}', {id}, 'false')"
                cur.execute(sql)
                self.conn.commit()
                return True
        except Exception as err:
            logging.error('Error into insert_specialization!')
            logging.error(err)
            self.conn.rollback()
            return False

    def delete_student(self, id):
        try:
            with self.conn.cursor() as cur:
                sql = f"Update student set is_delete = TRUE where id = {id}"
                cur.execute(sql)
                self.conn.commit()
                return True
        except Exception as err:
            logging.error('Error into delete_student!')
            logging.error(err)
            return False

    def delete_teacher_by_name(self, name):
        try:
            with self.conn.cursor() as cur:
                # sql = f"Delete from teacher where name='{name}' or full_name = '{name}'"
                sql = f"Update teacher " \
                      f"set is_delete = TRUE " \
                      f"where name='{name}' or full_name = '{name}'"
                cur.execute(sql)
                self.conn.commit()
                return True
        except Exception as err:
            logging.error('Error into delete teacher_by_name')
            logging.error(err)
            return False

    def delete_fac_by_name(self, name):
        try:
            with self.conn.cursor() as cur:
                # sql = f"Delete from teacher where name='{name}' or full_name = '{name}'"
                sql = f"Update faculty " \
                      f"set is_delete = TRUE " \
                      f"where name='{name}' "
                cur.execute(sql)
                self.conn.commit()
                return True
        except Exception as err:
            logging.error('Error into delete teacher_by_name')
            logging.error(err)
            return False

    def delete_admin(self, name):
        try:
            with self.conn.cursor() as cur:
                sql = f"Update admin " \
                      f"set is_delete = TRUE " \
                      f"where name='{name}' "
                cur.execute(sql)
                self.conn.commit()
                return True
        except Exception as err:
            logging.error('Error into delete teacher_by_name')
            logging.error(err)
            return False

    def delete_subject(self, name):
        try:
            with self.conn.cursor() as cur:
                sql = f"Update subject " \
                      f"set is_delete = TRUE " \
                      f"where name='{name}' "
                cur.execute(sql)
                self.conn.commit()
                return True
        except Exception as err:
            logging.error('Error into delete teacher_subject')
            logging.error(err)
            return False

    def delete_speciality(self, id):
        try:
            with self.conn.cursor() as cur:
                sql = f"Update speciality " \
                      f"set is_delete = TRUE " \
                      f"where name='{id}' "
                cur.execute(sql)
                self.conn.commit()
                return True
        except Exception as err:
            logging.error('Error into delete delete_speciality')
            logging.error(err)
            return False

    def insert_timetable(self, bell, subject, specialization, day_of_week, course):
        try:
            with self.conn.cursor() as cur:
                sql = "Insert into timetable(bell_id, id_subject, specialization_id, day_of_week, course) " \
                      f"values({bell}, {subject}, {specialization}, '{day_of_week}', '{course}')"
                cur.execute(sql)
                self.conn.commit()
                return True
        except Exception as err:
            logging.error('Error into insert_timetable!')
            logging.error(err)
            self.conn.rollback()
            return False

    def insert_course_spec(self, id, course):
        try:
            with self.conn.cursor() as cur:
                sql = "Insert into course_spec(spec_id, course, is_delete) " \
                      f"values({id}, {course}, FALSE)"
                cur.execute(sql)
                self.conn.commit()
                return True
        except Exception as err:
            logging.error('Error into insert_timetable!')
            logging.error(err)
            self.conn.rollback()
            return False

    def delete_timetable(self, id):
        try:
            with self.conn.cursor() as cur:
                sql = f"Update timetable " \
                      f"set is_delete = TRUE " \
                      f"where id='{id}' "
                cur.execute(sql)
                self.conn.commit()
                return True
        except Exception as err:
            logging.error('Error into delete delete_timetable')
            logging.error(err)
            return False

    def delete_course_spec(self, spec_id):
        try:
            with self.conn.cursor() as cur:
                sql = f"Update course_spec " \
                      f"set is_delete = TRUE " \
                      f"where spec_id='{spec_id}' "
                cur.execute(sql)
                self.conn.commit()
                return True
        except Exception as err:
            logging.error('Error into delete delete_timetable')
            logging.error(err)
            return False

    def update_timetable(self, timetable_id, bell, subject_id, specialization_id, day_of_week, course):
        try:
            with self.conn.cursor() as cur:
                sql = f"Update timetable t " \
                      f"set t.bell_id = {bell}, " \
                      f"t.id_subject = {subject_id}, " \
                      f"t.specialization_id = {specialization_id}, " \
                      f"t.day_of_week = {day_of_week}, " \
                      f"t.course = {course}, " \
                      f"t.is_delete = FALSE" \
                      f" where t.id = {timetable_id}"
                cur.execute(sql)
                self.conn.commit()
                return True
        except Exception as err:
            logging.error('Error into delete_student!')
            logging.error(err)
            return False


class LowDatabaseForTeacher(BaseLowDatabase):
    def __init__(self):
        self.conn = psycopg2.connect(host="localhost",  # Тут будет вход под пользователем "Преподаватель"
                                     port=5432,
                                     database="University",
                                     user="postgres",
                                     password="i183")


class LowDatabaseForStudent(BaseLowDatabase):
    def __init__(self):
        self.conn = psycopg2.connect(host="localhost",  # Тут будет вход под пользователем "Студент"
                                     port=5432,
                                     database="University",
                                     user="postgres",
                                     password="i183")


class Database:
    def __init__(self):
        self.low_db = LowLevelDb()

    def get_speciality_id_by_name(self, name_spec):
        res = self.low_db.select_spec_id_by_name(name_spec)
        return res[0]

    def get_homework_by_student(self, my_student):
        res = self.low_db.select_homework_by_student(my_student)
        return res

    def get_facultyes_by_spec(self, my_spec):
        my_fac = self.low_db.select_fac_by_spec(my_spec)
        return my_fac

    def get_bells_by_id(self, my_id):
        res = self.low_db.select_bells_by_id(my_id)
        return res

    def get_students(self):
        students = self.low_db.select_student()
        return students

    def get_speciality(self):
        speciality = self.low_db.select_specialization()
        return speciality

    def get_homework(self):
        homeworks = self.low_db.select_homework_with_all()
        return homeworks

    def get_deans(self):
        deans = self.low_db.select_deans()
        dict_deans = dict()
        for dean in deans:
            i = dean[0]
            dict_deans[i] = [dean[1], dean[3]]
        return dict_deans

    def get_bells(self):
        bells = self.low_db.select_bells()
        dict_bells = dict()
        for bell in bells:
            id = bell[0]
            dict_bells[id] = [bell[1], bell[2]]
        return dict_bells

    def delete_teacher(self, name):
        res = self.low_db.delete_teacher_by_name(name)
        return res

    def get_subjects(self):
        res = self.low_db.select_subjects()
        #################ДОБАВИТЬ ОБРАБОТКУ!!!!
        return res

    def get_teachers(self):
        res = self.low_db.select_teachers()
        return res

    def get_user_by_credentionals(self, password, full_name, username):
        students = self.low_db.select_student_by_cred(password=password,
                                                      full_name=full_name,
                                                      name=username)
        deans = self.low_db.select_dean_by_cred(password=password,
                                                full_name=full_name,
                                                name=username)
        teacher = self.low_db.select_teacher_by_cred(password=password,
                                                     full_name=full_name,
                                                     name=username)
        print(students)
        print(deans)
        print(teacher)
        if students:
            return list(students[0]), 'student'
        elif deans:
            return list(deans[0]), 'dean'
        elif teacher:
            return list(teacher[0]), 'teacher'
        else:
            return False, False

    def save_dean(self, full_name, name, password):
        self.low_db.insert_dean(full_name=full_name,
                                name=name,
                                password=password)

    def get_facultyes(self):
        res = 'a, b, c'
        raw_res = self.low_db.select_facultyes()
        print(raw_res)
        # print(raw_res[0][1])
        # res = [i[1] for i in raw_res]
        # res = ', '.join(res)
        return res

    def get_specialization(self):
        # raw_res = self.low_db.select_specialization()
        # print(raw_res)
        # res = [i[1] for i in raw_res]
        # res = ', '.join(res)
        return 1

    def get_student_names(self):
        # raw_res = self.low_db.select_student(names=True)
        # res = [i[1] for i in raw_res]
        # res = ', '.join(res)
        return 1


class LowLevelDb:
    def __init__(self):
        self.conn = psycopg2.connect(host="localhost",
                                     port=5432,
                                     database="University",
                                     user="postgres",
                                     password="i183")

    def delete_teacher_by_name(self, name):
        try:
            with self.conn.cursor() as cur:
                # sql = f"Delete from teacher where name='{name}' or full_name = '{name}'"
                sql = f"Update teacher set is_deleted = TRUE where name='{name}' or full_name = '{name}'"
                cur.execute(sql)
                self.conn.commit()
                return True
        except Exception as err:
            logging.error('Error into delete teacher_by_name')
            logging.error(err)
            return False

    def select_student_by_cred(self, name, full_name, password):
        try:
            with self.conn.cursor() as cur:
                sql = 'Select * from student ' \
                      f"where name = '{name}' and full_name = '{full_name}' and password = '{password}'"
                cur.execute(sql)
                query_results = cur.fetchall()
        except Exception as err:
            logging.error('Error in select_student_by_cred')
            logging.error(err)
            return False
        return query_results

    def select_dean_by_cred(self, name, full_name, password):
        try:
            with self.conn.cursor() as cur:
                sql = 'Select * from dean ' \
                      f"where name = '{name}' and full_name = '{full_name}' and password = '{password}'"
                cur.execute(sql)
                query_results = cur.fetchall()
        except Exception as err:
            logging.error('Error in select_dean_by_cred')
            logging.error(err)
            return False
        return query_results

    def select_teacher_by_cred(self, name, full_name, password):
        try:
            with self.conn.cursor() as cur:
                sql = 'Select * from teacher ' \
                      f"where name = '{name}' and full_name = '{full_name}' and password = '{password}'"
                cur.execute(sql)
                query_results = cur.fetchall()
        except Exception as err:
            logging.error('Error in select_teacher_by_cred')
            logging.error(err)
            return False
        return query_results

    def select_bells_by_id(self, my_id):
        try:
            with self.conn.cursor() as cur:
                sql = 'Select * from bell b ' \
                      f"where b.id = '{my_id}';"
                cur.execute(sql)
                query_results = cur.fetchall()
        except Exception as err:
            logging.error('Error in select_teacher_by_cred')
            logging.error(err)
            return False
        return query_results

    def select_fac_by_spec(self, my_spec):
        try:
            with self.conn.cursor() as cur:
                sql = 'select f.name from speciality s ' \
                      'inner join faculty f on f.id = s.id_fac ' \
                      f"where s.name='{my_spec}';"
                cur.execute(sql)
                query_results = cur.fetchall()
        except Exception as err:
            logging.error('Error in select_fac_by_spec')
            logging.error(err)
            return False
        return query_results

    def select_homework_by_student(self, my_student):
        try:
            with self.conn.cursor() as cur:
                sql = 'select t.task, t.addition ' \
                      'from homework h ' \
                      'inner join task t on h.task_id=t.id ' \
                      'inner join student s on h.id_student=s.id ' \
                      f"where s.username = '{my_student}'"
                cur.execute(sql)
                query_results = cur.fetchall()
        except Exception as err:
            logging.error('Error in select_fac_by_spec')
            logging.error(err)
            return False
        return query_results

    def select_spec_id_by_name(self, name_spec):
        try:
            with self.conn.cursor() as cur:
                sql = f"select id from speciality where name = '{name_spec}'"
                cur.execute(sql)
                query_results = cur.fetchall()
        except Exception as err:
            logging.error('Error in select_fac_by_spec')
            logging.error(err)
            return False
        return query_results

    def select_facultyes(self):
        pass

    def select_specialization(self):
        pass

    def select_student(self, names):
        pass


def main():
    my_db = Database()
    my_db.get_deans()
    # print(res)
    # print(res)


if __name__ == '__main__':
    main()
