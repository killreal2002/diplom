from flask import abort, Blueprint, current_app, flash, render_template, redirect, request, url_for
from flask_login import current_user, login_required

from webapp.db import db
from webapp.news.forms import CommentForm
from webapp.news.models import Comment, News
from webapp.weather import weather_by_city
from webapp.utils import get_redirect_target

blueprint = Blueprint('news', __name__)

@blueprint.route('/')
def index():
    title = "Weather/News report"
    weather = weather_by_city(current_app.config['WEATHER_DEFAULT_CITY'])
    news_list = News.query.filter(News.text.isnot(None)).order_by(News.published.desc()).all()
    return render_template('news/index.html', page_title=title, weather=weather, news_list=news_list)
#функція index() є однією з маршрутів веб-додатка, який обробляє запит до головної сторінки. 
#Функція відображає погоду за замовчуванням та список новин, відсортованих за датою публікації.

@blueprint.route('/news/<int:news_id>')
def single_news(news_id):
    my_news = News.query.filter(News.id == news_id).first()

    if not my_news:
        abort(404)
    comment_form = CommentForm(news_id=my_news.id)
    return render_template('news/single_news.html', page_title=my_news.title, news=my_news, comment_form=comment_form)
#функція single_news(news_id) також є маршрутом веб-додатка і відображає сторінку новини за заданим news_id. 
#Крім того, вона створює форму коментарів, яка передається у шаблон сторінки.

@blueprint.route('/news/comment', methods=['POST'])
@login_required
def add_comment():
    form = CommentForm()
    if form.validate_on_submit():
            comment = Comment(text=form.comment_text.data, news_id=form.news_id.data, user_id=current_user.id)
            db.session.add(comment)
            db.session.commit()
            flash('Succefully added')
    else:
        for field, errors in form.errors.items():
            for error in errors:
                flash('Mistake in field {} {}'.format(
                    getattr(form, field).label.text,
                    error
                ))
    return redirect(get_redirect_target())
#функція add_comment() є маршрутом веб-додатка для додавання коментарів до новин. 
#Функція перевіряє, чи форма коментарів валідна та додає коментар до бази даних. 
#В іншому випадку вона відображає повідомлення про помилки на сторінку.
