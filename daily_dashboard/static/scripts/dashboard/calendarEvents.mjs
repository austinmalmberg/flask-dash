
import { flashError } from '../general.mjs';

export async function fetchEvents() {
    const firstDateCard = document.querySelector('.date--card');
    const today = firstDateCard.id;
    if (new Date(today) == 'Invalid Date') {
        flashError('Unable to fetch events. Refresh the page or contact the developer if the problem persists.');
        console.log('Date card does not have a valid date formatted id', firstDateCard)
        return null;
    }

    const params = new URLSearchParams({
        date: today
    });

    const response = await fetch(`${CALENDAR_ENDPOINT}?${params}`);

    if (response.ok) {
        const text = await response.text();
        const container = document.createElement('div');
        container.innerHTML = text;
        addEventsToContainers([...container.children]);
        console.log(new Date().toLocaleString(), 'Events updated');
    } else if (response.redirected) {
        window.location.replace(LOGIN_EXTERNAL_ENDPOINT);
        console.log(new Date().toLocaleString(), 'Redirecting to login');
    } else{
        flashError('Unable to retrieve calendar events.');

        const err = await response.json();
        console.error(new Date().toLocaleString(), err);
    }
}


function addEventsToContainers(eventContainersArray) {
    for (const container of eventContainersArray) {
        const forDate = container.getAttribute('data-for-date');

        const card = document.getElementById(forDate);
        if (card !== null) {
            const eventContainer = card.querySelector(`.event--container`);
            eventContainer.innerHTML = container.innerHTML;
        }
    }
}

/*
 * Clears events from nodes with the event--container class.
 *
 * @param n - A node or array of nodes
*/
export function clearEvents(n) {
    if (Array.isArray(n)) {
        for (const e of n) {
            const c = getEventContainer(e);
            if (c) c.innerHTML = '';
        }
    } else if (typeof(n) === 'object') {
        const c = getEventContainer(n);
        if (c) c.innerHTML = '';
    }

    function getEventContainer(node) {
        return n.classList.contains('event--container') ? n : n.querySelector('.event--container');
    }
}
