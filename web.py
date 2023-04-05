from flask import Flask, render_template

from weather import weather_by_city
from org_news import get_news

app = Flask(__name__)

@app.route('/')
def index():
    title = "Weather/News report"
    weather = weather_by_city("Lviv,Ukraine")
    news_list = get_news()
    return render_template('index.html', page_title=title, weather=weather, news_list=news_list)

if __name__ == '__main__':
    app.run(debug=True)   