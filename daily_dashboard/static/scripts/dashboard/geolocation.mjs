import { getCookie, setCookie } from '../cookieManager.mjs';
import { flashError } from './general.mjs';

function requestPosition(options = {}, timeout) {
    const positionPromise = new Promise((resolve, reject) => navigator.geolocation.getCurrentPosition(resolve, reject, options));
    if (!timeout) return positionPromise;

    const timeoutPromise = new Promise((resolve, reject) => {
        let id = setTimeout(function() {
            clearTimeout(id);
            reject('Request for position timed out.');
        }, timeout);
    });

    return Promise.race([positionPromise, timeoutPromise])
}


export async function getPosition() {
    const COOKIE_NAME = 'coords';

    const position = getCookie(COOKIE_NAME);
    if (position)
        return position;

    return await setPositionCookie();


    async function setPositionCookie() {
        const DECIMAL_PLACES = 2;
        const COOKIE_DURATION = 30;

        // if the browser does not have the grid data stored as a cookie, set it
        try {
            // request user's location for 10 seconds
            const positionTimeout = 10000;
            const { coords } = await requestPosition({ timeout: positionTimeout }, positionTimeout);
            const { latitude, longitude } = coords;

            const result = `${formatDecimal(latitude, DECIMAL_PLACES)},${formatDecimal(longitude, DECIMAL_PLACES)}`;

            setCookie(COOKIE_NAME, result, COOKIE_DURATION);

            return result;
        } catch (err) {
            console.log(err);
        }

        return null;


        function formatDecimal(n, decimalPlaces) {
            const factor = Math.pow(10, decimalPlaces);
            return Math.round(n * factor) / factor;
        }
    }
}
