import os

basedir = os.path.abspath(os.path.dirname(__file__))

WEATHER_API_KEY = "73c921fc0aa94988af5105517230404"
WEATHER_DEFAULT_CITY= "Lviv,Ukraine"
WEATHER_URL ='http://api.worldweatheronline.com/premium/v1/weather.ashx' 
SQLALCHEMY_DATABASE_URI = 'sqlite:///' + os.path.join(basedir, '..', 'webapp.db')