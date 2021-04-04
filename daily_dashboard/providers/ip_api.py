import requests

BASE_ENDPOINT = 'http://ip-api.com/json'
PARAMS = ['lat', 'lon', 'timezone', 'status', 'message']


def request_location(ip_addr):
    params = {
        'fields': ','.join(PARAMS)
    }

    try:
        response = requests.get(f'{BASE_ENDPOINT}/{ip_addr}', params=params)
    except requests.exceptions.ConnectionError as e:
        # TODO: log error to file
        return 000, None

    return response.status_code, response.json()
