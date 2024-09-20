import PagePresenter from './PagePresenter.js'

export default class PagesPresenter {

    constructor({firstPageIdx}) {
        this.firstPageIdx = firstPageIdx
        this.pages = []
    }
    push(event) {
        if (event.type === "newPage") {
            this.pages.push(new PagePresenter(event.body))
        }
        else {
            this.pages[this.pages.length - 1].push(event)
        }
    }
    getViewModel(getNames) {
        const vm = []
        for (let page of this.pages) {
            for (let moment of page.getMomentViews(getNames)) {
                vm.push(moment)
            }
        }
        return vm
    }
    getTouchesTop() {
        console.log('from PagesPresenter.js')
        console.log(this.firstPageIdx)
        return this.firstPageIdx === 0
    }
    keepLast(n) {
        const len = this.pages.length
        if (n >= len) return
        const r = []
        for (let i = len - n; i < len; i++) r.push(this.pages[i])
        this.pages = r
        this.firstPageIdx += n
    }
}
