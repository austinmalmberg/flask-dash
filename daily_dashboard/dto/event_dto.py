from datetime import timedelta

from dateutil import parser


def _get_dates_between(start_dt, end_dt):
    """
    Returns a list of dates that the event runs through.

    :param start_dt:
    :param end_dt:
    :return:
    """
    res = []

    date = start_dt
    while date < end_dt:
        res.append(date.strftime('%Y-%m-%d'))
        date += timedelta(days=1)

    return res


def _get_style(colors, color_id):
    """
    Returns a tuple like (backgroundColor, foregroundColor)

    :param colors:
    :param color_id:
    :return:
    """
    return (
        colors['event'][color_id].get('background'),
        colors['event'][color_id].get('foreground')
    )


class EventDto:

    def __init__(self, event, background='#1d1d1d', foreground='#fff', colors=None):
        self.id = event['id']

        temp_start = event['start'].get('dateTime')
        if temp_start is None:
            temp_start = event['start'].get('date')
        self.start_dt = parser.isoparse(temp_start)

        temp_end = event['end'].get('dateTime')
        if temp_end is None:
            temp_end = event['end'].get('date')
        self.end_dt = parser.isoparse(temp_end)

        self.summary = event.get('summary', '(No title)')
        self.htmlLink = event['htmlLink']

        # styling
        self.color_id = event.get('colorId', None)
        if colors and self.color_id:
            self.background, self.foreground = _get_style(colors, self.color_id)
        else:
            self.background = background
            self.foreground = foreground

        self.style = f'background: {self.background}; color: {self.foreground}'

        self.dates = _get_dates_between(self.start_dt, self.end_dt)
