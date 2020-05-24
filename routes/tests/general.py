from datetime import datetime, timedelta

from flask import Blueprint, session, redirect, Response, url_for, render_template

bp = Blueprint('general_tests', __name__, url_prefix='/tests')


@bp.route('/home')
def home():
    return 'Test home'


@bp.route('/anotherpage')
def another_page():
    session['redirect_after'] = datetime.utcnow() + timedelta(seconds=7)
    print(f"redirect set for {session['redirect_after']}")

    return render_template('tests/another_page.html')


@bp.route('/poll', methods=('GET',))
def poll():
    if datetime.utcnow() > session['redirect_after']:
        print(f"redirecting back to {url_for('general_tests.home')}")
        return redirect(url_for('general_tests.home'))

    return Response(status=202)