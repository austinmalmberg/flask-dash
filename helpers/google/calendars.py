from flask_login import current_user
from googleapiclient.discovery import build


def get_service():
    credentials = current_user.build_credentials()

    return build('calendar', 'v3', credentials=credentials)


def get_calendar(id):
    service = get_service()

    calendar = service.calendars().get(calendarId=id).execute()

    return calendar


def get_calendar_list():
    service = get_service()

    calendars = []

    page_token = None
    while True:
        calendar_list = service.calendarList().list(pageToken=page_token).execute()
        calendars += calendar_list['items']
        page_token = calendar_list.get('nextPageToken')
        if page_token is None:
            break

    return calendars


def get_calendar_settings():
    service = get_service()

    settings = []

    page_token = None
    while True:
        settings_list = service.settings().list(pageToken=page_token).execute()
        settings += settings_list['items']
        page_token = settings_list.get('nextPageToken')
        if page_token is None:
            break

    return settings


