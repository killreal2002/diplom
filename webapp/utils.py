from urllib.parse import urlparse, urljoin
from flask import request

def is_safe_url(target):
    ref_url = urlparse(request.host_url)
    test_url = urlparse(urljoin(request.host_url, target))
    return test_url.scheme in ('http', 'https') and ref_url.netloc == test_url.netloc

def get_redirect_target():
    for target in request.values.get('next'), request.referrer:
        if not target:
            continue
        if is_safe_url(target):
            return target

#Код містить дві функції для перевірки безпеки перенаправлення.
#Функція is_safe_url перевіряє, чи є URL безпечним, якщо поточний хост та хост цільової сторінки співпадають, та використовує протоколи http або https.
#Функція get_redirect_target повертає поточний URL-адрес, що міститься в запиті next або referrer, якщо він безпечний.



