from enum import Enum
import functools

from flask import request, g, make_response

from daily_dashboard.providers.ip_api import request_location
from daily_dashboard.util.errors import BaseApplicationException


class PositionMethod(Enum):
    ARGS = 'args'
    COOKIE = 'cookie'
    IP_ADDR = 'ip_address'
    NONE = 'none'


def use_location(view):
    """
    A decorator function. Attempts to populate the following variables:

    g.lat - the latitude
    g.lon - the longitude

    Prioritizes lat and lon variables in order of importance.

    - Request params
    - Cookie values
    - IP location

    A new cookie will be set if a cookie does not already exist.

    Possible error responses:
        400 - missing one or both lat and lon variables
    :returns:
    """

    @functools.wraps(view)
    def wrapped_view(*args, **kwargs):
        # get location from request params
        position = request.args.get('pos', None)
        g.position_method = PositionMethod.ARGS

        # fallback location from cookie
        if position is None:
            g.position_method = PositionMethod.COOKIE
            position = request.cookies.get('position', None)

        # fallback location from IP address
        if position is None:
            g.position_method = PositionMethod.IP_ADDR
            position, _ = set_location_from_ip(request.remote_addr)

        # check that lat and lon params are set
        if position is None:
            return BaseApplicationException(
                400,
                title='Bad request',
                message="Missing 'lat' and 'lon' parameters."
            ).as_json()

        try:
            lat, lon = position.split(',')
            lat = float(lat)
            lon = float(lon)
        except TypeError:
            err = BaseApplicationException(
                400,
                title='Bad request',
                message="'lat' and 'lon' values must decimal values"
            )
            res = make_response(err.as_json())

            if g.position_method == PositionMethod.COOKIE:
                res.delete_cookie('position')

            return res

        g.lat = lat
        g.lon = lon

        v = view(*args, **kwargs)

        # return the view if a cookie already exists
        if 'position' in request.cookies:
            return v

        # otherwise, set these cookies
        res = make_response(v)
        res.set_cookie('position', f"{lat},{lon}")

        return res

    return wrapped_view


def set_location(res, lat, lon):
    """
    Attempts to set the
    :param res: the response view
    :param lat: a float value representing latitude
    :param lon: a float value representing longitude
    :return:
    """
    res.set_cookie('position', f"{lat},{lon}")

    g.lat = lat
    g.lon = lon

    return res


def get_location():
    """
    Gets location info from a cookie

    :return: a tuple like (lat, lon)
    """
    return request.cookies.get('lat', None), request.cookies.get('lon', None)


def set_location_from_ip(ip_addr):
    """
    Requests location through the ip-api API and returns a tuple like (lat, lon, error)

    Lat and lon will be None in the following circumstances
    - No response from the API
    - API response returned an error

    :param ip_addr: an IP address
    :return: (lat, lon, error)
    """
    error = None
    status_code, data = request_location(ip_addr or request.remote_addr)

    # there was a problem requesting the location from the API
    if status_code == 000:
        error = 'No response from the API'

    # the API did not return the location
    elif status_code != 200 or data.get('status', None) != 'success':
        error = data.get('message', 'Unknown error')

    if error:
        return None, error

    lat = data.get('lat')
    lon = data.get('lon')

    return f"{lat},{lon}", None

