from datetime import datetime, timedelta

from flask import session, request

from daily_dashboard.providers.ip_api import request_location

LOCATION_VARIABLES = ['lat', 'lon', 'timezone']
LOCATION_DURATION = 14


def set_location_from_ip(ip_addr, force=False):
    """
    Sets the location for the session.

    :return:
    """
    should_update = force

    # if any of the the session location variables are not in the session,
    # get the relative location from the request address
    for var in LOCATION_VARIABLES:
        if f'location_{var}' not in session:
            should_update = True
            break

    if 'location_expires' in session and datetime.utcnow() >= session['location_expires'] or \
            'location_error' in session:
        should_update = True

    if should_update:
        status_code, data = request_location(ip_addr or request.remote_addr)

        if status_code == 200:
            if data['status'] == 'success':
                session['location_expires'] = datetime.utcnow() + timedelta(days=LOCATION_DURATION)
                for var in LOCATION_VARIABLES:
                    session[f'location_{var}'] = data[var]

                session.pop('location_error', None)
            else:
                session['location_error'] = f"Unable to retrieve location for {request.remote_addr}. Reason: {data['message']}"
        else:
            session['location_error'] = f"Unable to retrieve location. Status code: {status_code}"
