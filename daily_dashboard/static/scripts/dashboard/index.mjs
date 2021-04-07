import { Clock, Subscriber } from './clock.mjs';
import { fetchWeather, clearWeather } from './weather.mjs';
import { fetchEvents, clearEvents } from './calendarEvents.mjs';

/*
 * Returns a date in the format: '2020-06-30'
 * @param {date} date - The date object
*/
export function isoDateString(date) {
    return `${ date.getFullYear() }-${ zPadNum(date.getMonth() + 1) }-${ zPadNum(date.getDate()) }`;

    function zPadNum(n, d=2) {
        return n.toString().padStart(d, '0');
    }
}


/*
 * Set day, month, and date fields on date cards.
 * @param {nodeList} cards - the date cards to set date headers on
 * @param {String} startingIsoDateString - a 10-digit ISO date string to begin populating the card date info from.
 *     If not specified, the function will set the first card header date info to the current date
*/
function setDateHeaders(cards, date=new Date()) {
    // initialize cards with dates based on `new Date()`
    for (const card of cards) {
        card.id = isoDateString(date);
        card.querySelector('.month').innerText = date.toLocaleDateString(undefined, { month: 'long' });
        card.querySelector('.day').innerText = date.toLocaleDateString(undefined, { weekday: 'long' });
        card.querySelector('.date').innerText = date.getDate();

        date.setDate(date.getDate() + 1);
    }
}


function dateRollover() {
    const secondaryNode = document.querySelector('#secondary');
    const secondaryDateCards = secondaryNode.querySelectorAll('.date--card');

    const primaryNode = document.querySelector('#primary');
    primaryNode.innerHTML = secondaryDateCards[0].outerHTML;

    secondaryNode.removeChild(secondaryDateCards[0]);

    const lastCard = secondaryDateCards[secondaryDateCards.length - 1];

    // create a new date card to append to secondary
    const newCard = lastCard.cloneNode(true);
    clearEvents(newCard);
    clearWeather(newCard);
    setDateHeaders([newCard], getNextDay(newCard.id));

    secondaryNode.appendChild(newCard);

    function getNextDay(isoDate) {
        const nextDay = new Date(`${isoDate}T00:00:00`);
        nextDay.setDate(nextDay.getDate() + 1);

        return nextDay;
    }
}

const dateCards = document.querySelectorAll('.date--card');
const clock = new Clock('clock');

// set headers when date changes
const setNewHeadersSubscriber = new Subscriber('rollover',
    (dt, lastRun) => !lastRun || dt.toDateString() != lastRun.toDateString(),
    () => setDateHeaders(dateCards)
);
clock.addSubscriber(setNewHeadersSubscriber, 'force');

clock.start();

fetchWeather();
setInterval(fetchWeather, 1000 * 60 * 10);

fetchEvents();
setInterval(fetchEvents, 1000 * 60 * 10);
