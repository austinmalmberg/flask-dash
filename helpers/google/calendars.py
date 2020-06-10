from googleapiclient.discovery import build


def _get_service(credentials):
    return build('calendar', 'v3', credentials=credentials)


def get_calendar(credentials, calendar_id):
    service = _get_service(credentials)
    calendar = service.calendars().get(calendarId=calendar_id).execute()

    return calendar


def get_calendar_list(credentials):
    service = _get_service(credentials)
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
    service = _get_service(credentials)
    settings = []

    page_token = None
    while True:
        settings_list = service.settings().list(pageToken=page_token).execute()
        settings += settings_list['items']
        page_token = settings_list.get('nextPageToken')
        if page_token is None:
            break

    return settings


