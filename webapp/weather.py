import requests

from flask import current_app


def weather_by_city(city_name):
    weather_url = current_app.config['WEATHER_URL']
    params = {
        'key' : current_app.config['WEATHER_API_KEY'],
        'q' : city_name,
        "format" : "json",
        "num_of_days" : 1,
        "lang" : "uk"
    }
    try:
        result = requests.get(weather_url, params=params)
        result.raise_for_status()
        weather = result.json()
        if 'data' in weather:
            if "current_condition" in weather['data']:
                try:
                    return weather['data']['current_condition'][0]
                except(IndexError, TypeError):
                    return False
    except(requests.RequestException, ValueError):
        print('Net eror')
        return False
    return False

if __name__ == '__main__':
    w = current_app.config['WEATHER_API_KEY']
    print(w)

#Код здійснює запит до API погоди, передаючи місто, та повертає дані про поточну погоду для нього.
#Якщо запит не вдається або немає даних про поточну погоду, повертається False.
