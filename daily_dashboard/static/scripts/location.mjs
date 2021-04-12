export function requestLocation() {
    // request user's location for 10 seconds
    const timeout = 10000;
    const options = { timeout };
    const positionPromise = new Promise((resolve, reject) => navigator.geolocation.getCurrentPosition(resolve, reject, options));

    const timeoutPromise = new Promise((resolve, reject) => {
        let id = setTimeout(function() {
            clearTimeout(id);
            reject('Request for position timed out.');
        }, timeout);
    });

    return Promise.race([positionPromise, timeoutPromise])
}