from daily_dashboard.themes import skycons

# grayscale
white = '#fff'
black = '#000'

# reds
red = '#f66'

# oranges
orange = '#ff8e69'

# yellows

# greens

# blues
navy = '#03509c'
blue = '#0973d6'
light_blue = '#a4bdfc'

# purples


class ThemeBase:
    name = 'Base'

    # general
    background_color = navy
    card_opacity = 0.9

    # clock
    time_color = white

    # header
    header_background_color = blue
    header_color = white

    # event
    event_background_color = white;

    # weather
    temp_hi_color = red
    temp_curr_color = white
    temp_lo_color = light_blue

    # [ 'main', 'moon', 'fog', 'fogbank', 'light_cloud',
    # 'cloud', 'dark_cloud', 'thunder', 'snow', 'hail',
    # 'sleet', 'wind', 'leaf', 'rain', 'sun' ]
    skycon_colors = skycons.get_color_dict()
    skycon_colors['moon'] = '#ddd'


class ThemeSun(ThemeBase):
    name = 'Sun'

    background_color = '#fffa65'    # sunshine yellow

    time_color = black

    header_background_color = '#ED4C67'     # pink/red
    header_color = black

    temp_hi_color = '#F99F2F'   # orange/yellow
    temp_curr_color = black
    temp_lo_color = '#9980FA'   # lilac purple


def get_all():
    return [
        ThemeBase(),
        ThemeSun()
    ]
