from webapp import create_app
from webapp.news.parsers import dou
from webapp.org_news import get_news

app = create_app()
with app.app_context():
    dou.get_news_snippets()
    dou.get_news_content()