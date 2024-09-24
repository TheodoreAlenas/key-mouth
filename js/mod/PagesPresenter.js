import ViewModelMapper from './ViewModelMapper.js'
import Splitter from './Splitter.js'

export default class PagesPresenter {

    constructor({maxPages, viewModelMapper}) {
        this.maxPages = maxPages
        if (typeof(maxPages) !== 'number') {
            throw new Error("typeof(maxPages) = " + typeof(maxPages))
        }
        this.viewModelMapper = viewModelMapper
        this.firstPageIdx = null
        this.lastPageIdx = null
        this.above = new Splitter()
        this.last = new Splitter()
        this.isBeginning = true
    }
    pushEvent(event) {
        this._pushFirstBatch(event)
        this.pushEvent = this._pushOneEvent
    }
    _pushFirstBatch(event) {
        try {
            this.firstPageIdx = event.firstPageIdx
            this.lastPageIdx = event.firstPageIdx
            for (let e of event.events) this.last.pushEvent(e)
        }
        catch (err) {
            console.error("error pushing initial load:")
            console.error(event)
            console.error(err)
        }
    }
    _pushOneEvent(event) {
        try {
            const r = this.last.pushEvent(event)
            if (r === 'new page') {
                this.lastPageIdx += 1
                if (this.last.pages.length > this.maxPages) {
                    this.last.pages.shift()
                    this.firstPageIdx += 1
                }
            }
        }
        catch (err) {
            console.error("error pushing event:")
            console.error(event)
            console.error(err)
        }
    }
    getViewModel() {
        return this.viewModelMapper.mapPages(this.last.pages)
    }
    getTouchesTop() {
        return this.firstPageIdx === 0
    }
}
