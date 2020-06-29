from datetime import datetime, date, timedelta
import pytz

from googleapiclient.discovery import build

from helpers.event_sort import sort_events

# TODO: Add option to fail silently if credentials are invalid or _getservice fails
# Right now, any problem getting the service or executing the action will throw an error or pass along an error


def _getservice(credentials):
    return build('calendar', 'v3', credentials=credentials)


def get_calendar(credentials, calendar_id):
    service = _getservice(credentials)

    calendar = service.calendars().get(calendarId=calendar_id).execute()
    return calendar


def get_calendar_list(credentials):
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

    return { setting['id']: setting['value'] for setting in settings }


def get_events(credentials, calendar_id, date_min=date.today(), range=7):
    """
    Get events of the given calendar. Events are ordered by start time.  If no time range is specified, the time range
    will be set as UTC midnight - 6 days later.

    :param credentials: OAuth 2.0 credentials
    :param calendar_id: The calendar id
    :param date_min: The min date range to get events
    :param range: The date range to query the Google Calendar API for events. range=1 will get events from midnight to
        11:59:59 of the same day
    :return: A list of events, ordered by start time
    """

    # add 6 days to it
    time_min = datetime.combine(date_min, datetime.min.time())
    time_max = time_min + timedelta(days=range, seconds=-1)

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
        event_list += events['items']
        page_token = events.get('nextPageToken')
        if page_token is None:
            break

    return event_list


def get_event_start_dt(event, tz_str):
    start = event['start'].get('dateTime')
    if start:
        return datetime.fromisoformat(start)

    start = event['start'].get('date')
    tz = pytz.timezone(tz_str)
    return tz.fromutc(datetime.fromisoformat(start))


def get_events_from_multiple_calendars(credentials, calendar_ids, date_min=None, time_range=None):
    tz_str = 'America/New_York'

    def event_comparator(event1, event2):
        d1 = get_event_start_dt(event1, tz_str)
        d2 = get_event_start_dt(event2, tz_str)

        if d1 == d2:
            return 0
        elif d1 < d2:
            return -1

        return 1

    kwargs = dict(
        credentials=credentials
    )

    if date_min:
        kwargs['date_min'] = date_min

    if time_range:
        kwargs['range'] = time_range

    res = []
    for calendar_id in calendar_ids:
        kwargs['calendar_id'] = calendar_id
        event_list = get_events(**kwargs)
        res = sort_events(event_comparator, res, event_list)

    return res


def get_colors(credentials):
    service = _getservice(credentials)

    colors = service.colors().get().execute()
    return colors