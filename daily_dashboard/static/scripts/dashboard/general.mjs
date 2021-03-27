/*
 * Returns a date in the format: '2020-06-30'
 * @param {date} date - The date object
*/
export function isoDateString(date) {
    return `${ date.getFullYear() }-${ zPadNum(date.getMonth() + 1) }-${ zPadNum(date.getDate()) }`;

    function zPadNum(n, d=2) {
        return n.toString().padStart(d, '0');
    }
}


/*
 * Creates a new element and append it to the given parent element.
 * param {string} tag
 * param {string array} classes
 * param {string or HTMLObject} innerHtml
 * param {HTMLObject} parent
 * return The newly created element
*/
export function generateElement({ tag, id, classes, style, innerHTML }, parent) {
    if (!tag) return null;

    const e = document.createElement(tag);
    if (id) e.id = id;
    if (classes) e.classList.add(...classes);
    if (style) e.style = style;
    if (innerHTML) e.innerHTML = innerHTML;
    if (parent) parent.appendChild(e);

    return e;
}

export function clearContainer(element) {
    element.innerHTML = '';
}

export function flashError(message) {
    generateElement({
        tag: 'p',
        classes: ['flash', 'error'],
        innerHTML: message
    }, flashContainer);
}

export function flashInfo(message) {
    generateElement({
        tag: 'p',
        classes: ['flash', 'info'],
        innerHTML: message
    }, flashContainer);
}
