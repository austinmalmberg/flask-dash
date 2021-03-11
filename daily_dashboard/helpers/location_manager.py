from datetime import datetime, timedelta
import functools

from flask import session, request, flash

from daily_dashboard.providers.ip_api import request_location

LOCATION_VARIABLES = ['lat', 'lon', 'timezone']


def use_location_cookie(view):
    @functools.wraps(view)
    def wrapped_view(*args, **kwargs):
        # do not update location when manually set through settings
        if 'location_method' in session and session['location_method'] != 'auto':
            return view(*args, **kwargs)

        should_update = 'location_expires' in session \
                        and datetime.utcnow() > session['location_expires']

        for var in LOCATION_VARIABLES:
            if var not in session:
                should_update = True

        if should_update:
            status_code, data = request_location(request.remote_addr)

            session['location_status'] = data['status']

            if status_code == 200 and session['location_status'] == 'success':
                # set cookies
                for var in LOCATION_VARIABLES:
                    session[var] = data[var]
            else:
                # enter temp session variables when location status fails
                session['lat'] = 40.7128
                session['lon'] = 74.0060
                session['timezone'] = 'America/New_York'

                flash('Your location defaulted to New York City. For accurate time and weather, update this manually '
                      'in Settings or share your location.', 'info')

            session['location_method'] = 'auto'
            session['location_expires'] = datetime.utcnow() + timedelta(days=7)

        return view(*args, **kwargs)

    return wrapped_view
