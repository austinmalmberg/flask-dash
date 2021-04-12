import { flashError } from '../general.mjs'
import { requestLocation } from '../location.mjs';
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


const dateCards = document.querySelectorAll('.date--card');
const clock = new Clock('clock');

// set headers when date changes
const setNewHeadersSubscriber = new Subscriber('rollover',
    (dt, lastRun) => !lastRun || dt.toDateString() != lastRun.toDateString(),
    () => setDateHeaders(dateCards)
);
clock.addSubscriber(setNewHeadersSubscriber, 'force');

clock.start();

// wait for the user to share location

// fetch weather and start weather interval
async function setLocation() {
    try {
        const { coords } = await requestLocation();
        const { latitude, longitude } = coords;
        if (latitude && longitude) {
            const response = await fetch(DEVICE_ENDPOINT, {
                method: 'PUT',
                headers: {
                    'Content-Type': 'application/json'
                },
                body: JSON.stringify({
                    lat: latitude,
                    lon: longitude
                })
            }).catch(console.error);

            if (response.ok) fetchWeather();

            return true;
        }

        throw new Error('Latitude and/or longitude could not be obtained from navigator.geolocation');

    } catch (err) {
        console.error(err);
        flashError('Could not get location. Update this manually through settings.');
    }

    return false;
}

if (!locationSet) {
    setLocation();
} else {
    fetchWeather();
}

setInterval(fetchWeather, 1000 * 60 * 5);

fetchEvents();
setInterval(fetchEvents, 1000 * 60 * 5);
