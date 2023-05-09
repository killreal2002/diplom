from functools import wraps

from flask import current_app, flash, request, redirect, url_for
from flask_login import config, current_user


def admin_required(func):
    @wraps(func)
    def decorated_view(*args, **kwargs):
        if request.method in config.EXEMPT_METHODS or current_app.config.get("LOGIN_DISABLED"):
            pass
        elif not current_user.is_authenticated:
            return current_app.login_manager.unauthorized()
        elif not current_user.is_admin:
            flash('This page is only available to admins')
            return redirect(url_for('news.index'))
        # flask 1.x compatibility
        # current_app.ensure_sync is only available in Flask >= 2.0
        if callable(getattr(current_app, "ensure_sync", None)):
            return current_app.ensure_sync(func)(*args, **kwargs)
        return func(*args, **kwargs)

    return decorated_view

# Kод описує декоратор "admin_required", який можна використовувати в фреймворку Flask для захисту доступу до адміністративних сторінок.
# Функція admin_required приймає іншу функцію (func) в якості параметра, і повертає декоровану функцію (decorated_view). 
# Декорована функція перевіряє, чи є поточний користувач аутентифікованим і чи є він адміністратором. 
# Якщо поточний користувач не є адміністратором, 
# то він буде перенаправлений на головну сторінку з повідомленням "This page is only available to admins".
# Декоратор також містить перевірку на наявність аргументу "ensure_sync" у поточному додатку Flask, і викликає його, якщо він є.