from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton

from keyboards.inline.type_button.type_callback import type_callback

type_choice = InlineKeyboardMarkup(row_width=2,
                                   inline_keyboard=[
                                       [
                                           InlineKeyboardButton(
                                               text='Студент',
                                               callback_data=type_callback.new(type='Student')
                                           ),
                                           InlineKeyboardButton(
                                               text='Преподаватель',
                                               callback_data=type_callback.new(type='Teacher')
                                           ),
                                           InlineKeyboardButton(
                                               text='Декан',
                                               callback_data=type_callback.new(type='Dean')
                                           )
                                       ]
                                   ])
