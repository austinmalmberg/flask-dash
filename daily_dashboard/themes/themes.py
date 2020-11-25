from daily_dashboard.themes import skycons

# grayscale
white = '#fff'
black = '#000'


class BaseTheme:
    # general
    card_opacity = 0.9
    color = white
    background_color = '#03509c'

    # header
    header_background_color = '#0973d6'

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

    def __init__(self):
        self.skycon_colors['moon'] = self.skycon_colors['sun']


''' UNUSED '''
class DarkCloudTheme(BaseTheme):

    def __init__(self):
        super().__init__()

        self.skycon_colors['moon'] = '#ddd'
        self.skycon_colors['light_cloud'] = self.skycon_colors['dark_cloud']
        self.skycon_colors['cloud'] = self.skycon_colors['dark_cloud']
        self.skycon_colors['wind'] = self.skycon_colors['dark_cloud']


''' UNUSED '''
class WhiteCloudTheme(BaseTheme):

    def __init__(self):
        super().__init__()

        self.skycon_colors['moon'] = '#ddd'
        self.skycon_colors['dark_cloud'] = '#ddd'
        self.skycon_colors['light_cloud'] = self.skycon_colors['dark_cloud']
        self.skycon_colors['cloud'] = self.skycon_colors['dark_cloud']
        self.skycon_colors['wind'] = self.skycon_colors['dark_cloud']


class ClearDayTheme(BaseTheme):

    def __init__(self):
        super().__init__()

        self.skycon_description = 'clear_day'
        self.color = black
        self.background_color = '#ffdeb0'
        self.header_background_color = '#578fb3'
        self.header_color = white


class ClearNightTheme(BaseTheme):

    def __init__(self):
        super().__init__()

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
        super().__init__()

        self.skycon_description = 'partly_cloudy_day'
        self.background_color = '#03509c'
        self.header_background_color = '#0973d6'


class PartlyCloudyNightTheme(BaseTheme):

    def __init__(self):
        super().__init__()

        self.skycon_description = 'partly_cloudy_night'
        self.color = '#ffdfb6'
        self.background_color = '#1d1916'
        self.header_background_color = black
        self.event_background_color = self.color


class CloudyTheme(BaseTheme):

    def __init__(self):
        super().__init__()

        self.skycon_description = 'cloudy'
        self.background_color = '#97a3b9'
        self.header_background_color = '#8f8594'
        self.event_background_color = white


class RainTheme(BaseTheme):

    def __init__(self):
        super().__init__()

        self.skycon_description = 'rain'
        self.background_color = '#c5dae5'
        self.color = black
        self.header_background_color = '#2d3436'
        self.header_color = '#dfe6e9'
        self.event_background_color = '#dfe6e9'


class SleetTheme(BaseTheme):

    def __init__(self):
        super().__init__()

        self.skycon_description = 'sleet'
        self.background_color = '#3f3f3f'
        self.header_background_color = '#2d3436'
        self.event_background_color = '#dfe6e9'


class SnowTheme(BaseTheme):

    def __init__(self):
        super().__init__()

        self.skycon_description = 'snow'
        self.background_color = '#84b8de'
        self.header_background_color = '#2980b9'
        self.event_background_color = white


class WindTheme(BaseTheme):

    def __init__(self):
        super().__init__()

        self.skycon_description = 'wind'
        self.background_color = '#f9f7f1'
        self.color = '#331800'
        self.header_background_color = '#d0ba86'
        self.event_background_color = white
        self.temp_hi_color = '#f66'
        self.temp_lo_color = '#66f'


class FogTheme(BaseTheme):

    def __init__(self):
        super().__init__()

        self.skycon_description = 'fog'
        self.background_color = '#8895a6'
        self.color = '#dfe6e9'
        self.header_background_color = '#130f40'
        self.event_background_color = self.color


''' UNUSED '''


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
