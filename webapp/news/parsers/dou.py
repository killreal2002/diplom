from datetime import datetime
from webapp.db import db

from webapp.news.models import News
from bs4 import BeautifulSoup
from webapp.news.parsers.utils import get_html, save_news


def get_news_snippets():
    html = get_html("https://dou.ua/lenta/tags/python/?lang=en")
    if html:
        soup = BeautifulSoup(html, 'html.parser')
        all_news = soup.find('div', class_='b-lenta').findAll('article', class_='b-postcard')
        result_news = []
        for news in all_news:
            find_title = news.find('h2', class_='title').find('a')
            title = find_title.text.strip()
            url = news.find('h2', class_='title').find('a')['href']
            published = news.find('time', class_='date').text
            
            try:
                published = datetime.strptime(published, '%d %B, %H:%M').replace(year=datetime.now().year)
            except ValueError:
                published = datetime.strptime(published, '%d %B %Y, %H:%M')
            save_news(title, url, published)

def get_news_content():
    news_without_text = News.query.filter(News.text.is_(None))
    for news in news_without_text:
        html = get_html(news.url)
        if html:
            soup = BeautifulSoup(html, 'html.parser')
            news_text = soup.find('article', class_='b-typo b-typo_post').decode_contents()
            if news_text:
                news.text = news_text
                db.session.add(news)
                db.session.commit()

            