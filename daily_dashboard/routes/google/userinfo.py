from flask import Blueprint, jsonify
from flask_login import login_required, current_user

from daily_dashboard.helpers.google.userinfo import get_userinfo
from daily_dashboard.routes.google.oauth import validate_oauth_token, handle_refresh_error

bp = Blueprint('user', __name__)


@bp.route('/userinfo', methods=('GET',))
@login_required
@validate_oauth_token
@handle_refresh_error
def userinfo():
    """
    Returns a list of all calendars for the user.
    :return:
    """
    userinfo = get_userinfo(token=current_user.token)

    return jsonify(userinfo)
