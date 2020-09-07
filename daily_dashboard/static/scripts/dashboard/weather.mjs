/*

A cookie is used to save the signed-in user's location

If the client does not have this cookie, the script will attempt to fetch weather data from the weather API using
the device's current position.  On a successful fetch, the grid location url is sent server-side to be cached and
resent as a cookie on the next request.

If the current position cannot be retrieved, flash a error.

This can occur for one of the following reasons--

- The browser does not support navigator.geolocation, or the user did not allow navigator.geolocation access to their
location. If this happens, display the message, "Unable to get your location. You'll need to update this within your
settings"
- The weather fetch failed.  In this case, display the message "Unable to request weather for your current location"

*/

import { requestPosition } from './geolocation.js';

/*

    check for grid url
    if no url,
        request location,
        onSuccess,
            send grid properties to server
            set grid URL
        onError,
            ask user to set their location manually in settings
            RETURN
    fetch weather data from grid URL
    then add weather to DOM
    catch error -> "There was a problem requesting weather for your location"

*/


async function handleWeather() {
    console.log(forecastGridDataUrl)
    if (typeof forecastGridDataUrl == 'undefined') {
        try {
            const position = await requestPosition({ timeout: 20000 });
            const properties = await getForecastProperties(position.coords);

            var forecastGridDataUrl = properties.forecastGridData;

            postForecastProperties(properties);
        } catch (err) {
            /*
                Flashes an error that the location was not set and reminds the user to update this in Settings.

                @param {GeolocationPositionError} error - Object with { code, message } values as outlined below
                    1 - PERMISSION_DENIED
                    2 - POSITION_UNAVAILABLE
                    3 - TIMEOUT
            */
            flashInfo("Could not retrieve weather because your location is not set. Update your location manually in Settings.")
            return;
        }
    }

    const weatherResponse = await fetch(`${forecastGridDataUrl}/forecast`);

    if (weatherResponse.ok) {
        const weatherData = await weatherResponse.json();
        console.log(weatherData.properties);
    } else {
        flashError("There was a problem retrieving the weather for your current location");
        clearForecastProperties();
    }
}


async function getForecastProperties({ latitude, longitude }) {
    const response = await fetch(`https://api.weather.gov/points/${latitude},${longitude}`);

    if (response.ok) {
        const { properties } = await response.json();

        return properties;
    }
}


/*
    Sends the following weather properties to the server to be stored as a cookie and sent with the next request.
        - forecastGridData
        - forecastZone (NOT IMPLEMENTED)
*/
function postForecastProperties({ gridId, gridX, gridY }) {
    const params = new URLSearchParams({ gridId, gridX, gridY });

    fetch(`${postForecastPropertiesUrl}?${params}`, { method: 'POST' })
    .then(() => console.log('properties set'))
    .catch(console.err);
}


function clearForecastProperties() {
    fetch(clearForecastPropertiesUrl, { method: 'POST' });
}

handleWeather();
