from datetime import datetime, date, timedelta
from dateutil import parser
from pytz import all_timezones

from googleapiclient.discovery import build

from daily_dashboard.util.merge_lists import merge_sorted_lists


def _string_to_dt(s):
    return parser.isoparse(s)


# TODO: Add option to fail silently if credentials are invalid or _getservice fails
# TODO: Right now, any problem getting the service or executing the action will throw an error or pass along an error
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


def get_events(credentials, calendar_id, dt_min=date.today(), max_days=7, timezone=None):
    """
    Get events of the given calendar. Events are ordered by start time.  If no time range is specified, the time range
    will be set as UTC midnight through 6 days later at 11:59.59 PM.

    :param credentials: OAuth 2.0 credentials
    :param calendar_id: The calendar id
    :param dt_min: The min date range to get events
    :param max_days: The date range to query the Google Calendar API for events. range=1 will get events from midnight to
        11:59:59 of the same day
    :param timezone: The timezone used in the event list response
    :return: A list of events, ordered by start time
    """
    # chop the time from dt_min
    date_min = datetime.combine(dt_min, datetime.min.time())
    # get the upper bound
    time_max = date_min + timedelta(days=min(max_days, 31), seconds=-1)

    options = {
        'timeMin': date_min.isoformat() + 'Z',
        'timeMax': time_max.isoformat() + 'Z',
        'orderBy': 'startTime',
        'singleEvents': True,
        'maxResults': min(250, max_days * 10)
    }

    if timezone and timezone in all_timezones:
        options['timeZone'] = timezone

    service = _getservice(credentials)

    event_list = []
    page_token = None
    while True:
        events = service.events().list(calendarId=calendar_id, **options).execute()
        for event in events['items']:
            event_list.append(event)
        page_token = events.get('nextPageToken')
        if page_token is None:
            break

    return event_list


def get_events_from_multiple_calendars(credentials, calendar_ids, dt_min=None, max_days=None, timezone=None):
    def event_comparator(event1, event2):
        event1_start = _string_to_dt(event1['start'].get('dateTime', event1['start'].get('date')))
        event2_start = _string_to_dt(event2['start'].get('dateTime', event2['start'].get('date')))

        # a negative value if event1 starts first
        start_diff = event1_start.timestamp() - event2_start.timestamp()

        # if they start at the same time, compare ending times
        # order by the event ending first
        if start_diff == 0:
            event1_end = _string_to_dt(event1['end'].get('dateTime', event1['end'].get('date')))
            event2_end = _string_to_dt(event2['end'].get('dateTime', event2['end'].get('date')))

            return event1_end.timestamp() - event2_end.timestamp()

        return start_diff

    kwargs = dict(credentials=credentials)

    if dt_min:
        kwargs['dt_min'] = dt_min

    if max_days:
        kwargs['max_days'] = max_days

    if timezone:
        kwargs['timezone'] = timezone

    res = []
    for calendar_id in calendar_ids:
        kwargs['calendar_id'] = calendar_id
        event_list = get_events(**kwargs)
        res = merge_sorted_lists(event_comparator, res, event_list)

    return res
