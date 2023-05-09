from webapp.user.forms import LoginForm, RegistrationForm
from webapp.user.models import User
from webapp.db import db

from flask import Blueprint, flash, redirect, url_for, render_template
from flask_login import current_user, login_user, logout_user
from webapp.utils import get_redirect_target

blueprint= Blueprint('user', __name__, url_prefix='/users')

@blueprint.route('/login')
def login():
    if current_user.is_authenticated:
        return redirect(get_redirect_target())
    title = 'Authorization'
    login_form = LoginForm()
    return render_template('user/login.html', page_title = title, form = login_form)

@blueprint.route('/process-login', methods=['POST'])
def process_login():
    form = LoginForm()

    if form.validate_on_submit():
        user = User.query.filter(User.username == form.username.data).first()
        if user and user.check_password(form.password.data):
            login_user(user, remember=form.remember_me.data)
            flash("You are logged in")
            return redirect(url_for('news.index'))
      
    flash('Mistake in username or password')
    return redirect(url_for('user.login'))

@blueprint.route('/logout')
def logout():
    logout_user()
    flash('Logged out')
    return redirect(url_for('news.index'))

@blueprint.route('/register')
def register():
    if current_user.is_authenticated:
        return redirect(url_for('news.index'))
    title = 'Registration'
    form = RegistrationForm()
    return render_template('user/registration.html', page_title = title, form = form)

@blueprint.route('/process-reg', methods=['POST'])
def process_reg():
    form = RegistrationForm()
    if form.validate_on_submit():
        news_user = User(username=form.username.data, email=form.email.data, role='user')
        news_user.set_password(form.password.data)
        db.session.add(news_user)
        db.session.commit()
        flash('You are passed a registration')
        return redirect(url_for('user.login'))
    else:
        for field, errors in form.errors.items():
            for error in errors:
                flash('Problem in {} : {}'.format(
                    getattr(form,field).label.text,
                    error
                ))
        flash('Please correct the errors in the form')
        return redirect(url_for('user.register'))

#код для Flask-блупрінту, який обробляє сторінки веб-додатку пов'язані з аутентифікацією та реєстрацією користувачів.
#Перші дві функції - це сторінки для входу користувача. 
# Функція login показує сторінку входу, а функція process_login перевіряє, чи вірні введені ім'я користувача та пароль. 
# Якщо вони вірні, вона залогінює користувача та перенаправить його на сторінку з новинами. 
# В іншому випадку вона поверне його на сторінку входу з помилкою.
#Функція logout від'єднує користувача від системи та перенаправляє його на головну сторінку з повідомленням про вихід.
#Функції register та process_reg відповідають за реєстрацію користувача. Функція register показує сторінку реєстрації, 
# а функція process_reg перевіряє правильність введених даних та додає нового користувача в базу даних, 
# якщо вони вірні. Якщо ж дані не вірні, 
# вона повертає користувача на сторінку реєстрації з відповідною помилкою.
#В цьому коді також використовується шаблонизатор Jinja2 для рендерингу HTML-сторінок.