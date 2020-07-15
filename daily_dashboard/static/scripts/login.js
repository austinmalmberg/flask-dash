async function poll_device_endpoint() {
    const response = await fetch(pollUrl);

    if (response.redirected) {
        window.location.href = response.url;
    }
}

// Begin polling the endpoint to check when the user authenticates
const intervalId = setInterval(poll_device_endpoint, 5 * 1000);