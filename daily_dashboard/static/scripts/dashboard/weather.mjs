/*

A cookie is used to save the signed-in user's grid position

If the client does not have this cookie, the script will attempt to fetch weather data from the weather API using
the device's current position.  On a successful fetch, the grid location saved as a cookie.

If the current position cannot be retrieved, flash an error.

This can occur for one of the following reasons--

- The browser does not support navigator.geolocation, or the user did not allow navigator.geolocation access to their
location. If this happens, display the message, "Unable to get your location. You'll need to update this within your
settings"
- The weather fetch failed.  In this case, display the message "Unable to request weather for your current location"

*/

import { flashInfo, flashError, clearContainer, generateElement } from './general.mjs';
import { requestPosition } from './geolocation.mjs';
import { getCookie, setCookie } from '../cookieManager.mjs';

const createForecastEndpoint = (weatherData) => `https://api.weather.gov/gridpoints/${weatherData}/forecast`;

async function handleWeather() {
    if (!getCookie('weatherData')) {
        // if the browser does not have the grid data stored as a cookie, set it
        try {
            // request user's location for 20 seconds
            const positionTimeout = 20000;
            const position = await requestPosition({ timeout: positionTimeout }, positionTimeout);
            const properties = await getForecastProperties(position.coords);
            const { cwa, gridX, gridY } = properties;

            setCookie('weatherData', `${cwa}/${gridX},${gridY}`, 30);
        } catch (err) {
            /*
                Flashes an error that the location was not set and reminds the user to update this in Settings.

                @param {GeolocationPositionError} error - Object with { code, message } values as outlined below
                    1 - PERMISSION_DENIED
                    2 - POSITION_UNAVAILABLE
                    3 - TIMEOUT
            */

            // TODO: find out why Chromium geolocation doesn't work
            // for now, set grid position manually
            setCookie('weatherData', 'GSP/112,77', 30);

            /*
            for (const weatherNode of document.querySelectorAll('.weather')) {
                weatherError(weatherNode);
            }

            flashInfo("Could not retrieve weather because your location is not set. Allow this website to use your " +
                "location or update it manually in Settings.")

            console.log(err);

            return null;
            */
        }
    }

    const weatherData = getCookie('weatherData');
    const forecastEndpoint = createForecastEndpoint(weatherData);
    const weatherResponse = await fetch(forecastEndpoint);

    if (weatherResponse.ok) {
        const weatherData = await weatherResponse.json();

        // populate each header with weather data
        addWeatherToDOM(weatherData.properties.periods);
    } else {
        flashError("There was a problem retrieving the weather for your current location.");
    }
}


async function getForecastProperties({ latitude, longitude }) {
    const response = await fetch(`https://api.weather.gov/points/${latitude},${longitude}`);

    if (response.ok) {
        const { properties } = await response.json();

        return properties;
    }
}

function addWeatherToDOM(periods) {
    const withinDate = (dateStr, period) => period.startTime.startsWith(dateStr) || period.endTime.startsWith(dateStr);

    const dateCards = document.querySelectorAll('.date--card');

    for(const dateCard of dateCards) {
        const date = dateCard.id;
        const relevantPeriods = periods.filter(period => withinDate(date, period));

        updateWeatherNode(dateCard.querySelector('.weather'), relevantPeriods);
    }
}

function updateWeatherNode(weatherNode, periods) {
    if (!periods || periods.length === 0) {
        weatherError(weatherNode);

    } else {
        const mainPeriod = weatherNode.closest('section').id !== 'primary' ?
            periods.filter(period => period.isDaytime)[0] : periods[0];

        weatherNode.querySelector('.forecast--image').src = mainPeriod.icon.replace('size=medium', 'size=large');

        const temps = periods.map(period => period.temperature);

        weatherNode.querySelector('.temp.hi').innerHTML = Math.max(...temps);
        weatherNode.querySelector('.temp.lo').innerHTML = Math.min(...temps);

    }
}

function weatherError(weatherNode) {
    clearContainer(weatherNode);
    generateElement({
        tag: 'p',
        innerHTML: 'No weather data'
    }, weatherNode);
}

handleWeather();
