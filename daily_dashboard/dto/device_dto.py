from enum import Enum


class AuthenticationMethod(Enum):
    # used when authenticating from the same device
    DIRECT = 0

    # used when authenticating from a device other than the one that is being signed into
    # i.e. limited input devices without mouse and/or keyboard
    INDIRECT = 0


class DeviceDto:

    def __init__(self, device):
        self.uuid = device.uuid
        self.common_name = device.common_name

        if device.is_limited_input_device:
            self.authentication_method = AuthenticationMethod.INDIRECT
        else:
            self.authentication_method = AuthenticationMethod.DIRECT

        self.locale = device.locale
        self.timezone = device.timezone
        self.date_field_order = device.date_field_order
        self.time_24hour = device.time_24hour

        self.watched_calendars = device.watched_calendars
