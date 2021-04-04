
export function Clock(clockId, timezone=null) {
    const timeOptions = TIME_OPTIONS;
    if (timezone) timeOptions.timeZone = timezone;

    return {
        clockId,
        timeOptions,
        startDt: new Date(),
        dt: new Date(),
        updateInterval: 1000 * 60,
        _subscribers: [],
        start: function() {
            this.update(true, false);
            setTimeout(() => {
                // runs the update function when the next minute starts
                this.update(true, false);

                // start an interval to run the update function every updateInterval
                this.intervalId = setInterval(() => this.update(true, false), this.updateInterval);
            }, this.updateInterval - this.dt % this.updateInterval);
        },
        setTimezone: function(timezone) {
            if (!timezone)
                delete this.timeOptions.timeZone;
            else
                this.timeOptions.timeZone = timezone;

            this.update(false, false);
        },
        update: function(notify, force) {
            this.dt = new Date();

            const time = this.dt.toLocaleTimeString(undefined, this.timeOptions);
            document.getElementById(clockId).innerText = time;

            if (notify || force) {
                for (const subscriber of this._subscribers) {
                    subscriber.run(this.dt, force);
                }
            }
        },
        addSubscriber: function(subscriber, runOption) {
            this._subscribers.push(subscriber);

            if (runOption === 'run now') {
                subscriber.run(this.dt);

            } else if (runOption === 'force') {
                subscriber.run(this.dt, true);

            }
        },
        removeSubscriber: function(name) {
            const len = this._subscribers.length;
            this._subscribers = this._subscribers.filter(sub => sub.name !== name);
            return this._subscribers.length != len;
        },
    };
}


export function Subscriber(name, predicateFn, func) {
    return {
        name,
        predicateFn,
        func,
        lastRun: null,
        predicate: function(dt) {
            return !this.predicateFn || this.predicateFn(dt, this.lastRun);
        },
        run: function(dt, force) {
            if (force || this.predicate(dt)) {
                this.func(dt);
                this.lastRun = dt;
            }
        }
    };
}

