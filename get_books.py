import requests
from bs4 import BeautifulSoup
import json
import time

from openpyxl.workbook import Workbook


# Возвращаем html кода из url
def get_data_html(url):
    headers = {
        'accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,'
                  'application/signed-exchange;v=b3;q=0.9',
        'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) '
                      'Chrome/105.0.0.0 Safari/537.36 '

    }
    response = requests.get(url=url, headers=headers)
    soup = BeautifulSoup(response.text, 'lxml')
    return soup


# Формируем список из словарей всех книг категории
def get_books(url):
    books = []
    html_for_number_page = get_data_html(url)
    page_count = int(html_for_number_page.find('div', class_='pagination-number__right').find('a').text)
    count_books = 0
    # for page in range(1, page_count + 1):
    for page in range(1, 3):
        url_page = f'{url}?display=table&page={page}'  # Ссылка на текущую страница
        soup_page = get_data_html(url_page)  # Получаем из функции html текущей страницы
        books_items = soup_page.find('tbody', class_='products-table__body').find_all('tr')  # Все строчки с книгами
        # Перебираем все строчки по одной
        for item in books_items:
            title = item.find('td', class_='col-sm-4').text.strip()
            author = item.find('td', class_='col-sm-2').text.strip()
            price_after = int(item.find('span', class_='price-val').text.replace('₽', '').replace(' ', '').strip())
            try:
                sell = int(item.find('span', class_='price-val')['title'].strip().split()[0][1:-1])
            except:
                sell = 0
            try:
                price_before = int(item.find('span', class_='price-old').text.strip().replace(' ', ''))
            except:
                price_before = 0
            url_book = f'https://www.labirint.ru{item.find("td", class_="col-sm-4").find("a")["href"]}'

            count_books += 1

            books.append(
                {
                    'title': title,
                    'author': author,
                    'price_before': price_before,
                    'price_after': price_after,
                    'percentage_discount': sell,
                    'url': url_book

                }
            )
    category = url.split('/')[-2]  # Извлекаем из url id категории
    books.append(category)  # Последний словарь с книгами с номером категории
    print(f'всего книг собрали {count_books}')
    print(f'Категория {category}')
    return books


def save_json(data: list):
    file_name = get_file_name(data[-1]) + '.json'
    with open(file_name, 'w', encoding='UTF-8') as file:
        json.dump(data[:-1], file, indent=4, ensure_ascii=False)


def save_excel(data: list):
    headers = list(data[0].keys())
    file_name = get_file_name(data[-1]) + '.xlsx'

    wb = Workbook()
    page = wb.active
    page.title = 'data'
    page.append(headers)
    for book in data[:-1]:
        # row = []
        # for k, v in book.items():
        #     row.append(v)
        # page.append(row)
        page.append(list(book.values()))
    wb.save(filename=file_name)


def get_file_name(category):
    return time.strftime("%m_%d_%Y_%H_%M") + '_' + category


def main(url):
    books_data = get_books(url)
    # save_excel(books_data)
    save_json(books_data)


if __name__ == '__main__':
    main('https://www.labirint.ru/genres/2308/')
