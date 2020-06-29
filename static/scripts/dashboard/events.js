// eventsUrl, eventCards set from dashboard.html template


// populate calendar with events
function fetchCalendarEvents(callback) {
    const now = new Date();
    const year = now.getFullYear();
    const month = (now.getMonth() + 1).toString().padStart(2, '0');
    const date = now.getDate().toString().padStart(2, '0');

    const params = new URLSearchParams({ timeMin: `${now.getFullYear()}-${month}-${date}` });

    fetch(`${eventsUrl}?${params}`)
        .then(handleFetchErrors)
        .then(response => response.json())
        .then(data => callback(data))
        .catch(err => {
            clearContainer(flashContainer);
            flashError(`Error fetching events: ${err}`);
        });
}


function handleFetchErrors(response) {
    if (!response.ok) {
        console.log(response);
        throw `${response.status} ${response.statusText}`;
    }
    return response;
}

/*
 *
 * @param {object} eventList
 * @returns
*/
function handleEvents(events) {
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

            if (eventEnd <= dayStart) {
                // remove events that start before the current day
                events.shift();
                continue;

            } else if (eventStart >= dayEnd) {
                // since events are sorted, if the event occurs at a future date then go to the next card
                break;
            }

            const eventElement = document.getElementById(event.id);

            // update the element if it exists. Otherwise, create a new element
            if (eventElement) {
                updateEventElement(eventElement, event);
            } else {
                addEventToElement(event, card);
            }

            const eventEndsToday = (dayEnd.getFullYear() === eventEnd.getFullYear() &&
                dayEnd.getMonth() === eventEnd.getMonth() &&
                dayEnd.getDate() === eventEnd.getDate());

            // remove elements that end on the current date. Otherwise, increment the index
            if (eventEndsToday) events.shift();
            else i++;
        }
    }
}


/*
 * Generates an event and adds it to the given element.
 *    <div class="event" id="[event.id]">
 *        <div class="time">
 *            <p class="start">9:30 AM</p>
 *            <p class="end">6:00 PM</p>
 *        </div>
 *        <p class="summary">Work</p>
 *    </div>
 *
 * @param {object} event
 * @param {HTMLObject} element
 * @returns null
*/
function addEventToElement(event, element) {
    const eventDiv = appendToElement(element, 'div', event.id, ['event']);
    const timeDiv = appendToElement(eventDiv, 'div', null, ['time']);

    const eventStart = new Date(event.start.dateTime || event.start.date);
    appendToElement(timeDiv, 'p', null, ['start'], eventStart.toLocaleTimeString(undefined, timeOptions));

    const eventEnd = new Date(event.end.dateTime || event.end.date);
    appendToElement(timeDiv, 'p', null, ['end'], eventEnd.toLocaleTimeString(undefined, timeOptions));

    appendToElement(eventDiv, 'p', null, ['summary'], event.summary);
}


function updateEventElement(element, event) {
    const eventStart = new Date(event.start.dateTime || event.start.date);
    element.querySelector('.start').innerHTML = eventStart.toLocaleTimeString(undefined, timeOptions);

    const eventEnd = new Date(event.end.dateTime || event.end.date);
    element.querySelector('.end').innerHTML = eventEnd.toLocaleTimeString(undefined, timeOptions);

    element.querySelector('.summary').innerHTML = event.summary;
}

fetchCalendarEvents(handleEvents);

// reload the page every 5 minutes
setTimeout(() => location.reload(), 1000 * 60 * 5);
