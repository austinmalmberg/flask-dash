
class DeviceDto:

    def __init__(self, device):
        self.name = device.name

        self.created_on = device.created_on
        self.last_used = device.last_used
        self.last_updated = device.last_updated

        self.locale = device.locale
        self.timezone = device.timezone
        self.date_order = device.date_order
        self.time_24hour = device.time_24hour
        self.position = device.position

        self.calendars = device.watched_calendars
