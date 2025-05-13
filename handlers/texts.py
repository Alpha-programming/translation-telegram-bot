from aiogram import Router,F
from aiogram.types import Message
from keyboards.inline import language_kb,delete_his_kb
from aiogram.fsm.context import FSMContext
from database.main import history_repo, users_repo
from aiogram.utils.markdown import bold, italic, text


router = Router()

@router.message(F.text == 'Translate')
async def translate(message: Message, state: FSMContext):
    await message.reply('Choose a language, from which you want to translate',
                        reply_markup=language_kb())
    await state.update_data(is_from=True)

@router.message(F.text == 'History')
async def translate(message: Message):
    user_id = users_repo.get_user(chat_id=message.from_user.id)
    history_translations = history_repo.get_history(user_id=user_id[0])
    if not history_translations:
        await message.reply("You have no translation history.")
        return

    for num,tran in enumerate(history_translations,start=1):
        original_lang = tran[0]
        translated_lang = tran[1]
        original_text = tran[2]
        translated_text = tran[3]
        timestamp = tran[4]
        _id = tran[5]

        entry = text(
            bold(f"{num} Original Text"),
            f"({italic(original_lang)}):",original_text,
            "\n",
            bold("Translated Text"),
            f"({italic(translated_lang)}):",translated_text,
            "\n",
            bold("Time:"),timestamp,
            "\n\n"
        )

        await message.reply(entry, parse_mode="Markdown",reply_markup=delete_his_kb(_id))
