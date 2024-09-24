import PagesPresenter from './PagesPresenter.js'

export default class Presenter {
    constructor({maxPages}) {
        this.maxPages = maxPages
        if (typeof(maxPages) !== 'number') {
            throw new Error("typeof(maxPages) = " + typeof(maxPages))
        }
        this.p = null
    }
    pushEvent(event) {
        if (this.p === null) {
            try {this._pushFirstBatch(event)}
            catch (err) {
                console.error("error pushing initial load:")
                console.error(event)
                console.error(err)
            }
        }
        else {
            try {this._pushOneEvent(event)}
            catch (err) {
                console.error("error pushing single event:")
                console.error(event)
                console.error(err)
            }
        }
    }
    _pushFirstBatch(event) {
        this.p = new PagesPresenter({
            firstPageIdx: event.firstPageIdx,
            maxPages: this.maxPages,
        })
        for (let e of event.events) this.p.pushEvent(e)
    }
    _pushOneEvent(event) {
        this.p.pushEvent(event)
    }
    getViewModel(getConnName) {
        try {return this._getViewModel(getConnName)}
        catch (err) {
            console.error("couldn't get the view model")
            console.error(err)
            throw err
        }
    }
    _getViewModel(getConnName) {
        const r = {
            moreTopButton: null,
            moreBottomButton: null,
            moments: this.p.getViewModel(getConnName)
        }
        if (this.p.getTouchesTop() === false) {
            r.moreTopButton = {
                label: "Load previous messages",
                onClick: function() {
                    alert("not implemented yet")
                }
            }
        }
        return r
    }
}
