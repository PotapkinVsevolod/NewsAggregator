# News Aggregator

![GitHub main code](https://img.shields.io/github/languages/top/PotapkinVsevolod/NewsAggregator)
![GitHub repo size](https://img.shields.io/github/repo-size/potapkinvsevolod/newsaggregator)

News Aggregator - это приложение, написанное на Django/Python для парсинга сайта Hacker News на предмет статей, хранение информации о статьях в базе данных (БД)
и API для получения данных клиентом в формате JSON.

## Необходимые условия

Прежде чем начать, убедитесь, что на вашем компьютере установлены:
* Python 3 (проект сделан на Python 3.8.5).
* База данных MySQL и все необходимые к ней драйвера.

## Установка News Aggregator

Для установки News Aggregator, клонируйте репозиторий с github с помощью ссылки:

```
clone https://github.com/PotapkinVsevolod/NewsAggregator.git
```
Для работы приложения необходимо установить все необходимые зависимости из файла requirements.txt.

Для записи и хранения статей необходимо будет создать базу данных, пользователя и предоставить пользователю доступ к базе.
Всю необходимую информацию по созданию и настройке БД можно найти здесь:
```
https://dev.mysql.com/doc/
```
Для связи приложения с базой данных, необходимо переопределить поля NAME, USER и PASSWORD в news_aggregator/news_aggregator/settings.py:
```
DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.mysql',
        'NAME': 'news_aggregator',
        'USER': 'potapkinvsevolod',
        'PASSWORD': 'qwerty',
    }
}
```
После этого необходимо сделать миграцию данных в БД:
```
python manage.py makemigrations
python manage.py migrate
```
## Использование News Aggregator
Парсер можно запустить командой:
```
python manage.py parse_news
```
По умолчанию парсер собирает данные сайта раз в час, но вы можете поменять тайминг, переопределив константу PAUSE (в секундах) в news_aggregator/aggregator/management/commands/parse_news.py.

Сервер API можно запустить командой:
```
python manage.py runserver
```
Пример обращения к API:
```
curl -X GET 'http://localhost:8000/posts?order=title&offset=5&limit=10'
```
## Контакты

Если возникли какие-либо вопросы, вы можете со мной связаться, написав на <potapkinvsevolod@gmail.com>.
