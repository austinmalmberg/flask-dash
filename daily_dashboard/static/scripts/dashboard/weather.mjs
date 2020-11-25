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
const createHourlyForecastEndpoint = (weatherData) => createForecastEndpoint(weatherData) + '/hourly';

async function fetchForecast(endpoint, callback, onErrorFlashMessage) {
    const weatherResponse = await fetch(endpoint);

    if (weatherResponse.ok) {
        const weatherData = await weatherResponse.json();
        callback(weatherData);
    } else {
        flashError(onErrorFlashMessage);
    }
}

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
                Flash info that the location was not set and reminds the user to update this in Settings.

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

    addHourlyForecastToPrimaryNode(weatherData);
    addWeeklyForecastToNodes(weatherData);
}


async function getForecastProperties({ latitude, longitude }) {
    const response = await fetch(`https://api.weather.gov/points/${latitude},${longitude}`);

    if (response.ok) {
        const data = await response.json();

        return data.properties;
    }
}

function addHourlyForecastToPrimaryNode(weatherData) {
    const hourlyForecastEndpoint = createHourlyForecastEndpoint(weatherData);

    fetchForecast(hourlyForecastEndpoint, weatherData => {
        // populate primary date card with current temperature
        const temperature = weatherData.properties.periods[0].temperature;
        document.querySelector('.temp.curr').innerHTML = temperature;
    }, "There was a problem retrieving current weather conditions for your area.");
}

function addWeeklyForecastToNodes(weatherData) {
    const forecastEndpoint = createForecastEndpoint(weatherData);

    fetchForecast(forecastEndpoint, weatherData => {
        // populate each header with weather data
        addForecastToDOM(weatherData.properties.periods);
    }, "There was a problem retrieving the forecast for your current location.");
}

function addForecastToDOM(forecastPeriods) {
    const withinDate = (dateStr, forecastPeriod) => forecastPeriod.startTime.startsWith(dateStr);
    const dateCards = document.querySelectorAll('.date--card');

    for(const dateCard of dateCards) {
        const date = dateCard.id;
        const relevantPeriods = forecastPeriods.filter(forecastPeriod => withinDate(date, forecastPeriod));

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
        const periodHi = Math.max(...temps);
        const periodLo = Math.min(...temps);

        weatherNode.querySelector('.temp.lo').innerHTML = periodLo;

        // only add the high if there is no current temp for that date, or if the high is greater than the current temperature
        const currTempText = weatherNode.querySelector('.temp.curr').innerText;
        if (currTempText) {
            const currTemp = Number(currTempText);
            if (isNaN(currTemp) || currTemp > periodHi) return;
        }
        weatherNode.querySelector('.temp.hi').innerHTML = periodHi;
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
