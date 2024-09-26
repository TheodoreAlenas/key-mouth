
export default class PageIndexTracker {
    constructor({splitter}) {
        this.firstPageIdx = null
        this.lastPageIdx = null
        this.screen = []
        this.splitter = splitter
    }
    getScreen() {
        return this.screen
    }
    getLastPage() {
        return this.splitter.lastPage
    }
    getLength() {
        return this.screen.length
    }
    initPageIdx(idx) {
        this.firstPageIdx = idx
        this.lastPageIdx = idx
    }
    pushEvent(event) {
        const newPage = this.splitter.pushEvent(event)
        if (newPage) this.lastPageIdx += 1
        return newPage
    }
    shift() {
        this.screen.shift()
        this.firstPageIdx += 1
    }
    unshift(page) {
        this.screen.unshift(page)
        this.firstPageIdx -= 1
    }
    pop() {
        this.screen.pop()
    }
    push(page) {
        this.screen.push(page)
    }
    getIsDetached() {
        if (this.firstPageIdx === null) return false
        if (this.lastPageIdx === null) throw new Error('last null')
        const endOfScreen = this.firstPageIdx + this.screen.length
        return endOfScreen < this.lastPageIdx
    }
    getIsContiguous() {
        return !this.getIsDetached()
    }
    getTouchesTop() {
        return this.firstPageIdx === 0 || this.firstPageIdx === null
    }
}
