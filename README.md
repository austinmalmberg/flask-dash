Endpoints
=========

#### `/`

The home page.

- If logged in, redirect to `/dashboard`
- If not logged in, redirect to `/login`

### Authentication

#### `/login`

The login page.

Visitors can login directly or with a code from another device by visiting www.google.com/device.
On successful login, redirect to `/dashboard`.

Backend
- Get device code from Google

Frontend
- Poll `/poll` every 5 seconds until user authenticates

#### `/oauth/authorize`

Authorizes the user through Google.

#### `/oauth/callback`

The endpoint where Google redirects the user once authorization has been completed.

#### `/oauth/revoke`

Revokes any tokens stored for the user.




### Dashboard

#### `/dashboard`

The main dashboard.

Backend
- Get weather
- Get events for all selected calendars

Frontend
- Setup to a channel to receive Server Side Events

#### `/weather`

Sends weather conditions for current location.



#### `/notifications`

The endpoint to receive calendar event watch notifications.

Receives calendar event notifications then sends a Server Side Event message with event summary, start time,
end time, and color.

```` 


Authentication
--------------
1. A new device visits `/`

    i. Application uses cookie to check for user in database. No user displays authentication code.
 
    i. Device displays authentication code
    
    ii. Device subscribes to `TBD <endpoint>`
    
2. Device owner visits `/register` from a separate device

    i. Sign into Google account 
    
    ii. Authenticate application
    
    iii. Enters device code
    
3. The new device

Settings
--------
- User can:
    - Set calendar id
    - Change time format (standard, military, show am/pm)
    - Change temperature format (fahrenheit, celcius)

Dashboard
---------
- Get events from Google for all selected calendars
- Subscribe to event changes on selected calendars
    - Notifications are sent to `/notifications`
    - Changes sent to subscribers via Server Side Events
    - Script adds event to dashboard under the correct day