
/*
 * Creates a new element and append it to the given parentElement.
 * param {HTMLObject} parentElement
 * param {string} tag
 * param {string array} classes
 * param {string or HTMLObject} html
 * return The newly created element
*/
function appendToElement(parentElement = document.body, tag = 'div',
        id = null, classes = null, html = null) {
    const e = document.createElement(tag);
    if (id) e.id = id;
    if (classes) e.classList.add(...classes);
    if (html) e.innerHTML = html;
    parentElement.appendChild(e);

    return e;
}

function clearContainer(element) {
    element.innerHTML = '';
}

function flashError(message) {
    appendToElement(flashContainer, 'p', null, ['flash', 'error'], message);
}

function flashInfo(message) {
    appendToElement(flashContainer, 'p', null, ['flash', 'info'], message);
}
