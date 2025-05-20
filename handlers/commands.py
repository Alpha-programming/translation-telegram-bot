from aiogram import Router
from aiogram.types import Message
from aiogram.filters.command import CommandStart,Command
from keyboards.reply import start_kb
from database.main import users_repo
from keyboards.inline import admin_panel

router = Router()

@router.message(CommandStart())
async def start(message: Message):
    user = message.from_user
    chat_id = user.id
    first_name = user.first_name
    last_name = user.last_name
    username = user.username
    language = user.language_code
    users_repo.add_user(
        chat_id=user.id,
        first_name=user.first_name,
        last_name=user.last_name,
        username=user.username,
        language=user.language_code
    )

    await message.answer('It is a bot to translate.\nChoose an action lower.',
                         reply_markup=start_kb())

@router.message(Command(commands='info'))
async def info(message: Message):
    await message.answer('This bot helps users to translate words and any sentences from one language to another chosen one\nIt has 113 languages in total')

@router.message(Command(commands='admin'))
async def user(message: Message):
    await message.answer("Choose an action",reply_markup=admin_panel())


