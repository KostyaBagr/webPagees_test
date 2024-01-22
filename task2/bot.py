import aiohttp
from aiogram import types
from aiogram.dispatcher import FSMContext
from bot_config import dp, bot
from task2.keyboard import parsing_btn
from task2.parser import parse_page, save_data
from task2.crud import user_exists, create_user
from aiogram.dispatcher.filters.state import State, StatesGroup



class RegistrationState(StatesGroup):
    waiting_for_name = State()


@dp.message_handler(commands=['start'])
async def command_start_handler(message: types.Message, state: FSMContext):
    user = await user_exists(telegram_id=message.from_user.id)

    if not user:
        await bot.send_message(message.from_user.id, "Введите свое имя")
        await RegistrationState.waiting_for_name.set()
    else:
        await bot.send_message(message.from_user.id, f"Добро пожаловать, {message.from_user.first_name}",
                               reply_markup=parsing_btn)


@dp.message_handler(state=RegistrationState.waiting_for_name)
async def process_user_name(message: types.Message, state: FSMContext):
    user_data = {
        "name": message.text,
        "username": message.from_user.username,
        "telegram_id": message.from_user.id
    }

    await create_user(data=user_data)

    await state.finish()
    await bot.send_message(message.from_user.id, "Спасибо! Теперь вы зарегистрированы.", reply_markup=parsing_btn)


@dp.message_handler(lambda message: message.text.startswith('https://books.toscrape.com/catalogue/category/b'))
async def process_category_link(message: types.Message):
    """Получение ссылки от пользователя"""
    category_url = message.text
    await message.reply("Жди, идет парсинг данных...")

    async with aiohttp.ClientSession() as session:
        books_data = await parse_page(category_url, session)

    csv_file_path = f'books_data_{message.from_user.id}.csv'
    await save_data(csv_file_path, books_data)

    await message.reply_document(types.InputFile(csv_file_path), caption="Парсинг завершен! Вот файл с данными.")


if __name__ == '__main__':
    from aiogram import executor

    executor.start_polling(dp, skip_updates=True)
