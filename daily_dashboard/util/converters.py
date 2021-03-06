from dateutil import parser

from werkzeug.routing import BaseConverter, ValidationError, FloatConverter


class DatetimeConverter(BaseConverter):
    regex = r'\d{4}\-\d{2}\-\d{2}'
    date_format = '%Y-%m-%d'

    def to_python(self, value):
        try:
            return parser.isoparse(value)
        except ValueError:
            raise ValidationError()

    def to_url(self, value):
        return value.strftime(self.date_format)


class CustomFloatConverter(FloatConverter):
    """
    A custom float converter which accepts negative numbers
    """
    regex = r'-?\d+(\.\d+)?'
