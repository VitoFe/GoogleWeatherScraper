from flask import Flask, render_template, request
from weather import get_weather_data

app = Flask(__name__)

@app.route('/', methods=['GET', 'POST'])
def index():
    if request.method == 'POST':
        region = request.form['region']
        if region:
            print(f"Weather data for {region}")
            region = region.replace(" ", "+")
            url = f"https://www.google.com/search?lr=lang_en&ie=UTF-8&q=weather+{region}"
        else:
            print("Weather data at your Location\n")
            url = "https://www.google.com/search?lr=lang_en&ie=UTF-8&q=weather"
        data = get_weather_data(url)
        return render_template('weather.html', data=data)
    return render_template('index.html')

if __name__ == '__main__':
    app.run(debug=True)
