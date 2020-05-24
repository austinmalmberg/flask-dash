import functools

from flask import Blueprint, session, g, redirect, url_for, flash

from database import User

bp = Blueprint('auth', __name__)


def login_required(view):
    @functools.wraps(view)
    def wrapped_view(*args, **kwargs):
        if g.user is None and 'token' not in kwargs:
            flash('You must be logged in to do that')
            return redirect(url_for('index'))
        return view(*args, **kwargs)
    return wrapped_view


@bp.before_app_request
def load_logged_in_user():
    """
    Uses the user_id stored in the session to load the user into g for the duration of the request.

    :return: None
    """
    user_id = session.get('user_id')

    if user_id is None:
        g.user = None
    else:
        g.user = User.query.filter_by(id=user_id).first()


@bp.route('/logout')
def logout():
    """
    Clears the session of any saved information.

    :return: a redirect back to '/'
    """
    session.clear()
    return redirect(url_for('index'))