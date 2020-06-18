from datetime import datetime, timedelta
import pytz

from googleapiclient.discovery import build

from helpers.zip_sorted import zip_sorted

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


def get_events(credentials, calendar_id, options=None):
    """
    Get events of the given calendar. Events are ordered by start time.  If no time range is specified, the time range
    will be set as UTC midnight - 6 days later.

    :param credentials: OAuth 2.0 credentials
    :param calendar_id: The calendar id
    :param options: Optional parameters as defined here: https://developers.google.com/calendar/v3/reference/events/list
        If options is None, time range will be set to:
            - timeMin: today at 12:00AM UTC
            - timeMax: timeMin + 6 days
    :return:
    """

    if options is None:
        # get UTC midnight
        range_min = datetime.combine(datetime.utcnow(), datetime.min.time())

        # add 6 days to it
        range_max = range_min + timedelta(days=7) - timedelta(seconds=1)

        options = {
            'timeMin': f'{str(range_min.isoformat())}Z',
            'timeMax': f'{str(range_max.isoformat())}Z',
        }

    options['orderBy'] = 'startTime'
    options['singleEvents'] = True

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


def get_events_from_multiple_calendars(credentials, calendar_ids, tz_str, options=None):
    def event_comparator(event1, event2):
        d1 = get_event_start_dt(event1, tz_str)
        d2 = get_event_start_dt(event2, tz_str)

        if d1 == d2:
            return 0
        elif d1 < d2:
            return -1

        return 1

    res = []
    for calendar_id in calendar_ids:
        events = get_events(credentials, calendar_id, options)
        res = zip_sorted(event_comparator, res, events)

    return res
