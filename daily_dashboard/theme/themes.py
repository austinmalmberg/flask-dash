from daily_dashboard.theme import skycons

# grayscale
white = '#fff'
black = '#000'


class BaseTheme:
    # general
    card_opacity = 0.9
    color = white
    background_color = '#03509c'
    background_image = None

    # header
    header_background_color = '#0973d6'
    header_color = black

    # event
    event_background_color = white

    # weather
    temp_hi_color = '#f99'
    temp_lo_color = '#a4bdfc'

    skycon_description = None

    # [ 'main', 'moon', 'fog', 'fogbank', 'light_cloud',
    # 'cloud', 'dark_cloud', 'thunder', 'snow', 'hail',
    # 'sleet', 'wind', 'leaf', 'rain', 'sun' ]
    skycon_colors = skycons.default_colors

    def __init__(self, name='Base'):
        self.name = name
        self.skycon_colors['moon'] = self.skycon_colors['sun']

    def general_style(self):
        return f'color: {self.color}; background-color: {self.background_color}; opacity: {self.card_opacity};' + \
            f' background-image: url({self.background_image});' if self.background_image else ''

    def header_style(self):
        return f'color: {self.header_color}; background-color: {self.header_background_color};'

    def event_container_style(self):
        return f'background-color: {self.event_background_color};'

    def temp_hi_style(self):
        return f'color: {self.temp_hi_color};'

    def temp_lo_style(self):
        return f'color: {self.temp_lo_color};'


class DarkCloudTheme(BaseTheme):
    ''' UNUSED '''

    def __init__(self):
        super().__init__('DarkCloud')

        self.skycon_colors['moon'] = '#ddd'
        self.skycon_colors['light_cloud'] = self.skycon_colors['dark_cloud']
        self.skycon_colors['cloud'] = self.skycon_colors['dark_cloud']
        self.skycon_colors['wind'] = self.skycon_colors['dark_cloud']


class WhiteCloudTheme(BaseTheme):
    ''' UNUSED '''

    def __init__(self):
        super().__init__('WhiteCloud')

        self.skycon_colors['moon'] = '#ddd'
        self.skycon_colors['dark_cloud'] = '#ddd'
        self.skycon_colors['light_cloud'] = self.skycon_colors['dark_cloud']
        self.skycon_colors['cloud'] = self.skycon_colors['dark_cloud']
        self.skycon_colors['wind'] = self.skycon_colors['dark_cloud']


class ClearDayTheme(BaseTheme):

    def __init__(self):
        super().__init__('ClearDay')

        self.skycon_description = 'clear_day'
        self.color = black
        self.background_color = '#ffdeb0'
        self.header_background_color = '#578fb3'
        self.header_color = white


class ClearNightTheme(BaseTheme):

    def __init__(self):
        super().__init__('ClearNight')

        self.skycon_description = 'clear_night'
        self.background_color = '#081426'
        self.color = '#d2dae2'
        self.header_background_color = self.color
        self.header_color = black
        self.event_background_color = '#2C3a47'
        self.temp_hi_color = '#f66'
        self.temp_lo_color = '#66f'


class PartlyCloudyDayTheme(BaseTheme):

    def __init__(self):
        super().__init__('PartlyCloudyDay')

        self.skycon_description = 'partly_cloudy_day'
        self.background_color = '#03509c'
        self.header_background_color = '#0973d6'


class PartlyCloudyNightTheme(BaseTheme):

    def __init__(self):
        super().__init__('PartlyCloudyNight')

        self.skycon_description = 'partly_cloudy_night'
        self.color = '#ffdfb6'
        self.background_color = '#1d1916'
        self.header_background_color = black
        self.event_background_color = self.color


class CloudyTheme(BaseTheme):

    def __init__(self):
        super().__init__('Cloudy')

        self.skycon_description = 'cloudy'
        self.background_color = '#97a3b9'
        self.header_background_color = '#8f8594'
        self.event_background_color = white


class RainTheme(BaseTheme):

    def __init__(self):
        super().__init__('Rain')

        self.skycon_description = 'rain'
        self.background_color = '#c5dae5'
        self.color = black
        self.header_background_color = '#2d3436'
        self.header_color = '#dfe6e9'
        self.event_background_color = '#dfe6e9'


class SleetTheme(BaseTheme):

    def __init__(self):
        super().__init__('Sleet')

        self.skycon_description = 'sleet'
        self.background_color = '#3f3f3f'
        self.header_background_color = '#2d3436'
        self.event_background_color = '#dfe6e9'


class SnowTheme(BaseTheme):

    def __init__(self):
        super().__init__('Snow')

        self.skycon_description = 'snow'
        self.background_color = '#84b8de'
        self.header_background_color = '#2980b9'
        self.event_background_color = white


class WindTheme(BaseTheme):

    def __init__(self):
        super().__init__('Wind')

        self.skycon_description = 'wind'
        self.background_color = '#f9f7f1'
        self.color = '#331800'
        self.header_background_color = '#d0ba86'
        self.event_background_color = white
        self.temp_hi_color = '#f66'
        self.temp_lo_color = '#66f'


class FogTheme(BaseTheme):

    def __init__(self):
        super().__init__('Fog')

        self.skycon_description = 'fog'
        self.background_color = '#8895a6'
        self.color = '#dfe6e9'
        self.header_background_color = '#130f40'
        self.event_background_color = self.color


''' NOT IMPLEMENTED '''


class ShowersDayTheme(BaseTheme):
    pass


class ShowersNightTheme(BaseTheme):
    pass


class RainSnowTheme(BaseTheme):
    pass


class RainSnowShowersDayTheme(BaseTheme):
    pass


class RainSnowShowersNightTheme(BaseTheme):
    pass


class SnowShowersNightTheme(BaseTheme):
    pass


class ThunderTheme(BaseTheme):
    pass


class ThunderRainTheme(BaseTheme):
    pass


class ThunderShowersDayTheme(BaseTheme):
    pass


class ThunderShowersNightTheme(BaseTheme):
    pass


class HailTheme(BaseTheme):
    pass


def get_theme(condition_id, is_day=True):
    """
    Weather conditions found here: https://openweathermap.org/weather-conditions

    :param condition_id: the condition id
    :param is_day: usually calculated by finding whether the current time is between sunrise and sunset
    :return: the weather theme
    """
    return RainTheme()

    if condition_id < 200 or condition_id == 800:
        return ClearDayTheme() if is_day else ClearNightTheme()

    if condition_id < 600:
        return RainTheme()

    if condition_id < 700:
        return SnowTheme()

    if condition_id < 800:
        return FogTheme()

    return PartlyCloudyDayTheme() if is_day else PartlyCloudyNightTheme()


def get_all():
    return [
        BaseTheme(),
        ClearDayTheme(),
        ClearNightTheme(),
        PartlyCloudyDayTheme(),
        PartlyCloudyNightTheme(),
        CloudyTheme(),
        RainTheme(),
        SleetTheme(),
        SnowTheme(),
        WindTheme(),
        FogTheme(),
        # HailTheme(),
        # SnowShowersNightTheme(),
        # ShowersDayTheme(),
        # ShowersNightTheme(),
        # RainSnowTheme(),
        # RainSnowShowersDayTheme(),
        # RainSnowShowersNightTheme(),
        # ThunderTheme(),
        # ThunderRainTheme(),
        # ThunderShowersDayTheme(),
        # ThunderShowersNightTheme(),
    ]
