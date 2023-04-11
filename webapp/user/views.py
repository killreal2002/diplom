from webapp.user.forms import LoginForm
from webapp.user.models import User

from flask import Blueprint, flash, redirect, url_for, render_template
from flask_login import current_user, login_user, logout_user

blueprint= Blueprint('user', __name__, url_prefix='/users')

@blueprint.route('/login')
def login():
    if current_user.is_authenticated:
        return redirect(url_for('news.index'))
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
            flash("You have been logined")
            return redirect(url_for('news.index'))
        
    flash('Mistake in username or password')
    return redirect(url_for('user.login'))

@blueprint.route('/logout')
def logout():
    logout_user()
    flash('Logged out')
    return redirect(url_for('news.index'))