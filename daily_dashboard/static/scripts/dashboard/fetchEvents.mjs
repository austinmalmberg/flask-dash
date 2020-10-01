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
        .then(data => callback(data))
        .catch(err => {
            clearContainer(flashContainer);
            console.error(err);
            flashError(`Error fetching events: ${err}`);
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

const now = new Date();

const midnight = new Date();
midnight.setHours(0, 0, 0, 0);
midnight.setDate(midnight.getDate() + 1);

// set page reload to the time until midnight or 5 minutes -- whichever comes first
const timeoutDuration = Math.min(midnight - now, 1000 * 60 * 5);

// reload the page every 5 minutes
setTimeout(() => location.reload(), timeoutDuration);
