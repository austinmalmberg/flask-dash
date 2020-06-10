from flask import Blueprint, jsonify
from flask_login import login_required, current_user

from helpers.google.userinfo import get_userinfo
from routes.google.oauth import validate_oauth_token

bp = Blueprint('user', __name__)


@bp.route('/userinfo', methods=('GET',))
@login_required
@validate_oauth_token
def userinfo():
    """
    Returns a list of all calendars for the user.
    :return:
    """
    credentials = current_user.build_credentials()
    userinfo = get_userinfo(credentials)

    return jsonify(userinfo)
