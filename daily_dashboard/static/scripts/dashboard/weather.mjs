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
import { getPosition } from './geolocation.mjs';

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


export async function fetchWeather() {
    const position = await getPosition();

    let endpoint = WEATHER_ENDPOINT;
    if (position) {
        endpoint += position;
    }

    const response = await fetch(endpoint);

    if (response.ok) {
        const text = await response.text();
        const container = document.createElement('div');
        container.id = 'temp--element';
        container.innerHTML = text;
        addWeatherToCards([...container.children]);
        placeSkycons();
    } else {
        flashError('Unable to retrieve forecast.');

        const err = await response.json();
        console.error(err);
    }
}


function addWeatherToCards(weatherElements) {
    while (weatherElements.length > 0) {
        const weatherElement = weatherElements.shift();
        const date = weatherElement.getAttribute('data-for-date');

        const card = document.getElementById(date);

        if (card) {
            const weatherContainer = card.querySelector('.weather');
            weatherContainer.outerHTML = weatherElement.outerHTML;
        }
    }
}


/*
 * Clears events from nodes with the event--container class.
 *
 * @param n - A node or array of nodes
*/
export function clearWeather(n) {
    if (Array.isArray(n)) {
        for (const e of n) {
            const w = getWeatherElement(e);
            if (w) w.innerHTML = '';
        }
    } else if (typeof(n) === 'object') {
        const w = getWeatherElement(n);
        if (w) w.innerHTML = '';
    }

    function getWeatherElement(node) {
        return n.classList.contains('weather') ? n : n.querySelector('.weather');
    }
}


function placeSkycons() {

    const skyconCanvases = document.getElementsByClassName('skycon--canvas');

    for (const canvas of skyconCanvases) {
        const description = canvas.getAttribute('data-skycon-description');
        skycons.set(canvas, Skycons[description]);
    }

    skycons.play();
}
