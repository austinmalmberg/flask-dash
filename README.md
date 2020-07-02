Daily Dashboard
===============

A productivity application that can be used in your home or office to manage your week.

Endpoints
---------

#### `/`

*Valid OAuth 2.0 token required*

The main dashboard. Shows users an overview of weather and events happening in the current week.

#### `/settings`

*Valid OAuth 2.0 token required*

An interface to update user settings.  This includes, date and time formatting, timezone, and which calendars are
displayed on the dashboard.

### Authentication

#### `/login`

The login page. Allows visitors to login directly through this page or using a code provided on the screen from another
device by visiting `www.google.com/device`.

#### `/poll`

The endpoint that is polled on the `/login` page to check when authorization is provided through a limited input device.

#### `/oauth/authorize`

Redirects the user to Google for application authorization.

#### `/oauth/callback`

The endpoint where Google redirects the user after authorization whether or not the user has allowed scope permissions.

#### `/oauth/revoke`

*Valid OAuth 2.0 token required*

Revokes and deletes any tokens stored in the database for the currently logged in user.


### User Information

#### `/userinfo`

*Valid OAuth 2.0 token required*

**GET** | The Google users info in JSON format.


### Calendar

#### `/calendars`

*Valid OAuth 2.0 token required*

**GET** | A list of all Google Calendars in JSON format.

#### `/calendars/events`

*Valid OAuth 2.0 token required*

**GET** | A list of Google calendar events in JSON format. This list will always be sorted. The range is set from today
to 6 days from today at 11:59 PM.

Only selected calendars where will be returned. This can be changed at `/settings`.

#### `/calendars/settings`

*Valid OAuth 2.0 token required*

**GET** | A list of the user's calendar settings in JSON format. More information can be found here:
https://developers.google.com/calendar/v3/reference/settings

#### `/calendars/colors`

*Valid OAuth 2.0 token required*

**GET** | The user's calendar colors in JSON format.


### NOT IMPLEMENTED

#### `/calendars/notifications`

The endpoint to receive calendar event watch notifications. Changing a calendar event will send the event to this
endpoint where it will be sent to the end user through server side events. Event details are then updated on the front
end.

#### `/weather`

**POST** | Sends weather conditions for the location supplied in the request body. 

    {
        latitude: <float>,
        longitude: <float>
    }
