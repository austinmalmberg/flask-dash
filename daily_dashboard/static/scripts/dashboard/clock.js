// clockElement set in dashboard.html template

let intervalId;

function updateClock() {
    clockElement.innerText = new Date().toLocaleTimeString(undefined, timeOptions);
}

// set initial clock time
updateClock();

// update clock every minute
const updateInterval = 1000 * 60;

// sync the clock time to update with the system clock
setTimeout(() => {

    // update clock time at the end of the clipped interval
    updateClock();

    // begin updating clock every interval
    intervalId = setInterval(updateClock, updateInterval);
}, updateInterval - new Date().getTime() % updateInterval);

