from flask import Blueprint, jsonify
from flask_login import login_required


from helpers.google.userinfo import get_userinfo
from routes.google.oauth import validate_oauth_token

bp = Blueprint('user', __name__)


@bp.route('/userinfo', methods=('GET',))
@validate_oauth_token
@login_required
def userinfo():
    """
    Returns a list of all calendars for the user.
    :return:
    """
    userinfo = get_userinfo()

    return jsonify(userinfo)
