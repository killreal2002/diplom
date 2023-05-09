from datetime import datetime
import requests
from bs4 import BeautifulSoup
from webapp.news.models import News
from webapp.db import db

def get_html(url):
    try:
        result = requests.get(url)
        result.raise_for_status()
        return result.text
    except(requests.RequestException, ValueError):
        print("network eror")
        return False


def get_news():
    html = get_html("https://www.python.org/blogs/")
    if html:
        soup = BeautifulSoup(html, 'html.parser')
        all_news = soup.find('ul', class_='list-recent-posts').findAll('li')
        result_news = []
        for news in all_news:
            title = news.find('a').text
            url = news.find('a')['href']
            published = news.find('time').text
            try:
                published = datetime.strptime(published, '%Y-%m-%d')
            except ValueError:
                published = datetime.now()
            save_news(title, url, published)


def save_news(title, url, published):
    news_exists = News.query.filter(News.url == url).count()
    print(news_exists)
    if not news_exists:
        published_str = published.isoformat()
        news_news = News(title=title, url=url, published=published_str)
        db.session.add(news_news)
        db.session.commit()

#це фрагмент коду, який здійснює веб-скрапінг новинних сторінок, аналізує HTML-код сторінки, 
# отримує необхідні поля новин (назву, URL, дату публікації) і зберігає цю інформацію в базі даних. 
# Функції get_html() та save_news() відповідають за отримання HTML-сторінки та збереження даних новин в базі даних відповідно. 
# Функція get_news() здійснює виклики цих двох функцій та обробку HTML-коду сторінки за допомогою бібліотеки BeautifulSoup.
