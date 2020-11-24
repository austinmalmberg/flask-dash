
from flask import Blueprint, render_template

from daily_dashboard.themes import themes, skycons

bp = Blueprint('themes', __name__, url_prefix='/themes')


@bp.route('/', methods=('GET',))
def index():
    return render_template(
        'development/themes.html',
        themes=themes.get_all(),
        skycon_descriptors=skycons.descriptions,
    )