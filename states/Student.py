from aiogram.dispatcher.filters.state import State, StatesGroup


class StudentState(StatesGroup):
    WhichCourse = State()
    WhichSpec = State()
    FinalReg = State()
    FreeState = State()
    SelectTimetable = State()
    SelectBell = State()
    FacBySpec = State()
    HomeworkByStudent = State()
    FirstSolving = State()
    SecondSolving = State()
    ThirdSolving = State()
