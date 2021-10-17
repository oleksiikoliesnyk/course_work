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