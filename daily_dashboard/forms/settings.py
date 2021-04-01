from wtforms import RadioField, StringField
from wtforms.validators import InputRequired, Regexp

from daily_dashboard.forms.csrf import CSRF_Form
from daily_dashboard.forms.custom_fields import MultiCheckboxField


class SettingsForm(CSRF_Form):
    date_format = RadioField(
        u'Date Format',
        choices=[
            ('MDY', 'MDY (i.e. January 1 2020)'),
            ('DMY', 'DMY (i.e. 1 January 2020)'),
            ('YMD', 'YMD (i.e. 2020 January 1)')
        ],
        default='MDY',
    )

    time_format = RadioField(
        u'Time Format',
        choices=[
            ('12hr', '5:00 PM'),
            ('24hr', '17:00'),
        ],
        default='12hr',
    )

    calendars = MultiCheckboxField(u'Displayed Calendars')

    # zip_code = StringField(
    #     u'Zip Code',
    #     validators=[InputRequired(), Regexp('^\d+$')]
    # )
