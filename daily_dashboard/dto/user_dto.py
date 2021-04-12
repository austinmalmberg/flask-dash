
class UserDto:

    def __init__(self, user):
        self.email = user.email
        self.name = user.name
        self.locale = user.locale
        self.timezone = user.timezone
        self.date_order = user.date_order
        self.time_24hour = user.time_24hour
