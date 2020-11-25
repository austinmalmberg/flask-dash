
from flask import Blueprint, render_template

from daily_dashboard.themes import themes, skycons

bp = Blueprint('test', __name__, url_prefix='/test')


@bp.route('/themes', methods=('GET',))
def index():
    return render_template(
        'development/themes.html',
        themes=themes.get_all(),
        skycon_descriptors=skycons.descriptions,
    )