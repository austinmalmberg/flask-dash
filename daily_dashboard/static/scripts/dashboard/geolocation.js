export function requestPosition(options) {
    return new Promise((resolve, reject) => navigator.geolocation.getCurrentPosition(resolve, reject, options));
}
