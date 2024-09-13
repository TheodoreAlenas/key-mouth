import EventPresenter from './EventPresenter.js'

export default class Presenter {
    constructor(pageSize) {
        this.pageSize = pageSize
        this.ep = null
    }
    push(event) {
        if (this.ep === null) {
            this.ep = new EventPresenter(event.momentIdx, this.pageSize)
        }
        this.ep.push(event)
    }
    getViewModel(getConnName) {
        return this.ep.getMomentViews(getConnName)
    }
}
