from datetime import datetime

from daily_dashboard.themes.themes import get_theme


class WeatherDto:

    def __init__(self, forecast, current=None):
        self.date = datetime.fromtimestamp(forecast['dt']).date()

        # temp
        self.lo = round(forecast['temp']['min'])
        self.hi = round(forecast['temp']['max'])

        # timings
        self.sunrise = datetime.fromtimestamp(forecast['sunrise'])
        self.sunset = datetime.fromtimestamp(forecast['sunset'])

        # weather
        self.cloud_pct = forecast['clouds']
        self.weather_id = forecast['weather'][0]['id']
        self.weather_condition = forecast['weather'][0]['main']
        self.weather_description = forecast['weather'][0]['description']
        self.wind_speed = forecast['wind_speed']

        if current:
            self.current = CurrentWeatherDto(current)


class CurrentWeatherDto:

    def __init__(self, current):
        self.cloud_pct = current['clouds']
        self.temp = round(current['temp'])
        self.weather_id = current['weather'][0]['id']
        self.weather_condition = current['weather'][0]['main']
        self.weather_description = current['weather'][0]['description']
        self.wind_speed = current['wind_speed']

        self.theme = get_theme(self.weather_id)
