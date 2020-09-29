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
 * Creates a new element and append it to the given parentElement.
 * param {HTMLObject} parentElement
 * param {string} tag
 * param {string array} classes
 * param {string or HTMLObject} html
 * return The newly created element
*/
export function appendToElement(parentElement = document.body, tag = 'div', id = null, classes = null, html = null) {
    const e = document.createElement(tag);
    if (id) e.id = id;
    if (classes) e.classList.add(...classes);
    if (html) e.innerHTML = html;
    parentElement.appendChild(e);

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
