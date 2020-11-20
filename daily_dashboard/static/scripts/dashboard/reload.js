const now = new Date();

const midnight = new Date();
midnight.setDate(midnight.getDate() + 1);
midnight.setHours(0, 0, 0, 0);

// get the smaller time between time 'til midnight and 10 minutes
const timeoutDuration = Math.min(midnight - now, 1000 * 60 * 10);

// set timeout to reload the page
setTimeout(() => location.reload(), timeoutDuration);
