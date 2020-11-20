from datetime import timedelta
from dateutil import parser

from daily_dashboard.dto.mapper import obj_mapper


def event_dto(event, colors=None):
    key_info = [
        {
            'name': 'id',
        },
        {
            'name': 'start',
        },
        {
            'name': 'end',
        },
        {
            'name': 'summary',
            'default': '(No title)'
        },
        {
            'name': 'htmlLink'
        }
    ]

    event_out = obj_mapper(event, key_info)

    # add the styling
    background = '#1d1d1d'
    foreground = '#fff'

    if colors:
        color_id = event.get('colorId', None)

        if 'colorId' in event:
            background = colors['event'][color_id].get('background')
            foreground = colors['event'][color_id].get('foreground')
        elif not color_id and '#holiday' not in event['organizer'].get('email', ''):
            background = '#4285f4'
            foreground = '#fff'

    event_out['style'] = f"background: {background}; color: {foreground}"

    event_out['dates'] = []
    start_date = parser.isoparse(event['start'].get('dateTime', event['start'].get('date')))
    end_date = parser.isoparse(event['end'].get('dateTime', event['end'].get('date')))
    date = start_date
    while date < end_date:
        event_out['dates'].append(date.strftime('%Y-%m-%d'))
        date += timedelta(days=1)

    return event_out
