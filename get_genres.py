import requests
from bs4 import BeautifulSoup
import datetime
import json

all_data = []


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


def get_data_page(soup):
    global all_data
    try:
        links = soup.find('ul', class_='genre-list genre-list-all').find_all('li')
        # print(links)
        for link in links:
            if 'genres' in link.find('a')['href'] and 'only_exclusive' not in link.find('a')['href']:
                gen = link.find('a')['href']
                url = f'https://www.labirint.ru{gen}'
                # print(url)
                # all_data.append(get_data_page(get_data_html(url)))
                k = get_data_page(get_data_html(url))
                # print(url, k)
                all_data.append({url: k})
    except:
        return soup.find('h1', class_='genre-name').text


def main(url):
    t = datetime.datetime.now()
    html = get_data_html(url)

    get_data_page(html)
    # print(all_data)
    with open('cat.json', 'w', encoding='UTF-8') as file:
        json.dump(all_data, file, indent=4, ensure_ascii=False)
    print(datetime.datetime.now() - t)


if __name__ == '__main__':
    main('https://www.labirint.ru/books/')
    # main('https://www.labirint.ru/genres/966/')
