from datetime import datetime, date, timedelta

from googleapiclient.discovery import build

from daily_dashboard.helpers.event_sort import sort_events


# TODO: Add option to fail silently if credentials are invalid or _getservice fails
# Right now, any problem getting the service or executing the action will throw an error or pass along an error


def _getservice(credentials):
    return build('calendar', 'v3', credentials=credentials)


def get_calendar(credentials, calendar_id):
    service = _getservice(credentials)

    calendar = service.calendars().get(calendarId=calendar_id).execute()
    return calendar


def get_calendar_list(credentials):
    """

    :param credentials: Google.oauth.credentials.Credentials
    :return: An array of CalendarList resources as shown here:
        https://developers.google.com/calendar/v3/reference/calendarList#resource
    """
    service = _getservice(credentials)
    calendars = []

    page_token = None
    while True:
        calendar_list = service.calendarList().list(pageToken=page_token).execute()
        calendars += calendar_list['items']
        page_token = calendar_list.get('nextPageToken')
        if page_token is None:
            break

    return calendars


def get_calendar_settings(credentials):
    service = _getservice(credentials)
    settings = []

    page_token = None
    while True:
        settings_list = service.settings().list(pageToken=page_token).execute()
        settings += settings_list['items']
        page_token = settings_list.get('nextPageToken')
        if page_token is None:
            break

    return {setting['id']: setting['value'] for setting in settings}


def get_colors(credentials):
    service = _getservice(credentials)

    colors = service.colors().get().execute()
    return colors


def _event_parser(event, colors=None):
    colorId = event.get('colorId')

    res = dict(
        id=event['id'],
        start=event['start'],
        end=event['end'],
        summary=event.get('summary', '(No title)'),
        colorId=colorId,
        htmlLink=event['htmlLink']
    )

    if colors and colorId:
        res['background'] = colors['event'][colorId].get('background')
        res['foreground'] = colors['event'][colorId].get('foreground')
    elif colors and not colorId and '#holiday' not in event['organizer'].get('email', ''):
        res['background'] = '#4285f4'
        res['foreground'] = '#fff'
    else:
        res['background'] = '#1d1d1d'
        res['foreground'] = '#fff'

    return res


def get_events(credentials, calendar_id, colors=None, date_min=date.today(), max_days=7):
    """
    Get events of the given calendar. Events are ordered by start time.  If no time range is specified, the time range
    will be set as UTC midnight through 6 days later at 11:59.59 PM.

    :param credentials: OAuth 2.0 credentials
    :param calendar_id: The calendar id
    :param date_min: The min date range to get events
    :param max_days: The date range to query the Google Calendar API for events. range=1 will get events from midnight to
        11:59:59 of the same day
    :return: A list of events, ordered by start time
    """
    if not colors:
        colors = get_colors(credentials)

    # add 6 days to it
    time_min = datetime.combine(date_min, datetime.min.time())
    time_max = time_min + timedelta(days=max_days, seconds=-1)

    options = {
        'timeMin': f'{str(time_min.isoformat())}Z',
        'timeMax': f'{str(time_max.isoformat())}Z',
        'orderBy': 'startTime',
        'singleEvents': True
    }

    service = _getservice(credentials)

    event_list = []
    page_token = None
    while True:
        events = service.events().list(calendarId=calendar_id, **options).execute()
        for event in events['items']:
            event_list.append(_event_parser(event, colors=colors))
        page_token = events.get('nextPageToken')
        if page_token is None:
            break

    return event_list


def get_events_from_multiple_calendars(credentials, calendar_ids, date_min=None, max_days=None):
    def event_comparator(event1, event2):
        # set dates to value from start.dateTime or start.date (in the case of all/multi-day events)
        d1 = datetime.fromisoformat(
            event1['start'].get('dateTime', event1['start'].get('date'))
        )

        d2 = datetime.fromisoformat(
            event2['start'].get('dateTime', event2['start'].get('date'))
        )

        if d1.timestamp() == d2.timestamp():
            return 0

        return -1 if d1.timestamp() < d2.timestamp() else 1

    kwargs = dict(
        credentials=credentials
    )

    if date_min:
        kwargs['date_min'] = date_min

    if max_days:
        kwargs['max_days'] = max_days

    kwargs['colors'] = get_colors(credentials)

    res = []
    for calendar_id in calendar_ids:
        kwargs['calendar_id'] = calendar_id
        event_list = get_events(**kwargs)
        res = sort_events(event_comparator, res, event_list)

    return res
