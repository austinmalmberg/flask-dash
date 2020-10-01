/*
 * Returns a date in the format: '2020-06-30'
 * @param {date} date - The date object
*/
export function isoDateString(date) {
    return `${ date.getFullYear() }-${ padNum(date.getMonth() + 1) }-${ padNum(date.getDate()) }`;

    function padNum(n) {
        return n.toString().padStart(2, '0');
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
    appendToElement(flashContainer, 'p', null, ['flash', 'error'], message);
}

export function flashInfo(message) {
    appendToElement(flashContainer, 'p', null, ['flash', 'info'], message);
}
