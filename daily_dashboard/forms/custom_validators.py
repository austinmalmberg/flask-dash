from wtforms.validators import ValidationError, InputRequired


class RequiredIf(InputRequired):

    def __init__(self, other_field_name, message=None):
        self.other_field_name = other_field_name
        super(RequiredIf, self).__init__(message=message)

    def __call__(self, form, field):
        try:
            other_field = form[self.other_field_name]
        except KeyError:
            raise ValidationError(f'Invalid field name: {self.other_field_name}')

        # make sure the other field has data
        if other_field.raw_data and bool(other_field.raw_data[0]):
            # run InputRequired validation
            super(RequiredIf, self).__call__(form, field)
