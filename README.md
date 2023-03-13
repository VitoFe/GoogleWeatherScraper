# GoogleWeatherScraper
Python script to scrape weather data from Google using the Beautiful Soup library. The script extracts weather data for a given region, or if no region is specified, for the user's current IP location.

The script outputs the following weather data:
- Region
- Date and time
- Current weather
- Temperature
- Precipitation
- Humidity
- Wind speed
- Week weather forecast

### Dependencies
- Python 3.x
- requests
- BeautifulSoup

### Usage
`python weather.py [region]`

#### Arguments
- `region` (optional): The region to get weather for. If not specified, the script will get weather data for the user's current IP location.

#### Example
- `python weather.py New York`

This command will get the weather data for New York.
