
export function getIsAtBottom(element) {
    const mm = window.matchMedia('@media screen and (max-width: 25cm)')
    if (mm.matches) {
        return getIsAtBottom_window()
    }
    return getIsAtBottom_element(element)
}

function getIsAtBottom_window() {
    const visible = window.innerHeight
    const above = Math.floor(window.scrollY)
    const all = document.documentElement.scrollHeight
    return visible + above + 5 > all
}

function getIsAtBottom_element(element) {
    const visible = element.clientHeight
    const above = Math.floor(element.scrollTop)
    const all = element.scrollHeight
    return visible + above + 5 > all
}

export function scrollToBottom(element) {
    const mm = window.matchMedia('@media screen and (max-width: 25cm)')
    if (mm.matches) {
        scrollToBottom_window()
    }
    else {
        scrollToBottom_element(element)
    }
}

function scrollToBottom_window() {
    window.scrollTo({top: document.documentElement.scrollHeight})
}
function scrollToBottom_element(element) {
    element.scrollTop = element.scrollHeight
}
