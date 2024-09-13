import EventPresenter from './EventPresenter.js'

export default class Presenter {
    constructor(pageSize) {
        this.pageSize = pageSize
        this.ep = null
    }
    push(event) {
        if (this.ep === null) {
            this.ep = new EventPresenter(event.firstMomentIdx)
            for (let e of event.moments) this.ep.push(e)
            this.ep.keepLast(this.pageSize)
        }
        else {
            this.ep.push(event)
            this.ep.keepLast(this.pageSize)
        }
    }
    getViewModel(getConnName) {
        const r = {
            moreTopButton: null,
            moreBottomButton: null,
            moments: this.ep.getMomentViews(getConnName)
        }
        if (!this.ep.touchesTop()) {
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
