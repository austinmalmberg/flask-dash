
function appendTextElement(parentElement, tag, classes, text) {
    const e = document.createElement(tag);
    e.classList.add(...classes);
    e.innerText = text;
    parentElement.appendChild(e);
}

function clearContainer(element) {
    element.innerHTML = '';
}

function flashMessage(message) {
    appendTextElement(flashContainer, 'span', ['flash', 'error'], message);
}
