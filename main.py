import requests
from bs4 import BeautifulSoup
import json
import time

from openpyxl.workbook import Workbook


def get_data():
    headers = {
        'accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,'
                  'application/signed-exchange;v=b3;q=0.9',
        'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) '
                      'Chrome/105.0.0.0 Safari/537.36 '

    }
    books = []
    url = 'https://www.labirint.ru/genres/2308/'

    response = requests.get(url=url, headers=headers)
    soup = BeautifulSoup(response.text, 'lxml')
    page_count = int(soup.find('div', class_='pagination-number__right').find('a').text)
    # print(page_count)
    count_books = 0
    for page in range(1, page_count + 1):
        # print(f 'СТРАНИЦА {page}')
        url = f'https://www.labirint.ru/genres/2308/?page={page}&display=table'
        response = requests.get(url=url, headers=headers)
        soup = BeautifulSoup(response.text, 'lxml')
        books_items = soup.find('tbody', class_='products-table__body').find_all('tr')
        for k, item in enumerate(books_items):
            # print(f'Айтем №{k + 1}')
            title = item.find('td', class_='col-sm-4').text.strip()
            author = item.find('td', class_='col-sm-2').text.strip()
            price_after = item.find('span', class_='price-val').text.replace('₽', '').strip()
            # print(price_after)
            try:
                sell = item.find('span', class_='price-val')['title'].strip()
            except:
                sell = 'Нет скидки'
            try:
                price_before = item.find('span', class_='price-old').text.strip()
            except:
                price_before = 0
            url = f'https://www.labirint.ru{item.find("td", class_="col-sm-4").find("a")["href"]}'

            count_books += 1

            books.append(
                {
                    'title': title,
                    'author': author,
                    'price_before': price_before,
                    'price_after': price_after,
                    'sell': sell,
                    'url': url

                }
            )
    # with open('labirint.json', 'w', encoding='UTF-8') as file:
    #     json.dump(books, file, indent=4, ensure_ascii=False)
    print(f'всего книг собрали {count_books}')
    return books


def save_excel(data: list):
    headers = ['Название', 'Автор', 'Цена до скидки', 'Цена со скидкой', 'Скидки', 'URL']
    workbook_name = time.strftime("%m_%d_%Y_%H_%M") + '.xlsx'

    wb = Workbook()
    page = wb.active
    page.title = 'data'
    page.append(headers)  # write the headers to the first line

    for book in data:
        row = []
        for k, v in book.items():
            row.append(v)
        page.append(row)
        # page.append(list(book.values()))
    wb.save(filename=workbook_name)


def main():
    all_books = get_data()
    save_excel(all_books)


if __name__ == '__main__':
    main()
