import aiohttp
import asyncio
import csv
from bs4 import BeautifulSoup
import datetime


async def fetch_html(url, session):
    """Получаем html код со страцниы"""
    async with session.get(url) as response:
        return await response.text()


async def get_book_data(detail_url, session):
    """Получение детальных данных о книге"""

    html = await fetch_html(detail_url, session)
    soup = BeautifulSoup(html, 'lxml')
    product_info_block = soup.find('div', class_='sub-header').find_next('table')
    product_info = {}
    for row in product_info_block.find_all('tr'):
        columns = row.find_all(['th', 'td'])
        key = columns[0].get_text(strip=True)
        value = columns[1].get_text(strip=True)
        product_info[key] = value

    return product_info


async def get_all_books(url, session):
    """Парсим страницу"""
    html = await fetch_html(url, session)
    soup = BeautifulSoup(html, 'lxml')
    base_url = 'https://books.toscrape.com/catalogue'

    books = []
    for book in soup.select('.product_pod'):
        title = book.h3.a['title']
        price = book.select_one('.price_color').get_text(strip=True)
        in_stock = book.select_one('.instock.availability').get_text(strip=True)
        book_link = base_url + book.select_one('.image_container').a['href'][8:]
        product_info = await get_book_data(book_link, session)
        books.append({'Название': title, 'Цена': price, "Наличие": in_stock, "Ссылка": book_link,
                      'Характеристики': product_info})

    return books


async def save_data(url):
    """Сохранение данных"""
    url = url

    async with aiohttp.ClientSession() as session:
        books = await get_all_books(url, session)

    curr_time = datetime.datetime.now().strftime('%Y%m%d%H%M%S')
    csv_file = f'books_{curr_time}.csv'
    fieldnames = ['Название', 'Цена', 'Наличие', 'Ссылка', 'Характеристики']

    with open(csv_file, mode='w', newline='', encoding='utf-8') as file:
        writer = csv.DictWriter(file, fieldnames=fieldnames)
        writer.writeheader()
        writer.writerows(books)


if __name__ == '__main__':
    asyncio.run(save_data('https://books.toscrape.com/catalogue/category/books/travel_2/index.html'))
