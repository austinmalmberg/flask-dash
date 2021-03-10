import requests

BASE_ENDPOINT = 'http://ip-api.com/json'
PARAMS = ['lat', 'lon', 'timezone', 'status', 'message']


def request_location(ip_addr):
    params = {
        'fields': ','.join(PARAMS)
    }

    response = requests.get(f'{BASE_ENDPOINT}/{ip_addr}', params=params)

    return response.json()
