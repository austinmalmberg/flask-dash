from datetime import datetime

from flask import Blueprint, render_template, g, redirect, url_for, session

from routes.auth.google import oauth_limited_input_device

bp = Blueprint('main', __name__)


@bp.route('/')
def index():
    if g.user and g.user.token:
        return redirect(url_for('main.dashboard'))

    no_credentials = 'device_credentials' not in session
    credentials_expired = 'device_credentials' in session and \
                          datetime.utcnow() > session['device_credentials']['valid_until']

    # if no_credentials or credentials_expired:
    session['device_credentials'] = oauth_limited_input_device.create_device_credentials()

    return render_template('index.html', device_credentials=session.get('device_credentials'))


@bp.route('/dashboard')
def dashboard():
    # get events

    return render_template('dashboard.html')
