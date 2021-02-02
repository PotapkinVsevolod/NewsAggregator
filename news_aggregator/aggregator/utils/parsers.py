import time

import bs4
import requests


def news_parser():
    response = requests.get('https://news.ycombinator.com')
    soup = bs4.BeautifulSoup(response.text, 'lxml')
    news = soup.findAll('tr', {'class': 'athing'})
    for item in reversed(news):
        title = item.find('a', 'storylink').getText()
        link = item.find('a', 'storylink')['href']
        # print(f'Заголовок - {title}\nСсылка - {link}')


if __name__ == '__main__':
    news_parser()
