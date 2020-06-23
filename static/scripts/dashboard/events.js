// eventsUrl, eventCards set from dashboard.html template


// populate calendar with events
async function fetchCalendarEvents(callback) {
    const response = await fetch(eventsUrl);

    if (response.status === 200) {
        // add events to calendar
        const data = await response.json();
        callback(data);
    } else {
        clearContainer(flashContainer);
        flashError(`${response.status} | ${response.statusText}`);
    }
}


/*
 *
 * @param {object} eventList
 * @returns
*/
function addEventsToDOM(events) {
    for (let card of eventCards) {
        const dayStart = new Date(card.id);

        const dayEnd = new Date(card.id);
        dayEnd.setHours(dayStart.getHours() + 23, 59, 59, 999);

        let i = 0;

        while (i < events.length) {
            let event = events[i];

            // get event start and end dates
            let eventStart = new Date(event.start.dateTime || event.start.date);
            let eventEnd = new Date(event.end.dateTime || event.end.date);

            // remove events that start before the current day
            if (eventEnd <= dayStart) {
                events.shift();
                continue;

            // since events are sorted, if the event occurs at a future date then go to the next card
            } else if (eventStart >= dayEnd) {
                break;
            }

            addEventToElement(card, event);

            const eventEndsToday = (dayEnd.getFullYear() === eventEnd.getFullYear() &&
                dayEnd.getMonth() === eventEnd.getMonth() &&
                dayEnd.getDate() === eventEnd.getDate());

            if (eventEndsToday) {
                events.shift();
            } else {
                i++;
            }
        }
    }
}


/*
 * Adds an event to a given element.
 *
 * @param {object} event
 * @param {index} event
 * @returns
*/
function addEventToElement(element, event) {
    const eventStart = new Date(event.start.dateTime || event.start.date);
    const startP = document.createElement('p');
    startP.classList.add('start');
    startP.innerText = eventStart.toLocaleTimeString(undefined, timeOptions);

    const eventEnd = new Date(event.end.dateTime || event.end.date);
    const endP = document.createElement('p');
    endP.classList.add('end');
    endP.innerText = eventEnd.toLocaleTimeString(undefined, timeOptions);

    const timeDiv = document.createElement('div');
    timeDiv.classList.add('time');
    timeDiv.appendChild(startP);
    timeDiv.appendChild(endP);

    const summaryP = document.createElement('p');
    summaryP.classList.add('summary');
    summaryP.innerText = event.summary;

    const eventDiv = document.createElement('div');
    eventDiv.classList.add('event')
    eventDiv.id = event.id;
    eventDiv.appendChild(timeDiv);
    eventDiv.appendChild(summaryP);

    element.appendChild(eventDiv);
}


fetchCalendarEvents(addEventsToDOM);


// populate weather
