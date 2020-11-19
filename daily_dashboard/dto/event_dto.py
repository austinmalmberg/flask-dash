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
    color_id = event.get('colorId', None)
    background = '#1d1d1d'
    foreground = '#fff'

    if colors and 'colorId' in event:
        background = colors['event'][color_id].get('background')
        foreground = colors['event'][color_id].get('foreground')
    elif colors and not color_id and '#holiday' not in event['organizer'].get('email', ''):
        background = '#4285f4'
        foreground = '#fff'

    event_out['style'] = f"background: {background}; color: {foreground}"

    return event_out


