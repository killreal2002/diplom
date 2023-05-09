from flask_wtf import FlaskForm
from wtforms import HiddenField, StringField, SubmitField
from wtforms.validators import DataRequired, ValidationError

from webapp.news.models import News

class CommentForm(FlaskForm):
    news_id = HiddenField('News ID', validators=[DataRequired()])
    comment_text = StringField("Your comment:", validators=[DataRequired()], render_kw={"class": "form-control"})
    submit = SubmitField('Send comment', render_kw={"class": "btn btn-primary"})

    def validate_news_id(self, news_id):
        if not News.query.get(news_id.data):
            raise ValidationError('Article with this ID doesnt exist')
#Клас CommentForm описує форму для додавання коментаря до новини. Він успадковує клас FlaskForm.
#news_id - приховане поле з ID новини, до якої додається коментар.
#comment_text - текстове поле для введення коментаря.
#submit - кнопка для відправки форми.
#Метод validate_news_id виконує перевірку наявності новини з вказаним ID в базі даних. 
#Якщо новина не знайдена, викликається помилка валідації з повідомленням "Article with this ID doesnt exist".