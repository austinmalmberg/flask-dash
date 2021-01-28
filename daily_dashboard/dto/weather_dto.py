from datetime import datetime

from daily_dashboard.theme.themes import get_theme

openweathermap_ids = {
    200: {
        'main': 'Thunderstorm',
        'description': 'thunderstorm with light rain',
        'skycon_descriptions': ['THUNDER_SHOWERS_DAY', 'THUNDER_SHOWERS_NIGHT'],
    },
    201: {
        'main': 'Thunderstorm',
        'description': 'thunderstorm with rain',
        'skycon_descriptions': ['THUNDER_RAIN', 'THUNDER_RAIN'],
    },
    202: {
        'main': 'Thunderstorm',
        'description': 'thunderstorm with heavy rain',
        'skycon_descriptions': ['THUNDER_RAIN', 'THUNDER_RAIN'],
    },
    210: {
        'main': 'Thunderstorm',
        'description': 'light thunderstorm',
        'skycon_descriptions': ['THUNDER_RAIN', 'THUNDER_RAIN'],
    },
    211: {
        'main': 'Thunderstorm',
        'description': 'thunderstorm',
        'skycon_descriptions': ['THUNDER_RAIN', 'THUNDER_RAIN'],
    },
    212: {
        'main': 'Thunderstorm',
        'description': 'heavy thunderstorm',
        'skycon_descriptions': ['THUNDER_RAIN', 'THUNDER_RAIN'],
    },
    221: {
        'main': 'Thunderstorm',
        'description': 'ragged thunderstorm',
        'skycon_descriptions': ['THUNDER_RAIN', 'THUNDER_RAIN'],
    },
    230: {
        'main': 'Thunderstorm',
        'description': 'thunderstorm with light drizzle',
        'skycon_descriptions': ['THUNDER_RAIN', 'THUNDER_RAIN'],
    },
    231: {
        'main': 'Thunderstorm',
        'description': 'thunderstorm with drizzle',
        'skycon_descriptions': ['THUNDER_RAIN', 'THUNDER_RAIN'],
    },
    232: {
        'main': 'Thunderstorm',
        'description': 'thunderstorm with heavy drizzle',
        'skycon_descriptions': ['THUNDER_RAIN', 'THUNDER_RAIN'],
    },
    300: {
        'main': 'Drizzle',
        'description': 'light intensity drizzle',
        'skycon_descriptions': ['RAIN', 'RAIN'],
    },
    301: {
        'main': 'Drizzle',
        'description': 'drizzle',
        'skycon_descriptions': ['RAIN', 'RAIN'],
    },
    302: {
        'main': 'Drizzle',
        'description': 'heavy intensity drizzle',
        'skycon_descriptions': ['RAIN', 'RAIN'],
    },
    310: {
        'main': 'Drizzle',
        'description': 'light intensity drizzle rain',
        'skycon_descriptions': ['RAIN', 'RAIN'],
    },
    311: {
        'main': 'Drizzle',
        'description': 'drizzle rain',
        'skycon_descriptions': ['RAIN', 'RAIN'],
    },
    312: {
        'main': 'Drizzle',
        'description': 'heavy intensity drizzle rain',
        'skycon_descriptions': ['RAIN', 'RAIN'],
    },
    313: {
        'main': 'Drizzle',
        'description': 'shower rain and drizzle',
        'skycon_descriptions': ['SHOWERS_DAY', 'SHOWERS_NIGHT'],
    },
    314: {
        'main': 'Drizzle',
        'description': 'heavy shower rain and drizzle',
        'skycon_descriptions': ['RAIN', 'RAIN'],
    },
    321: {
        'main': 'Drizzle',
        'description': 'shower drizzle',
        'skycon_descriptions': ['SHOWERS_DAY', 'SHOWERS_NIGHT'],
    },
    500: {
        'main': 'Rain',
        'description': 'light rain',
        'skycon_descriptions': ['RAIN', 'RAIN'],
    },
    501: {
        'main': 'Rain',
        'description': 'moderate rain',
        'skycon_descriptions': ['RAIN', 'RAIN'],
    },
    502: {
        'main': 'Rain',
        'description': 'heavy intensity rain',
        'skycon_descriptions': ['RAIN', 'RAIN'],
    },
    503: {
        'main': 'Rain',
        'description': 'very heavy rain',
        'skycon_descriptions': ['RAIN', 'RAIN'],
    },
    504: {
        'main': 'Rain',
        'description': 'extreme rain',
        'skycon_descriptions': ['RAIN', 'RAIN'],
    },
    511: {
        'main': 'Rain',
        'description': 'freezing rain',
        'skycon_descriptions': ['SLEET', 'SLEET'],
    },
    520: {
        'main': 'Rain',
        'description': 'light intensity shower rain',
        'skycon_descriptions': ['SHOWERS_DAY', 'SHOWERS_NIGHT'],
    },
    521: {
        'main': 'Rain',
        'description': 'shower rain',
        'skycon_descriptions': ['SHOWERS_DAY', 'SHOWERS_NIGHT'],
    },
    522: {
        'main': 'Rain',
        'description': 'heavy intensity shower rain',
        'skycon_descriptions': ['RAIN', 'RAIN'],
    },
    531: {
        'main': 'Rain',
        'description': 'ragged shower rain',
        'skycon_descriptions': ['RAIN', 'RAIN'],
    },
    600: {
        'main': 'Snow',
        'description': 'light snow',
        'skycon_descriptions': ['SNOW_SHOWERS_DAY', 'SNOW_SHOWERS_NIGHT'],
    },
    601: {
        'main': 'Snow',
        'description': 'Snow',
        'skycon_descriptions': ['SNOW', 'SNOW'],
    },
    602: {
        'main': 'Snow',
        'description': 'Heavy snow',
        'skycon_descriptions': ['SNOW', 'SNOW'],
    },
    611: {
        'main': 'Snow',
        'description': 'Sleet',
        'skycon_descriptions': ['SLEET', 'SLEET'],
    },
    612: {
        'main': 'Snow',
        'description': 'Light shower sleet',
        'skycon_descriptions': ['SLEET', 'SLEET'],
    },
    613: {
        'main': 'Snow',
        'description': 'Shower sleet',
        'skycon_descriptions': ['SLEET', 'SLEET'],
    },
    615: {
        'main': 'Snow',
        'description': 'Light rain and snow',
        'skycon_descriptions': ['RAIN_SNOW_SHOWERS_DAY', 'RAIN_SNOW_SHOWERS_NIGHT'],
    },
    616: {
        'main': 'Snow',
        'description': 'Rain and snow',
        'skycon_descriptions': ['RAIN_SNOW', 'RAIN_SNOW'],
    },
    620: {
        'main': 'Snow',
        'description': 'Light shower snow',
        'skycon_descriptions': ['SNOW_SHOWERS_DAY', 'SNOW_SHOWERS_NIGHT'],
    },
    621: {
        'main': 'Snow',
        'description': 'Shower snow',
        'skycon_descriptions': ['SNOW_SHOWERS_DAY', 'SNOW_SHOWERS_NIGHT'],
    },
    622: {
        'main': 'Snow',
        'description': 'Heavy shower snow',
        'skycon_descriptions': ['SNOW', 'SNOW'],
    },
    701: {
        'main': 'Mist',
        'description': 'mist',
        'skycon_descriptions': ['FOG', 'FOG'],
    },
    711: {
        'main': 'Smoke',
        'description': 'Smoke',
        'skycon_descriptions': ['FOG', 'FOG'],
    },
    721: {
        'main': 'Haze',
        'description': 'Haze',
        'skycon_descriptions': ['FOG', 'FOG'],
    },
    731: {
        'main': 'Dust',
        'description': 'sand/ dust whirls',
        'skycon_descriptions': ['FOG', 'FOG'],
    },
    741: {
        'main': 'Fog',
        'description': 'fog',
        'skycon_descriptions': ['FOG', 'FOG'],
    },
    751: {
        'main': 'Sand',
        'description': 'sand',
        'skycon_descriptions': ['FOG', 'FOG'],
    },
    761: {
        'main': 'Dust',
        'description': 'dust',
        'skycon_descriptions': ['FOG', 'FOG'],
    },
    762: {
        'main': 'Ash',
        'description': 'volcanic ash',
        'skycon_descriptions': ['FOG', 'FOG'],
    },
    771: {
        'main': 'Squall',
        'description': 'squalls',
        'skycon_descriptions': ['WIND', 'WIND'],
    },
    781: {
        'main': 'Tornado',
        'description': 'tornado',
        'skycon_descriptions': ['WIND', 'WIND'],
    },
    800: {
        'main': 'Clear',
        'description': 'clear sky',
        'skycon_descriptions': ['CLEAR_DAY', 'CLEAR_NIGHT'],
    },
    801: {
        'main': 'Clouds',
        'description': 'few clouds: 11-25%',
        'skycon_descriptions': ['PARTLY_CLOUDY_DAY', 'PARTLY_CLOUDY_NIGHT'],
    },
    802: {
        'main': 'Clouds',
        'description': 'scattered clouds: 25-50%',
        'skycon_descriptions': ['PARTLY_CLOUDY_DAY', 'PARTLY_CLOUDY_NIGHT'],
    },
    803: {
        'main': 'Clouds',
        'description': 'broken clouds: 51-84%',
        'skycon_descriptions': ['CLOUDY', 'CLOUDY'],
    },
    804: {
        'main': 'Clouds',
        'description': 'overcast clouds: 85-100%',
        'skycon_descriptions': ['CLOUDY', 'CLOUDY'],
    },
}


def get_skycon_descriptions(openweathermap_id):
    if openweathermap_id in openweathermap_ids:
        return openweathermap_ids[openweathermap_id]['skycon_descriptions']

    return 'FOG'


class WeatherDto:

    def __init__(self, forecast):
        self.date = datetime.fromtimestamp(forecast['dt']).date()

        # temp
        self.lo = round(forecast['temp']['min'])
        self.hi = round(forecast['temp']['max'])

        # timings
        self.sunrise = datetime.fromtimestamp(forecast['sunrise'])
        self.sunset = datetime.fromtimestamp(forecast['sunset'])

        # weather
        self.weather_id = forecast['weather'][0]['id']
        self.skycon_descriptions = get_skycon_descriptions(self.weather_id)
        # self.cloud_pct = forecast['clouds']
        # self.weather_condition = forecast['weather'][0]['main']
        # self.weather_description = forecast['weather'][0]['description']
        # self.wind_speed = forecast['wind_speed']

    def get_skycon_description(self):
        return self.skycon_descriptions[0]


class CurrentWeatherDto(WeatherDto):

    def __init__(self, forecast, current):
        super().__init__(forecast)

        # overrides
        self.weather_id = current['weather'][0]['id']
        self.skycon_descriptions = get_skycon_descriptions(self.weather_id)
        self.sunrise = datetime.fromtimestamp(current['sunrise'])
        self.sunset = datetime.fromtimestamp(current['sunset'])

        self.is_current = True
        self.dt = datetime.fromtimestamp(current['dt'])
        self.curr_temp = round(current['temp'])
        self.weather_id = current['weather'][0]['id']

        # self.cloud_pct = current['clouds']
        # self.weather_condition = current['weather'][0]['main']
        # self.weather_description = current['weather'][0]['description']
        # self.wind_speed = current['wind_speed']

        # self.theme = get_theme(self.weather_id)

    def get_skycon_description(self):
        if self.sunrise < self.dt < self.sunset:
            return self.skycon_descriptions[0]

        return self.skycon_descriptions[1]

