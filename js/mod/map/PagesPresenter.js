
// license at the bottom

import ViewModelMapper from './ViewModelMapper.js'
import PageIndexTracker from './PageIndexTracker.js'

export default class PagesPresenter {

    constructor({maxPages, viewModelMapper, splitter}) {
        if (typeof(maxPages) !== 'number') {
            throw new Error("typeof(maxPages) = " + typeof(maxPages))
        }
        if (maxPages < 2) {
            throw new Error("maxPages = " + maxPages + " < 2")
        }
        this.maxViewLength = maxPages - 1
        this.viewModelMapper = viewModelMapper
        this.pageIndexTracker = new PageIndexTracker({splitter})
    }
    pushEvent(event) {
        this._pushFirstBatch(event)
        this.pushEvent = this._pushOneEvent
    }
    _pushFirstBatch(event) {
        try {
            this.pageIndexTracker.initPageIdx(event.firstPageIdx)
            for (let e of event.events) this._pushOneEvent(e)
        }
        catch (err) {
            console.error("error pushing initial load:")
            console.error(event)
            console.error(err)
        }
    }
    _pushOneEvent(event) {
        try {
            const pit = this.pageIndexTracker
            const wasDetached = pit.getIsDetached()
            const newPage = pit.pushEvent(event)
            if (!newPage) return
            if (wasDetached) return
            if (pit.getLength() >= this.maxViewLength) {
                pit.shift()
            }
            pit.push(newPage)
        }
        catch (err) {
            console.error("error pushing event:")
            console.error(event)
            console.error(err)
        }
    }
    getViewModel() {
        const all = this._getVisiblePages()
        return this.viewModelMapper.mapPages(all)
    }
    _getVisiblePages() {
        const p = this.pageIndexTracker
        if (p.getIsDetached()) return p.getScreen()
        if (p.getLastPage() === null) return p.getScreen()
        return p.getScreen().concat([p.getLastPage()])
    }
    getTouchesTop() {
        return this.pageIndexTracker.getTouchesTop()
    }
    getIsDetached() {
        return this.pageIndexTracker.getIsDetached()
    }
    getPreviousPageIdx() {
        return this.pageIndexTracker.getPreviousPageIdx()
    }
    getNextPageIdx() {
        return this.pageIndexTracker.getNextPageIdx()
    }
    prependPage(page) {
        const p = this.pageIndexTracker
        if (p.getLength() >= this.maxViewLength) p.pop()
        p.unshift(page)
    }
    appendPage(page) {
        const p = this.pageIndexTracker
        if (p.getIsContiguous()) {
            throw new Error('contiguous append')
        }
        p.shift()
        p.push(page)
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
