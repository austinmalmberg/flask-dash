from datetime import datetime

from flask import Blueprint, render_template, redirect, url_for, session
from flask_login import current_user, login_required

from routes.google import oauth_limited_input_device

bp = Blueprint('main', __name__)


@bp.route('/')
@login_required
def dashboard():
    """
    Sends basic template. Uses frontend AJAX calls to app endpoints that populate weather and events

    :return: The template
    """
    if current_user.token is None:
        return redirect(url_for('main.login'))

    # get events
    # start watching calendars

    # get weather

    return render_template('dashboard.html')


@bp.route('/login')
def login():
    if 'device_credentials' not in session or datetime.utcnow() > session['device_credentials']['valid_until']:
        session['device_credentials'] = oauth_limited_input_device.create_device_credentials()

    return render_template('login.html', device_credentials=session['device_credentials'])


@bp.route('/settings', methods=('GET', 'POST'))
def settings():
    """
    View and update user settings

    GET -- returns JSON representing user settings
    POST -- updates user settings

    :return:
    """
    return render_template('settings.html')
