import requests
from bs4 import BeautifulSoup
import csv

URL = 'https://www.weblancer.net/jobs/'
HOST = 'https://www.weblancer.net'

def get_html(url, params=''):
    r = requests.get(url, params=params)
    return r

def Get_content(html):
    soup = BeautifulSoup(html, 'html.parser')
    items = soup.find_all('div', class_='row click_container-link set_href')

    cards = []
    for item in items:
        cards.append(
            {
                'title': item.find('div' ,class_='title').get_text(),
                'price': item.find('div' ,class_='float-right').get_text(),
                'orders': item.find('div' ,class_='float-left').get_text().strip(),
                'later': item.find('span' ,class_='text-muted').get_text(),
                'type': item.find('span' ,class_='text-nowrap').get_text(),
                'link': item.find('div' ,class_='title').find('a').get('href')
            }
        )
    return cards

def save_doc(items, path):
    with open(path, 'w', newline='') as file:
        writer = csv.writer(file, delimiter=';')
        writer.writerow(['название', 'цена', 'заявки', 'дата', 'тип', 'ссылка'])
        for item in items:
            writer.writerow( [item['title'], item['price'], item['orders'], item['later'], item['type'], item['link']] )

def pars():
    PAGENATION = input('количество страниц: ')
    PAGENATION = int(PAGENATION.strip())
    html = get_html(URL)
    if html.status_code == 200:
        cards = []
        for page in range(1, PAGENATION):
            print(f"парсинг страницы: {page}")
            html = get_html(URL, params={'?page' : page})
            cards.extend(Get_content(html.text))
        save_doc(cards, 'wedlancer.csv')
        print(cards)
    else:
        print('Eror')

pars()