from flask import Flask, render_template, flash, redirect, url_for
from flask_login import LoginManager, current_user, login_required, login_user, logout_user

from webapp.weather import weather_by_city
from  webapp.model import db, News, User
from webapp.forms import LoginForm

def create_app():
    app = Flask(__name__)
    app.config.from_pyfile('config.py')
    db.init_app(app)

    login_manger = LoginManager()
    login_manger.init_app(app)
    login_manger.login_view = 'login'

    @login_manger.user_loader
    def load_user(user_id):
        return User.query.get(user_id)

    @app.route('/')
    def index():
        title = "Weather/News report"
        weather = weather_by_city(app.config['WEATHER_DEFAULT_CITY'])
        news_list = News.query.order_by(News.published.desc()).all()
        return render_template('index.html', page_title=title, weather=weather, news_list=news_list)

    @app.route('/login')
    def login():
        if current_user.is_authenticated:
            return redirect(url_for('index'))
        title = 'Authorization'
        login_form = LoginForm()
        return render_template('login.html', page_title = title, form = login_form)

    @app.route('/process-login', methods=['POST'])
    def process_login():
        form = LoginForm()

        if form.validate_on_submit():
            user = User.query.filter(User.username == form.username.data).first()
            if user and user.check_password(form.password.data):
                login_user(user)
                flash("You have been logined")
                return redirect(url_for('index'))
            
        flash('Mistake in username or password')
        return redirect(url_for('login'))

    @app.route('/logout')
    def logout():
        logout_user()
        flash('Logged out')
        return redirect(url_for('index'))
    
    @app.route('/admin')
    @login_required
    def admin_index():
        if current_user.is_admin:
            return "Hello admin"
        else:
            return "You not the admin"
    
    return app
