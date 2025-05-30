from aiogram.utils.keyboard import InlineKeyboardBuilder
from aiogram.types import InlineKeyboardButton
from deep_translator import GoogleTranslator

translator = GoogleTranslator(source='auto', target='en')
LANGUAGES = translator.get_supported_languages(as_dict=True)

def language_kb(start=0, limit=30, current_page=1, is_from=True):
    kb = InlineKeyboardBuilder()

    # Turn dict to list of tuples (lang_code, lang_name)
    language_items = list(LANGUAGES.items())
    total_pages = round(len(LANGUAGES) / 30 + 1)


    for lang_name,lang_code in language_items[start:limit]:
        if is_from:
            callback_data = f'get_lang_from:{lang_code}:{lang_name}'
        else:
            callback_data = f'get_lang_to:{lang_code}:{lang_name}'
        kb.button(text=lang_name.title(), callback_data=callback_data)

    kb.adjust(3)

    kb.row(
        InlineKeyboardButton(text='<', callback_data=f'prev_page:{start}:{limit}:{current_page}'),
        InlineKeyboardButton(text=f'{current_page}/{total_pages}', callback_data='current'),
        InlineKeyboardButton(text='>', callback_data=f'next_page:{start}:{limit}:{current_page}:{total_pages}'),
    )

    kb.row(InlineKeyboardButton(text='Main', callback_data='home'))

    return kb.as_markup()

def delete_his_kb(tran_id: int):
    kb = InlineKeyboardBuilder()
    kb.button(text='Delete History', callback_data=f'delete:{tran_id}')
    return kb.as_markup()

def admin_panel():
    kb = InlineKeyboardBuilder()
    kb.button(text='Users',callback_data='admin:users')
    kb.button(text='Translations',callback_data='admin:translations')

    return kb.as_markup()