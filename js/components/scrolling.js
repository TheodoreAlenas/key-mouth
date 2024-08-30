
export function getIsAtBottom(element) {
    const visible = element.clientHeight
    const above = Math.floor(element.scrollTop)
    const all = element.scrollHeight
    return visible + above + 5 > all
}

export function scrollToBottom(element) {
    element.scrollTop = element.scrollHeight
}

