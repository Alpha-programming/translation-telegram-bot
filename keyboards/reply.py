from aiogram.types import ReplyKeyboardMarkup, KeyboardButton
from aiogram.utils.keyboard import ReplyKeyboardBuilder

def start_kb():
    kb = ReplyKeyboardBuilder()

    kb.button(text='Translate')
    kb.button(text='History')

    kb.adjust(2)

    return kb.as_markup(resize_keyboard=True)


# from aiogram.types import InlineKeyboardButton, InlineKeyboardMarkup
#
# def start_kb(deactivated=False):
#     kb = InlineKeyboardMarkup()
#
#     if deactivated:
#         # Deactivated buttons
#         kb.add(InlineKeyboardButton(text="Translate", callback_data="deactivated_translate"))
#         kb.add(InlineKeyboardButton(text="History", callback_data="deactivated_history"))
#     else:
#         # Active buttons
#         kb.add(InlineKeyboardButton(text="Translate", callback_data="translate"))
#         kb.add(InlineKeyboardButton(text="History", callback_data="history"))
#     kb.adjust(2)
#
#     return kb.as_markup(resize_keyboard=True)
