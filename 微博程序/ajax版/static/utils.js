
const e = elm => document.querySelector(elm)

const es = elms => document.querySelectorAll(elms)

const bindEvent = function(elm, eventName, callback) {
    elm.addEventListener(eventName, callback)
}

const appendHtml = (element, html) => {
    element.insertAdjacentHTML('beforeend', html)
}

const bindAll = (selector, eventName, callback) => {
    const elements = document.querySelectorAll(selector)
    for (let i = 0; i < elements.length; i++) {
        let e = elements[i]
        bindEvent(e, eventName, callback)
    }
}







