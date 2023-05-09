from flask import Flask, render_template
from flask_login import LoginManager
from flask_migrate import Migrate

from webapp.admin.views import blueprint as admin_blueprint
from webapp.news.views import blueprint as news_blueprint
from webapp.db import db
from webapp.user.models import User
from webapp.user.views import blueprint as user_blueprint

def create_app():
    app = Flask(__name__)
    app.config.from_pyfile('config.py')
    db.init_app(app)
    migrate = Migrate(app,db)

    login_manger = LoginManager()
    login_manger.init_app(app)
    login_manger.login_view = 'user.login'
    app.register_blueprint(admin_blueprint)
    app.register_blueprint(user_blueprint)
    app.register_blueprint(news_blueprint)
    
    @login_manger.user_loader
    def load_user(user_id):
        return User.query.get(user_id)

    return app

#Функція create_app() створює Flask додаток з конфігурацією з файлу config.py, 
# підключує базу даних SQLAlchemy та міграції з Flask-Migrate. 
# Далі, ініціалізує об'єкт LoginManager для авторизації користувачів та зареєстровує блюпрінти, 
# які містять маршрути та логіку відповідної частини додатку. Також визначає функцію load_user(), 
# яка повертає об'єкт користувача на основі ідентифікатора користувача.
