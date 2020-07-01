/*
 * creates a new HTML element representing the event.
 *
 * @param {object} event - The event object
 * @param {date} start - The start date of the event
 * @param {date} curr - A date for the container that the element is being created for.
 *      Hours, minutes, seconds, and milliseconds are all set to 0.
 * @param {date} end - The end date of the event
 * @return An HTML element for the event
*/
function generateEventElement(event, start, curr, end) {
    const eventElement = document.createElement('div');
    eventElement.id = event.id;
    eventElement.classList.add('event');
    eventElement.style = `background: ${event.background}; color: ${event.foreground}`;

    const timeDiv = document.createElement('div');
    timeDiv.classList.add('time');

    const startingOnCurrentDate = sameDate(start, curr);

    const endMinusOneSecond = new Date(end);
    endMinusOneSecond.setSeconds(end.getSeconds() - 1);
    const endingOnCurrentDate = sameDate(endMinusOneSecond, curr);

    if (startingOnCurrentDate) {
        const startElement = document.createElement('p');
        startElement.classList.add('start');
        startElement.innerHTML = start.toLocaleTimeString(undefined, timeOptions);
        timeDiv.appendChild(startElement);
    }

    const allDayEvent = (!sameDate(end, curr));
    if (endingOnCurrentDate && !allDayEvent) {
        // only add the end time if the event ends on at midnight on the next day
        const endElement = document.createElement('p');
        endElement.classList.add('end');
        endElement.innerHTML = `- ${ end.toLocaleTimeString(undefined, timeOptions) }`;
        timeDiv.appendChild(endElement);
    }

    const summary = document.createElement('p');
    summary.classList.add('summary');
    summary.innerText = event.summary;

    eventElement.appendChild(timeDiv);
    eventElement.appendChild(summary);

    if (!startingOnCurrentDate && endingOnCurrentDate) eventElement.classList.add('carryover');

    return eventElement;


    function sameDate(d1, d2) {
        return (
            d1.getFullYear() === d2.getFullYear() &&
            d1.getMonth() === d2.getMonth() &&
            d1.getDate() === d2.getDate()
        );
    }
}


/*
 * Returns a date in the format: '2020-06-30'
 * @param {date} date - The date object
*/
function isoDateString(date) {
    return `${ date.getFullYear() }-${ padNum(date.getMonth() + 1) }-${ padNum(date.getDate()) }`;

    function padNum(n) {
        return n.toString().padStart(2, '0');
    }
}

/*
 * @param {object} event - An event object
 *      {
 *          "background": "#e1e1e1",
 *          "end": {
 *              "dateTime": "2020-06-29T18:00:00-04:00"
 *          },
 *          "foreground": "#1d1d1d",
 *          "htmlLink": <link to event>,
 *          "id": <string>,
 *          "start": {
 *              // one or the other, never both
 *              "dateTime": "2020-06-29T09:30:00-04:00",
 *              "date": "2020-06-29"
 *          },
 *          "summary": "Work"
 *      }
 * @return null
*/
export function addEvent(event) {
    let eventStart = new Date(event.start.dateTime || `${event.start.date}T00:00:00`);
    let eventEnd = new Date(event.end.dateTime || `${event.end.date}T00:00:00`);

    let curr = new Date(eventStart);
    curr.setHours(0, 0, 0, 0);

    while (curr < eventEnd) {
        // continue to add events to the next eventContainer until curr >= eventEnd or eventContainer comes back null
        let eventContainer = document.getElementById(isoDateString(curr));
        let eventElement = generateEventElement(event, eventStart, curr, eventEnd);

        if (eventContainer) eventContainer.appendChild(eventElement);

        curr.setDate(curr.getDate() + 1);
    }
}


export function addAllEvents(events) {
    events.forEach(addEvent);
}
