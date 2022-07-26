from datetime import datetime
from time import sleep
from typing import List
from bs4 import BeautifulSoup
import requests


def get_names(soup) -> List:
    links = soup.find('div', class_='mw-category mw-category-columns').find_all('a')
    names = [None] * len(links)
    for idx, link in enumerate(links):
        names[idx] = link['title']

    return names

def next_page(soup):
    return soup.find('a', text='Следующая страница')['href']


def count_names(names: List[str]) -> dict:
    counts = {}

    for name in names:
        alpha = name[0].lower()
        if alpha in counts.keys():
            counts[alpha] += 1
        else:
            counts[alpha] = 1

    return counts


def write_result(filename, result):
    with open(filename, 'w') as f:
        for key in result.keys():
            f.write(f'{key}: {result[key]}\n')
        exit()



if __name__ == '__main__':
    base_url = 'https://ru.wikipedia.org'
    url = 'https://ru.wikipedia.org/wiki/Категория:Животные_по_алфавиту'

    time_now = datetime.utcnow()
    link_filename = f'result/{time_now}_links.txt'
    result_filename = f'result/{time_now}_result.txt'

    result = {}
    # количество страниц для парсинга, найдено опытным путем
    # если искать - пока есть кнопка Следующая страница, то перейдём на английские имена
    # если искать, пока не встретится английское имя, то будет ошибка, т.к. присуствует
    # одно животное, которое не перевели и на нём всё закончится.
    pages_to_parse = 96

    for i in range(pages_to_parse):
        page = requests.get(url)
        if page.status_code != 200:
            write_result(result_filename, result)
                
        soup = BeautifulSoup(page.text, 'html.parser')

        names = get_names(soup)
        alphas = count_names(names)

        for alpha in alphas.keys():
            if alpha in result.keys():
                result[alpha] += alphas[alpha]
            else:
                result[alpha] = alphas[alpha]

        url = base_url + next_page(soup)
        
        with open(link_filename, 'a') as f:
            f.write(url)
            f.write('\n')
        
        print(f'Parsed page {i+1} of {pages_to_parse}...')
        sleep(1)

    write_result(result_filename, result)
