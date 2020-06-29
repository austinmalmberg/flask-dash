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
- [ ] Roll events over to the next card on date change
- [x] **Bug**: Retrieving events after 8:00pm does not populate the current day
    - This is related to timezones. Being in EST on DST, we are -4:00 behind UTC. Server calculates based off UTC date.
    - **Fix**: Send date information during `/events` fetch
- [ ] **Bug**: Correct time on all-day events
- [ ] Display weather
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
