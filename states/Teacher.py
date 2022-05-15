from aiogram.dispatcher.filters.state import State, StatesGroup


class TeacherState(StatesGroup):
    WhichCourse = State()
    WhichSpec = State()
    FinalReg = State()
    FreeState = State()
    SelectTimetable = State()
    SelectBell = State()
    FacBySpec = State()
    HomeworkByStudent = State()