from aiogram.types import CallbackQuery,Message
from aiogram import Router,F
from keyboards.inline import language_kb,delete_his_kb
from aiogram.fsm.context import FSMContext
from misc.state import TranslationState,AdminState
from deep_translator import GoogleTranslator
from keyboards.reply import start_kb
from database.main import translations_repo,users_repo,history_repo
from datetime import datetime
import os
from dotenv import  load_dotenv
load_dotenv()

PASSWORD = os.getenv('PASSWORD')
CHAT_ID = os.getenv("CHAT_ID")

router = Router()



@router.callback_query(F.data == 'home')
async def back_to_main(call: CallbackQuery, state: FSMContext):
    await state.clear()

    from handlers.commands import start
    await start(call.message)


@router.callback_query(F.data.startswith('next_page'))
async def next_languages(call: CallbackQuery, state: FSMContext):

    state_data = await state.get_data()


    data = call.data
    __, start, finish, page, total_pages = data.split(':')

    if int(page) == int(total_pages):
        return await call.answer('Last page', show_alert=True)

    await call.message.edit_reply_markup(
        reply_markup=language_kb(
            start=int(start)+30,
            limit = int(finish) + 30,
            current_page=int(page) + 1,
            is_from=state_data.get('is_from')
        )
    )

@router.callback_query(F.data.startswith('prev_page'))
async def prev_languages(call: CallbackQuery, state: FSMContext):
    state_data = await state.get_data()

    data = call.data
    __, start, finish, page = data.split(':')

    if int(page) == 1:
        return await call.answer('You are in a first page', show_alert=True)

    await call.message.edit_reply_markup(
        reply_markup=language_kb(
            start=int(start)-30,
            limit=int(finish)-30,
            current_page=int(page)-1,
            is_from = state_data.get('is_from')
        )
    )

@router.callback_query(F.data.startswith('get_lang_from'))
async def get_lang(call: CallbackQuery, state: FSMContext):
    await call.answer()

    _, lang_code,lang_name = call.data.split(':')

    await state.update_data(is_from=False,lang_from_code=lang_code,lang_from=lang_name)
    # await state.set_state(TranslationState.lang_to)

    await call.message.edit_text(
        text=f'Chosen language: {lang_code}\nChoose a language to witch you want to translate.',
        reply_markup=language_kb(is_from=False)
    )


@router.callback_query(F.data.startswith('get_lang_to'))
async def get_lang_to(call: CallbackQuery, state: FSMContext):
    await call.answer()

    state_data = await state.get_data()
    __,lang_code,lang_name = call.data.split(':')

    await call.message.edit_text(text='Write a word or a sentence for translation.',
                                 reply_markup=None)

    await state.update_data(lang_to_code=lang_code,lang_to=lang_name)
    await state.set_state(TranslationState.text)

@router.message(TranslationState.text)
async def translate(message: Message, state: FSMContext):
    state_data = await state.get_data()

    lang_from_code = state_data.get('lang_from_code')
    lang_to_code = state_data.get('lang_to_code')

    lang_from = state_data.get('lang_from')
    lang_to = state_data.get('lang_to')

    text = message.text

    translator = GoogleTranslator(source=lang_from_code, target=lang_to_code)
    translated_text = translator.translate(text)

    user_id = users_repo.get_user(chat_id=message.from_user.id)
    current_datetime = datetime.now()

    translations_repo.add_translation(
        lang_from=lang_from,
        lang_to=lang_to,
        original=text,
        translated=translated_text,
        created_at=current_datetime.strftime("%Y-%m-%d %H:%M:%S"),
        user_id=user_id[0]
    )

    await message.answer(
        text=f'''
FROM: {lang_from}
TO: {lang_to}
ORIGINAL: {text}
TRANSLATED: {translated_text}
''',reply_markup=start_kb()
    )
    await state.clear()

@router.callback_query(F.data.startswith('delete'))
async def delete(call: CallbackQuery, state:FSMContext):
    state_data = await state.get_data()
    __, _id = call.data.split(':')
    history_repo.delete_history(_id = _id)
    await call.message.edit_text('This translation was deleted from your history of translations',reply_markup=None)

#admin

@router.callback_query(F.data.startswith('admin'))
async def admin_users(call: CallbackQuery, state: FSMContext):
    __, _action = call.data.split(':')
    await state.update_data(action=_action)
    await call.message.edit_text(text='Please write a password to access this page')
    await state.set_state(AdminState.password)

@router.message(AdminState.password)
async def give_datas(message: Message, state: FSMContext):
    password = message.text
    chat_id = message.from_user.id
    data = await state.get_data()
    action = data['action']
    if password == PASSWORD and chat_id == int(CHAT_ID):
        if action == 'users':
            users = users_repo.get_all_users()
            for user in users:
                await message.answer(f'User ID: {user[0]}\nChat ID: {user[1]}\nFirst Name: {user[2]}\nLast Name: {user[3]}\nUsername: {user[4]}\nLanguage: {user[5]}')
        elif action == 'translations':
            pass
    else:
        await message.answer("You're not allowed to access this data")