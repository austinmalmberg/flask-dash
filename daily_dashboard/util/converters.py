from dateutil import parser

from werkzeug.routing import BaseConverter, ValidationError


class DatetimeConverter(BaseConverter):
    date_format = '%Y-%m-%d'

    def to_python(self, value):
        try:
            return parser.isoparse(value)
        except ValueError:
            raise ValidationError()

    def to_url(self, value):
        return value.strftime(self.date_format)
