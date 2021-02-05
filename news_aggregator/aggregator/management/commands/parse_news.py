import time

import bs4
import requests
from django.core.management.base import BaseCommand
from django.utils import timezone

from aggregator.models import News


PAUSE = 60*60


class Command(BaseCommand):
    help = 'Start periodical parsing of Hacker News and save result to db.'

    def handle(self, *args, **options):
        while True:
            last_news_titles = News.objects.order_by('-id')[:30].values_list('title', flat=True)
            response = requests.get('https://news.ycombinator.com')
            soup = bs4.BeautifulSoup(response.text, 'lxml')
            news = soup.findAll('tr', {'class': 'athing'})

            for item in reversed(news):
                title = item.find('a', 'storylink').getText()
                link = item.find('a', 'storylink')['href']

                if title not in last_news_titles:
                    News.objects.create(title=title, link=link)

            print(f'News downloads in {timezone.now()}.')
            time.sleep(PAUSE)
