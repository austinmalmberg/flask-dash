/*
        This module has been deprecated.
        Events are now retrieved and added to the dashboard on the backend and sent with the template
*/

import { isoDateString, generateElement } from './general.mjs';

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
    const eventElement = generateElement({
        tag: 'div',
        id: event.id,
        classes: ['event'],
        style: event.style
    });

    const timeDiv = generateElement({
        tag: 'div',
        classes: ['time'],
    }, eventElement);

    const startingOnCurrentDate = isSameDate(start, curr);

    if (startingOnCurrentDate) {
        generateElement({
            tag: 'p',
            classes: ['start'],
            innerHTML: start.toLocaleTimeString(undefined, timeOptions)
        }, timeDiv);
    } else {
        eventElement.classList.add('carryover');
    }

    // All day events end on the next day at 12:00AM so subtract one second to avoid adding the event to the next day
    const endMinusOneSecond = new Date(end);
    endMinusOneSecond.setSeconds(end.getSeconds() - 1);
    const endingOnCurrentDate = isSameDate(endMinusOneSecond, curr);

    if (endingOnCurrentDate) {
        // only add the end time if the event ends at midnight on the next day
        generateElement({
            tag: 'p',
            classes: ['end'],
            innerHTML: `- ${ end.toLocaleTimeString(undefined, timeOptions) }`
        }, timeDiv);
    }

    generateElement({
        tag: 'p',
        classes: ['summary'],
        innerHTML: event.summary
    }, eventElement);

    return eventElement;


    function isSameDate(d1, d2) {
        return (
            d1.getFullYear() === d2.getFullYear() &&
            d1.getMonth() === d2.getMonth() &&
            d1.getDate() === d2.getDate()
        );
    }
}


/* EXPORTS */


/*
 * @param {object} event - An event object
 *      {
 *          "background": "#e1e1e1",
 *          "end": {
 *              // one or the other, never both
 *              "dateTime": "2020-06-29T18:00:00-04:00",
 *              "date": "2020-06-29"
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
export function addEventToDOM(event) {
    let eventStart = new Date(event.start.dateTime || `${event.start.date}T00:00`);
    let eventEnd = new Date(event.end.dateTime || `${event.end.date}T00:00`);

    console.log({event, 'times': { eventStart, eventEnd }});

    let curr = new Date(eventStart);
    curr.setHours(0, 0, 0, 0);

    while (curr < eventEnd) {
        // continue to add events to the next eventContainer until curr >= eventEnd or eventContainer comes back null
        let eventCard = document.getElementById(isoDateString(curr));

        if (eventCard) {
            let eventContainer = eventCard.querySelector('.event--container');
            let eventElement = generateEventElement(event, eventStart, curr, eventEnd);
            eventContainer.appendChild(eventElement);
        }

        curr.setDate(curr.getDate() + 1);
    }
}


export function addAllEventsToDOM(events) {
    events.forEach(addEventToDOM);
}
