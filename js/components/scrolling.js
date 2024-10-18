
export function getIsAtBottom(element) {
    if (window.innerWidth <= 1000) {
        return getIsAtBottom_window()
    }
    return getIsAtBottom_element(element)
}

function getIsAtBottom_window() {
    const visible = window.outerHeight
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
    if (window.innerWidth <= 1000) {
        scrollToBottom_window()
    }
    else {
        scrollToBottom_element(element)
    }
}

function scrollToBottom_window() {
    window.scrollTo({top: document.documentElement.scrollHeight - 100})
}
function scrollToBottom_element(element) {
    element.scrollTop = element.scrollHeight
}
