from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton
from loader import db_admin as db
from aiogram.utils.callback_data import CallbackData

my_fac = db.get_faculty().split(', ')

inline_keyboard_list = list()
my_callback = CallbackData('fac', 'fac')
for ind, i in enumerate(my_fac):
    my_keyboard = InlineKeyboardButton(text=i, callback_data=my_callback.new(fac=ind.__repr__()))
    inline_keyboard_list.append(my_keyboard)

fac_choice = InlineKeyboardMarkup(row_width=2,
                                   inline_keyboard=[
                                       inline_keyboard_list
                                   ])
