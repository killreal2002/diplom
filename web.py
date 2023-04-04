from flask import Flask

from weather import weather_by_city

app = Flask(__name__)

@app.route('/')
def index():
    weather = weather_by_city("Lviv,Ukraine")
    if weather:
        return f"Weather: {weather['temp_C']} C°, feels like {weather['FeelsLikeC']} C°"
    else:
        return "Weather service temporary unavailible"

if __name__ == '__main__':
    app.run(debug=True)   