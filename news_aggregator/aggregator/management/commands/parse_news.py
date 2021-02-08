import time

import bs4
import requests
from django.core.management.base import BaseCommand
from django.utils import timezone

from aggregator.models import News


class Command(BaseCommand):
    help = 'Start periodical parsing of Hacker News and save result to db.'

    def handle(self, *args, **options):
        while True:
            last_news_titles = News.objects.order_by('-id').values_list('title', flat=True)[:30]
            response = requests.get('https://news.ycombinator.com')
            soup = bs4.BeautifulSoup(response.text, 'lxml')
            news = soup.findAll('tr', {'class': 'athing'})

            for item in reversed(news):
                title = item.find('a', 'storylink').getText()
                link = item.find('a', 'storylink')['href']

                bulk_creates = []
                if title not in last_news_titles:
                    bulk_creates.append(News(title=title, link=link))

                if bulk_creates:
                    News.objects.bulk_create(bulk_creates)

            options['pause'] = int(options['pause'])
            print(f'News downloads in {timezone.now()}.')
            time.sleep(options['pause'])

    def add_arguments(self, parser):
        parser.add_argument(
            '-p',
            '--pause',
            action='store',
            default=60*60,
            help='Time between parsing in seconds'
        )
