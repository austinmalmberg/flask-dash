
import { flashError } from './general.mjs';

async function fetchEvents() {
    const response = await fetch(CALENDAR_ENDPOINT);

    if (response.ok) {
        const text = await response.text();
        const container = document.createElement('div');
        container.innerHTML = text;
        addEventsToContainers([...container.children]);
    } else {
        flashError('Unable to retrieve calendar events. If this problem persists, contact the developer.');

        const err = await response.json();
        console.error(err);
    }
}


function addEventsToContainers(eventContainersArray) {
    for (const container of eventContainersArray) {
        const forDate = container.getAttribute(CARD_DATE_ATTRIBUTE);

        const card = document.getElementById(forDate);
        if (card !== null) {
            const eventContainer = card.querySelector(`.${EVENT_CONTAINER_CLASS}`);
            eventContainer.innerHTML = container.innerHTML;
        }
    }
}


fetchEvents();

