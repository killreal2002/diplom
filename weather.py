import requests

from settings import WEATHER_API_KEY

def weather_by_city(city_name):
    weather_url = 'http://api.worldweatheronline.com/premium/v1/weather.ashx'
    params = {
        'key' : WEATHER_API_KEY,
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
    w = weather_by_city("Kyiv,Ukraine")
    print(w)