from bs4 import BeautifulSoup as bs
from datetime import datetime
import requests
import argparse

DEBUG = False
URL = "https://www.google.com/search?lr=lang_en&ie=UTF-8&q=weather"
USER_AGENT = "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/110.0.0.0 Safari/537.36"
LANGUAGE = "en-US,en;q=0.5"
TODAY = datetime.today().strftime('%Y%m%d')
# Consent Cookies
COOKIES = {"CONSENT": f"YES+cb.{TODAY}-07-p0.en+FX+410"}

def get_soup(url):
    session = requests.Session()
    session.headers['User-Agent'] = USER_AGENT
    session.headers['Accept-Language'] = LANGUAGE
    session.headers['Content-Language'] = LANGUAGE
    html = session.get(url, cookies=COOKIES)
    if DEBUG:
        with open("tmp.html", 'w') as f:
            f.write(html.text)
    return bs(html.text, "html.parser")

def get_weather_data(url):
    soup = get_soup(url)
    result = {}
    # Get Region
    result['region'] = soup.find("div", attrs={"id": "taw"}).find("div", attrs={'id': True, 'data-ved': True}).find_all('span')[1].text
    # Get Current Weather
    result['temp_now'] = soup.find("span", attrs={"id": "wob_tm"}).text
    result['dayhour'] = soup.find("div", attrs={"id": "wob_dts"}).text
    result['weather_now'] = soup.find("span", attrs={"id": "wob_dc"}).text
    result['precipitation'] = soup.find("span", attrs={"id": "wob_pp"}).text
    result['humidity'] = soup.find("span", attrs={"id": "wob_hm"}).text
    result['wind'] = soup.find("span", attrs={"id": "wob_ws"}).text
    # Get Week Forecast
    next_days = []
    days = soup.find("div", attrs={"id": "wob_dp"})
    for day in days.findAll("div", attrs={"class": "wob_df"}):
        day_name = day.find("div").attrs['aria-label']
        weather = day.find("img").attrs["alt"]
        temp = day.findAll("span", {"class": "wob_t"})
        max_temp = temp[0].text # temp[1].text F
        min_temp = temp[2].text # temp[3].text F
        next_days.append({"name": day_name, "weather": weather, "max_temp": max_temp, "min_temp": min_temp})
    result['next_days'] = next_days
    return result


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Scrape Weather data using Google Weather")
    parser.add_argument("region", nargs="?", help="""Region to get weather for, defaults to your current IP Location""", default="")
    args = parser.parse_args()
    region = args.region
    if region:
        print(f"Weather data for {region}")
        region = region.replace(" ", "+")
        URL += f"+{region}"
    else:
        print("Weather data at your Location\n")
    data = get_weather_data(URL)
    # Print formatted data
    print(f"> {data['region']} | {data['dayhour'].upper()}")
    print(f"Weather: {data['weather_now']}")
    print(f"Temperature: {data['temp_now']}°C")
    print(f"Precipitation: {data['precipitation']}")
    print(f"Humidity: {data['humidity']}")
    print(f"Wind: {data['wind']}")
    print("\nNext days:")
    for dayweather in data['next_days']:
        print(f"> {dayweather['name'].upper()}: {dayweather['weather']} [{dayweather['min_temp']}°C | {dayweather['max_temp']}°C]")
