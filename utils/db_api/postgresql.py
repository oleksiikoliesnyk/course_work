import logging

import psycopg2


class BaseDatabase:
    def __init__(self):
        self.low_db = BaseLowDatabase()

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
        raw_res = self.low_db.select_admins()
        res = raw_res  # Тут будет обработка
        return res

    def get_bells(self):
        raw_res = self.low_db.select_bells()
        res = raw_res  # Тут будет обработка
        return res

    def get_timetable(self):
        pass

    def get_faculty(self):
        raw_res = self.low_db.select_facultyes()
        res = raw_res  # Тут будет обработка
        return '1, 2, 3'

    def get_speciality(self):
        raw_res = self.low_db.select_specialization()
        res = raw_res  # Тут будет обработка
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
        raw_res = self.low_db.select_subject()
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

    def save_specialization(self, name_spec, name_fac):
        fac_id = self.low_db.select_id_fac_by_name(name_fac)
        res = self.low_db.insert_specialization(name=name_spec,
                                                id=fac_id)
        return res

    def delete_student(self, id):
        res = self.low_db.delete_student(id)
        return res

    def delete_teacher(self, name):
        res = self.low_db.delete_teacher_by_name(name)
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
            sql = 'Select * from dean d' \
                  'where d.is_deleted <> TRUE;'
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
                  'from faculty f'
            cur.execute(sql)
            query_results = cur.fetchall()
            return query_results

    def select_specialization(self):
        with self.conn.cursor() as cur:
            sql = 'select s.name, f.name ' \
                  'from speciality s ' \
                  'inner join faculty f on f.id = s.id_fac; '
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
            sql = 'Select * from subject'
            cur.execute(sql)
            query_results = cur.fetchall()
            return query_results

    def select_id_fac_by_name(self, name_fac):
        with self.conn.cursor() as cur:
            sql = 'Select f.id from facultyes f' \
                  f'where f.name = "{name_fac}";'
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
            return False

    def insert_specialization(self, name, id):
        try:
            with self.conn.cursor() as cur:
                sql = "Insert into specialization(name,id_fac) " \
                      f"values('{name}','{id}')"
                cur.execute(sql)
                self.conn.commit()
                return True
        except Exception as err:
            logging.error('Error into insert_specialization!')
            logging.error(err)
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
