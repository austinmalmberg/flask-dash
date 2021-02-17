from wtforms import RadioField

from daily_dashboard.forms.csrf import CSRF_Form
from daily_dashboard.forms.custom_fields import MultiCheckboxField


class SettingsForm(CSRF_Form):
    date_format = RadioField(
        u'Date Format',
        choices=[
            ('MDY', 'January 1 2020'),
            ('DMY', '1 January 2020'),
            ('YMD', '2020 January 1')
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

    # timezone = SelectField(
    #     u'Time Zone',
    #     coerce=int
    # )

    calendars = MultiCheckboxField(u'Displayed Calendars')
