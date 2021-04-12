from wtforms import RadioField, DecimalField
from wtforms.validators import Optional

from daily_dashboard.forms.csrf import CSRF_Form
from daily_dashboard.forms.custom_fields import MultiCheckboxField
from daily_dashboard.forms.custom_validators import RequiredIf


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

    lat = DecimalField(u'Latitude', validators=[
        RequiredIf('lon', message='Required if setting Longitude'), Optional(strip_whitespace=True)
    ])
    lon = DecimalField(u'Longitude', validators=[
        RequiredIf('lat', message='Required if setting Latitude'), Optional(strip_whitespace=True)
    ])
