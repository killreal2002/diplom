from celery import Celery
from celery.schedules import crontab
from redis import Redis

from webapp import create_app
from webapp.news.parsers import dou
from webapp.org_news import get_news

flask_app = create_app()
celery_app = Celery('task', broker='redis://localhost:6379/0')

@celery_app.task
def dou_snippets():
    with flask_app.app_context():
        dou.get_news_snippets()

@celery_app.task
def dou_content():
    with flask_app.app_context():
        dou.get_news_content()

@celery_app.on_after_configure.connect
def setup_periodic_tasks(sender, **kwargs):
    sender.add_periodic_task(crontab(minute='*/1'), dou_snippets.s())
    sender.add_periodic_task(crontab(minute='*/1'), dou_content.s())
#Код створює Flask-додаток та об'єкт Celery, 
#де останній дозволяє запускати задачі для отримання коротких та повних новин від DOU 
#з використанням періодичної задачі за допомогою crontab.
