import { flashError } from './general.mjs'
import { requestPosition } from './geolocation.mjs';
import { Clock, Subscriber } from './clock.mjs';
import { fetchWeather, clearWeather } from './weather.mjs';
import { fetchEvents, clearEvents } from './calendarEvents.mjs';
import { getCookie, setCookie } from '../cookieManager.mjs';

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


const dateCards = document.querySelectorAll('.date--card');
const clock = new Clock('clock');

// set headers when date changes
const setNewHeadersSubscriber = new Subscriber('rollover',
    (dt, lastRun) => !lastRun || dt.toDateString() != lastRun.toDateString(),
    () => setDateHeaders(dateCards)
);
clock.addSubscriber(setNewHeadersSubscriber, 'force');

clock.start();

async function startWeatherInterval() {
    let error;

    // attempt to set position cookie from navigator.geolocation
    if (!getCookie('position')) {
        await requestPosition()
            .then(coords => {
                let { latitude, longitude } = coords;

                // round to two decimal places
                latitude = parseInt(Math.round(latitude * 100)) / 100;
                longitude = parseInt(Math.round(longitude * 100)) / 100;

                // set the position cookie with location
                setCookie('position', `${latitude},${longitude}`, 14)
            })
            .catch(err => error = err.message);
    }

    // try once to fetch weather (whether or not the cookie was set)
    // if successful, fetch weather on a 10 minute interval
    fetchWeather()
        .then(response => {
            if (response.ok) setInterval(fetchWeather, 1000 * 60 * 10);
        }).catch(err => flashError(error || err.message));
}

startWeatherInterval();

fetchEvents();
setInterval(fetchEvents, 1000 * 60 * 10);
