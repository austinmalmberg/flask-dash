descriptions = {
    'clear_day',
    'clear_night',
    'partly_cloudy_day',
    'partly_cloudy_night',
    'cloudy',
    'rain',
    'showers_day',
    'showers_night',
    'sleet',
    'rain_snow',
    'rain_snow_showers_day',
    'rain_snow_showers_night',
    'snow',
    'snow_showers_night',
    'wind',
    'fog',
    'thunder',
    'thunder_rain',
    'thunder_showers_day',
    'thunder_showers_night',
    'hail'
}

components = [
    'main', 'moon', 'fog', 'fogbank', 'light_cloud',
    'cloud', 'dark_cloud', 'thunder', 'snow', 'hail',
    'sleet', 'wind', 'leaf', 'rain', 'sun'
]

default_colors = [
    "#111", "#353545", "#CCC", "#AAA", "#888",
    "#666", "#444", "#FF0", "#C2EEFF", "#CCF",
    "#C2EEFF", "#777", "#2C5228", "#7FDBFF", "#FFDC00"
]


def get_color_dict(colors=None):
    if not colors:
        colors = default_colors
    elif len(colors) != len(components):
        raise ValueError('len(colors) did not match len(components)')

    return {item: default_colors[i] for i, item in enumerate(components)}


