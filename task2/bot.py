import aiohttp
from aiogram import types
from bot_config import dp
from task2.parser import parse_page, save_data


@dp.message_handler(commands=['start'])
async def cmd_start(message: types.Message):
    """Старт"""
    await message.reply("Привет! Для начала, давай зарегистрируем тебя. Как тебя зовут?")


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


@dp.message_handler(lambda message: message.text and not message.text.startswith('/'))
async def get_user_name(message: types.Message):
    """получение имени пользователя"""
    await message.reply(f"Приятно познакомиться, {message.text}! Теперь выбери категорию товаров для парсинга.")


if __name__ == '__main__':
    from aiogram import executor

    executor.start_polling(dp, skip_updates=True)
