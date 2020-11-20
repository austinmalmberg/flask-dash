Project Backlog
===============

#### General
- [x] On account creation,
    - [x] Add primary calendar to database
    - [x] Add user's calendars to database
    - [x] Set user calendar settings
- [ ] Implement tests

#### Dashboard
- [x] Display date
- [x] Display calendar events
- [x] Create proper headers
- [x] Add styling
- [x] Set page to refresh at midnight
- [x] Use Google color scheme for events
- [x] **Bug**: Retrieving events from `/events` after 8:00pm does not populate the current day
    - This is related to timezones. The server calculates the date from UTC. Being in EST on DST, we are -4:00 behind
        UTC effectively one day behind UTC after 8:00PM
    - **Fix**: Send date information during `/events` fetch
- [x] **Bug**: Correct time on all-day events
    - **Fix**: The frontend was formatting a UTC date into a time string which caused the date to be offset by -4:00.
        Added `T00:00:00` to the string to treat it as a timezone relative date
- [x] Display weather
- [ ] Refactor templates; add escaping
- [ ] Add method typing
- [ ] Allow users to change their timezone in `/settings`
    - A session variable for the timezone is set when a user authorizes the application.
- [ ] Implement SSE/polling
    - [ ] Begin watching selected calendars for event changes
        - [ ] If the event falls within the calendar duration, send event details in next poll (or SSE)
        - [ ] Update watch notifications when `/settings` are changed
    - [ ] Send event changes to client
        - [ ] Handle updating events
- [ ] Change day header to holiday theme

#### `/login`
- [x] Add styling

#### `/settings`
- [x] Make calendar list reflect currently selected calendars
- [x] Begin watching checked calendars through POST request
- [x] Add styling
- [ ] Implement general settings
- [ ] Center select options

#### `/userinfo`
- [ ] **Bug**: Fix 401 UNAUTHENTICATED error when attempting to get user info
