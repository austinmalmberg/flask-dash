
function appendTextElement(parentElement, tag, classes, text) {
    const e = document.createElement(tag);
    e.classList.add(...classes);
    e.innerText = text;
    parentElement.appendChild(e);
}

function clearContainer(element) {
    element.innerHTML = '';
}

function flashError(message) {
    appendTextElement(flashContainer, 'span', ['flash', 'error'], message);
}

function flashInfo(message) {
    appendTextElement(flashContainer, 'span', ['flash', 'info'], message);
}
