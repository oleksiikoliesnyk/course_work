from abc import ABC, abstractmethod
from loader import db_admin, db_student, db_teacher


class DefaultEssence(ABC):
    @abstractmethod
    def read(self):
        """
        Любую сущность можно прочитать
        """
        pass

    @abstractmethod
    def write(self, data):
        """
        В любую сущность можно записать новую строчку
        """
        pass

    @abstractmethod
    def delete(self, id):
        """
        В любой сущности можно удалить нужную строчку
        """
        pass


class Faculty(DefaultEssence):
    def read(self):
        facultyes = db_admin.get_facultyes()
        return facultyes

    def write(self, data):
        flag = db_admin.save_faculty(data)
        return flag

    def delete(self, id):
        flag = db_admin.delete_faculty(id)
        return flag


class Speciality(DefaultEssence):
    def read(self):
        my_speciality = db_admin.get_speciality()
        return my_speciality

    def write(self, data):
        name_of_speciality = data['spec_name']
        name_of_faculty = data['fac_name']
        if_of_faculty = db_admin.get_id_fac_by_name(name_of_faculty)
        res = db_admin.save_specialization(name=name_of_speciality,
                                           fac_id=if_of_faculty)
        return res

    def delete(self, id):
        flag = db_admin.delete_speciality(id)
        return flag


class Student(DefaultEssence):
    def read(self):
        list_of_student = db_admin.get_students()
        return list_of_student

    def write(self, data):
        name_of_student = data['name']
        full_name = data['full_name']
        password = data['password']
        course = data['course']
        id_spec = data['id_spec']
        flag = db_admin.save_student(name=name_of_student,
                                     full_name=full_name,
                                     password=password,
                                     course=course,
                                     id_spec=id_spec)
        return flag

    def delete(self, name):
        student_id = db_admin.get_student_id_by_name(name)
        flag = db_admin.delete_admin(student_id)
        return flag


class Teacher(DefaultEssence):
    def read(self):
        list_of_teacher = db_admin.get_teachers()
        return list_of_teacher

    def write(self, data):
        name_of_teacher = data['name']
        password = data['password']
        full_name = data['full_name']
        flag = db_admin.save_teacher(full_name=full_name,
                                     name=name_of_teacher,
                                     password=password)
        return flag

    def delete(self, name):
        flag = db_admin.delete_teacher(name=name)
        return flag


class Task(DefaultEssence):
    def read(self):
        pass

    def write(self, data):
        pass

    def delete(self):
        pass


class Subject(DefaultEssence):
    def read(self):
        list_of_subject = db_admin.get_subject()
        return list_of_subject

    def write(self, data):
        teacher = data['teacher']
        subject = data['subject']
        db_admin.save_subject(teacher=teacher,
                              subject=subject)

    def delete(self, name):
        flag = db_admin.delete_subject(name)
        return flag


class Bell(DefaultEssence):
    def write(self, data):
        id_of_bell = data['id']
        first_time = data['first_time']
        second_time = data['second_time']
        flag = db_admin.save_bell(id=id_of_bell,
                                  first_time=first_time,
                                  second_time=second_time)
        return flag

    def delete(self, id):
        """
        Звонки не следует удалять
        """
        pass

    def read(self):
        list_of_bells = db_admin.get_bells()
        return list_of_bells


class Homework(DefaultEssence):
    def read(self):
        pass

    def write(self):
        pass

    def delete(self):
        pass


class TimeTable(DefaultEssence):
    def read(self, speciality):
        timetable = db_admin.get_timetable(speciality)
        return timetable

    def write(self, data):
        bell = data['bell']
        subject = data['subject']
        specialization = data['specialization']
        day_of_week = data['day_of_week']
        flag = db_admin.save_timetable(bell=bell,
                                       subject=subject,
                                       specialization=specialization,
                                       day_of_week=day_of_week)
        return flag

    def delete(self):
        pass


class SolvingHomework(DefaultEssence):
    def read(self):
        pass

    def write(self):
        pass

    def delete(self):
        pass


class Admin(DefaultEssence):
    def read(self):
        list_of_admins = db_admin.get_admins()
        return list_of_admins

    def write(self, data):
        name = data['name']
        full_name = data['full_name']
        password = data['password']
        flag = db_admin.save_admin(name=name,
                                   full_name=full_name,
                                   password=password)
        return flag

    def delete(self, name):
        flag = db_admin.delete_admin(name)
        return flag


def main():
    pass


if __name__ == '__main__':
    main()
