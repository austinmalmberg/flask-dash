
class DeviceDto:

    def __init__(self, device, is_current=None, calendar_list=None):
        self.name = device.name
        self.uuid = device.uuid

        if is_current is not None:
            self.is_current = is_current

        self.created_on = device.created_on
        self.last_used = device.last_used
        self.last_updated = device.last_updated

        self.locale = device.locale
        self.timezone = device.timezone
        self.date_order = device.date_order
        self._time_24hour = device.time_24hour

        self.position = device.position

        self.calendars = device.watched_calendars

        if calendar_list is not None:
            self.calendar_summaries = []
            for calendar in self.calendars:
                summary = next(
                    (cal.get('summary') for cal in calendar_list if cal.get('id', None) == calendar),
                    calendar
                )
                self.calendar_summaries.append(summary)

    @property
    def time_format(self):
        hours = '12'
        if self._time_24hour:
            hours = '24'

        return f'{hours}-hour'
