function getGeolocation() {
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


export async function requestPosition() {
    try {
        const { coords } = await getGeolocation();
        return coords;
    } catch (err) {
        console.error(err);
        if (err instanceof GeolocationPositionError) {
            throw new Error('Could not get position. Share it or set it manually through settings.')
        }
        throw new Error(err.message);
    }
    return null;
}
