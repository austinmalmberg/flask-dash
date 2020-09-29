export function requestPosition(options = {}, timeout) {
    const positionPromise = new Promise((resolve, reject) => navigator.geolocation.getCurrentPosition(resolve, reject, options));
    if (!timeout) return positionPromise;

    const timeoutPromise = new Promise((resolve, reject) => {
        let id = setTimeout(function() {
            clearTimeout(id);
            reject('Request for position timed out.');
        }, timeout);
    });

    return Promise.race([ positionPromise, timeoutPromise])
}
