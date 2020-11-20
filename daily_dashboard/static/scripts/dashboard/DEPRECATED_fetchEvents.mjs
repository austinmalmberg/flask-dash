/*
        This module has been deprecated.
        Events are now retrieved and added to the dashboard on the backend and sent with the template
*/

import { clearContainer, flashError } from './general.mjs';
import { addAllEventsToDOM } from './calendarManager.mjs';

// eventsUrl set from dashboard.html template


// populate calendar with events
function fetchCalendarEvents(callback) {
    const today = new Date();
    today.setHours(0, 0, 0, 0);

    const params = new URLSearchParams({ timeMin: today.toISOString() });

    fetch(`${eventsUrl}?${params}`)
        .then(handleFetchErrors)
        .then(response => response.json())
        .then(data => callback(data.events))
        .catch(err => {
            clearContainer(flashContainer);
            flashError(`Error fetching events: ${err}`);
            console.error(err);
        });
}


async function handleFetchErrors(response) {
    if (response.redirected) {
        window.location.href = response.url;
    } else if (!response.ok) {
        const data = await response.json();

        console.error(response);
        console.error(data);

        throw `${response.status} ${response.statusText}`;
    }
    return response;
}


fetchCalendarEvents(addAllEventsToDOM);
