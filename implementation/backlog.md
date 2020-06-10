Backlog
=======

#### General
- [ ] Implement tests
- [ ] On account creation,
    - [x] Add primary calendar to database
    - [ ] Set user calendar settings
    - [ ] Begin watching primary calendar
    - [ ] Watch for Google settings to change
- [ ] Implement SSE

#### Dashboard
- [ ] Display date
- [ ] Display calendar events
- [ ] Display weather
- [ ] Watch all calendars the user selected in the `/settings` menu
    - [ ] If the event falls within the calendar duration, send event details in next poll
    - [ ] to update watch when `/settings` are changed
- [ ] Change day header to holiday theme

#### `/settings`

- [x] Make calendar list reflect currently selected calendars
- [ ] Add newly checked calendars to database through POST request
