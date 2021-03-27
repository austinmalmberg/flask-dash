
class DeviceDto:

    def __init__(self, device):
        self.uuid = device.uuid
        self.common_name = device.common_name

        self.authentication_method = 'QR Code' if device.is_limited_input_device else 'Direct'

        self.locale = device.locale
        self.timezone = device.timezone
        self.date_field_order = device.date_field_order
        self.time_24hour = device.time_24hour

        self.watched_calendars = device.watched_calendars
