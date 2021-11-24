from aiogram.dispatcher.filters.state import State, StatesGroup


class DeanState(StatesGroup):
    FreeState = State()
    ChangeBellFirst = State()
    ChangeBellSecond = State()
    DeleteTeacher = State()
    SelectBell = State()
    FacBySpec = State()
    HomeworkByStudent = State()
    SetDeanName = State()
    SetDeanPassword = State()
    SetFac = State()
    SetSpecFirst = State()
    SetSpecSecond = State()
    SetStudentFirst = State()
    SetStudentSecond = State()
    SetStudentThird = State()
    SetStudentFourth = State()
    SetStudentFifth = State()
    SetTeacherFirst = State()
    SetTeacherSecond = State()
    SetTeacherThird = State()
    DeleteStudent = State()
    DeleteFaculty = State()
    SetAdminFirst = State()
    SetAdminSecond = State()
    SetAdminThird = State()
    DeleteAdminFirst = State()
    DeleteSubject = State()
    DeleteSpeciality = State()
    SelectTimetable = State()
    SetTimetableFirst = State()
    SetTimetableSecond = State()
    SetTimetableThird = State()
    SetTimetableFourth = State()
    SetTimetableFifth = State()
    DeleteTimeTableFirst = State()
    DeleteTimeTableSecond = State()
    DeleteTimeTableThird = State()
    DeleteTimeTableFourth = State()
    AddSubjectFirst = State()
    AddSubjectSecond = State()



