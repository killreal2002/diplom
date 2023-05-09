from flask import Blueprint, render_template
from webapp.user.decorators import admin_required


blueprint = Blueprint('admin', __name__, url_prefix='/admin')

@blueprint.route('/')
@admin_required
def admin_index():
        title = "Control panel"
        return render_template('admin/index.html', page_title=title)
#Kод створює маршрут "/admin/", який веде до сторінки "Control panel", і доступний лише для користувачів з правами адміністратора, 
#які авторизовані в системі. Для перевірки доступності використовується декоратор @admin_required. 
#Якщо користувач не авторизований або не має прав адміністратора, 
#він буде перенаправлений на сторінку авторизації або на головну сторінку (залежно від налаштувань системи).