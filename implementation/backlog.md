Project Backlog
===============

#### General
- [ ] Implement tests
- [ ] On account creation,
    - [x] Add primary calendar to database
    - [ ] Set user calendar settings

#### Dashboard
- [ ] Display date
- [ ] Display calendar events
- [ ] Display weather
- [ ] Watch all selected calendars
    - [ ] If the event falls within the calendar duration, send event details in next poll
    - [ ] Update watch when `/settings` are changed
- [ ] Change day header to holiday theme
- [ ] Implement SSE
    - [ ] Begin watching selected calendars for event changes
    - [ ] Send event changes to client
        - [ ] Handle updating events

#### `/settings`
- [x] Make calendar list reflect currently selected calendars
- [ ] Add newly checked calendars to database through POST request
