
// license at the bottom

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
    getPreviousPageIdx() {
        return this.firstPageIdx - 1
    }
    getNextPageIdx() {
        return this.firstPageIdx + this.screen.length
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

/*
Copyright 2024 <dimakopt732@gmail.com>

Permission is hereby granted, free of charge, to any person obtaining a
copy of this software and associated documentation files
(the “Software”), to deal in the Software without restriction,
including without limitation the rights to use, copy, modify, merge,
publish, distribute, sublicense, and/or sell copies of the Software,
and to permit persons to whom the Software is furnished to do so,
subject to the following conditions:

The above copyright notice and this permission notice shall be included
in all copies or substantial portions of the Software.

THE SOFTWARE IS PROVIDED “AS IS”, WITHOUT WARRANTY OF ANY KIND,
EXPRESS OR IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF
MERCHANTABILITY, FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT.
IN NO EVENT SHALL THE AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR
ANY CLAIM, DAMAGES OR OTHER LIABILITY, WHETHER IN AN ACTION OF CONTRACT,
TORT OR OTHERWISE, ARISING FROM, OUT OF OR IN CONNECTION WITH THE
SOFTWARE OR THE USE OR OTHER DEALINGS IN THE SOFTWARE.
*/
