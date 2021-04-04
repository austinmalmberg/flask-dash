from datetime import datetime, timedelta
import functools

from flask import session, request, flash

from daily_dashboard.providers.ip_api import request_location

LOCATION_VARIABLES = ['lat', 'lon', 'timezone']
LOCATION_DURATION = 7


def use_location(view):
    @functools.wraps(view)
    def wrapped_view(*args, **kwargs):
        should_update=False

        # if any of the the session location variables are not in the session, get the location from the request address
        for var in LOCATION_VARIABLES:
            if var not in session:
                should_update = True

        if 'location_expires' in session and datetime.utcnow() >= session['location_expires']:
            should_update = True

        if should_update:
            status_code, data = request_location(request.remote_addr)

            if data is None:
                flash('There was a problem retrieving your relative location. Weather and events may not work as expected', 'info')
                return view(*args, **kwargs)

            session['location_status'] = data['status']

            if status_code == 200 and session['location_status'] == 'success':
                # set cookies
                for var in LOCATION_VARIABLES:
                    session[var] = data[var]

                session['location_expires'] = datetime.utcnow() + timedelta(days=LOCATION_DURATION)
            else:
                # set temp session variables to NYC when location status fails
                session['zip_code'] = '10007'
                session['lat'] = 40.7128
                session['lon'] = -74.0060
                session['timezone'] = 'America/New_York'

                flash('Your location defaulted to New York City. For accurate time and weather, '
                      'update this manually in Settings or share your location.', 'info')

                session['location_expires'] = datetime.utcnow() + timedelta(days=1)

        return view(*args, **kwargs)

    return wrapped_view


def set_location(zip_code=None, lat=None, lon=None):
    # TODO: lat/lon only: get zip_code, timezone
    if zip_code:
        session['zip_code'] = zip_code
        # TODO: zip_code only: get lat, lon, timezone

    if lat and lon:
        session['lat'] = lat
        session['lon'] = lon

    # session['timezone'] = timezone

    # pop expiry so it does not get set automatically
    session.pop('location_expires', None)
    pass
