/*

A cookie is used to save the signed-in user's position

If the client does not have this cookie, the script will attempt to fetch weather data from the weather API using
the device's geolocation.  On a successful fetch, the location is saved as a cookie.

If the current position cannot be retrieved, flash an error.

This can occur for one of the following reasons--

- The browser does not support navigator.geolocation, or the user did not allow navigator.geolocation access to their
location.
- The weather fetch failed

*/

import { flashInfo, flashError, clearContainer, generateElement } from './general.mjs';
import { requestPosition } from './geolocation.mjs';
import { getCookie, setCookie } from '../cookieManager.mjs';

const WEATHER_ENDPOINT = '/weather';


async function fetchWeather() {
    const position = await getPosition();

    const endpoint = `${WEATHER_ENDPOINT}/${position}`;
    const response = await fetch(endpoint);

    if (response.ok) {
        const text = await response.text();
        const container = document.createElement('div');
        container.id = 'temp--element';
        container.innerHTML = text;
        addWeatherToCards([...container.children]);
        addSkycons();
    } else {
        flashError('Unable to retrieve forecast due to a problem with the server. If this persists, contact the developer.');

        const err = await response.json();
        console.error(err);
    }


    async function getPosition() {
        const COOKIE_NAME = 'coords';

        const position = getCookie(COOKIE_NAME);
        if (position)
            return position;

        return await setPositionCookie();


        async function setPositionCookie() {
            const DECIMAL_PLACES = 2;
            const COOKIE_DURATION = 30;

            // set cookie manually for now
            let result = `35.52,-80.98`;

            // if the browser does not have the grid data stored as a cookie, set it
            try {
                // request user's location for 20 seconds
                const positionTimeout = 20000;
                const { coords } = await requestPosition({ timeout: positionTimeout }, positionTimeout);
                const { latitude, longitude } = coords;

                result = `${formatDecimal(latitude, DECIMAL_PLACES)},${formatDecimal(longitude, DECIMAL_PLACES)}`;
            } catch (err) {
                flashError('Unable to retrieve the forecast due to a problem getting your location. Please update your location in settings');
            }

            setCookie(COOKIE_NAME, result, COOKIE_DURATION);

            return result;


            function formatDecimal(n, decimalPlaces) {
                const factor = Math.pow(10, decimalPlaces);
                return Math.round(n * factor) / factor;
            }
        }
    }
}


function addWeatherToCards(weatherElements) {
    while (weatherElements.length > 0) {
        const weatherElement = weatherElements.shift();
        const date = weatherElement.getAttribute('data-for-date');

        const card = document.getElementById(date);

        if (card) {
            const header = card.querySelector('.header');
            header.append(weatherElement);
        } else {
            console.error(`No event card found for ${date}`);
        }
    }
}

function addSkycons() {

    // darken specific features
    const colors = {
        'main': "#111",
        'fog': "#111",
        'fogbank': "#111",
        'light_cloud': "#333",
        'cloud': "#111",
        'dark_cloud': "#000",
        'wind': "#111",
        'moon': "#FFDC00",
    };

    const skycons = new Skycons({ monochrome: false, colors });

    const skyconCanvases = document.getElementsByClassName('skycon--canvas');

    for (const canvas of skyconCanvases) {
        const description = canvas.getAttribute('data-skycon-description');
        skycons.add(canvas, Skycons[description]);
    }

    skycons.play();
}

fetchWeather();

