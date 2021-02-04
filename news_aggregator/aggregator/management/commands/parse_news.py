import time

import bs4
import requests
from django.core.management.base import BaseCommand

from aggregator.models import News


PAUSE = 60*60


def _parse_news(last_news_titles):
    while True:
        response = requests.get('https://news.ycombinator.com')
        soup = bs4.BeautifulSoup(response.text, 'lxml')
        news = soup.findAll('tr', {'class': 'athing'})
        for item in reversed(news):
            title = item.find('a', 'storylink').getText()
            link = item.find('a', 'storylink')['href']
            if title not in last_news_titles:
                News.objects.create(title=title, link=link).save()
        print('Статьи загружены')
        time.sleep(PAUSE)


def _get_last_news_titles_from_db():
    last_news = News.objects.order_by('-id')[:31]
    last_news_titles = []
    for item in last_news:
        last_news_titles.append(item.title)
    return last_news_titles


class Command(BaseCommand):
    help = 'Start periodical parsing of Hacker News and save result to db.'

    def handle(self, *args, **options):
        last_news_titles = _get_last_news_titles_from_db()
        _parse_news(last_news_titles=last_news_titles)
