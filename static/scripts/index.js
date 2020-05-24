async function poll_device_endpoint() {
    const response = await fetch('/poll');

    if (response.redirected) {
        window.location.href = response.url;
    }
}

// set an interval to poll the endpoint that checks whether or not the user has authenticated
const intervalId = setInterval(poll_device_endpoint, 5 * 1000);