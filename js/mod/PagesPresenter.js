import PagePresenter from './PagePresenter.js'

export default class PagesPresenter {

    constructor({firstPageIdx, maxPages}) {
        this.firstPageIdx = firstPageIdx
        this.lastPageIdx = firstPageIdx
        this.maxPages = maxPages
        this.above = []
        this.last = []
    }
    pushEvent(event) {
        if (event.type === "newPage") {
            if (this.last.length >= this.maxPages) {
                this.last.shift(1)
                this.firstPageIdx += 1
            }
            this.last.push(new PagePresenter(event.body))
            this.lastPageIdx += 1
        }
        else {
            this.last[this.last.length - 1].pushEvent(event)
        }
    }
    getViewModel(getNames) {
        const vm = []
        for (let page of this.last) {
            for (let moment of page.getMomentViews(getNames)) {
                vm.push(moment)
            }
        }
        return vm
    }
    getTouchesTop() {
        return this.firstPageIdx === 0
    }
    setPageAbove(page) {
        if (this.above.length === 0) {
            this.above.push(page)
            for (let x of this.last) this.above.push(x)
            this.above.pop()
        }
    }
}
