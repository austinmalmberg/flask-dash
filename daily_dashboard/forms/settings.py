from wtforms import RadioField, DecimalField, StringField
from wtforms.validators import Optional, NumberRange, Length

from daily_dashboard.forms.csrf import CSRF_Form
from daily_dashboard.forms.custom_fields import MultiCheckboxField
from daily_dashboard.forms.custom_validators import RequiredIf


class SettingsForm(CSRF_Form):

    device_name = StringField(
        u'Device Name',
        description='A friendly name for this device so it can be easily identified',
        validators=[
            Length(max=20),
            Optional()
        ]
    )

    date_format = RadioField(
        u'Date Format',
        description='Determines how to display the date.',
        choices=[
            ('MDY', 'MDY (i.e. January 1 2020)'),
            ('DMY', 'DMY (i.e. 1 January 2020)'),
            ('YMD', 'YMD (i.e. 2020 January 1)')
        ],
        default='MDY',
    )

    time_format = RadioField(
        u'Time Format',
        description='Determines how to display the time.',
        choices=[
            ('12hr', '5:00 PM'),
            ('24hr', '17:00'),
        ],
        default='12hr',
    )

    calendars = MultiCheckboxField(
        u'Displayed Calendars',
        description='Choose which calendars to display on the dashboard.'
    )

    lat = DecimalField(u'Latitude', places=2, validators=[
        RequiredIf('lon', message='Required if setting Longitude'),
        NumberRange(min=-90.0, max=90.0),
        Optional()
    ])
    lon = DecimalField(u'Longitude', places=2, validators=[
        RequiredIf('lat', message='Required if setting Latitude'),
        NumberRange(min=-180.0, max=180.0),
        Optional()
    ])
