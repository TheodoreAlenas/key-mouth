import PagesPresenter from './PagesPresenter.js'

export default class Presenter {
    constructor({pagesPresenter, withPage}) {
        this.pagesPresenter = pagesPresenter
        this.withPage = withPage
    }
    pushEvent(event) {
        this.pagesPresenter.pushEvent(event)
    }
    getViewModel() {
        const r = {
            moreTopButton: null,
            moreBottomButton: null,
            pages: this.pagesPresenter.getViewModel()
        }
        const pp = this.pagesPresenter
        const withPage = this.withPage
        if (this.pagesPresenter.getTouchesTop() === false) {
            r.moreTopButton = {
                label: "Load previous moments",
                onClick: function() {
                    const i = pp.getPreviousPageIdx()
                    withPage(i, function(p) {pp.prependPage(p)})
                }
            }
        }
        if (this.pagesPresenter.getIsDetached()) {
            r.moreBottomButton = {
                label: "Load later moments",
                onClick: function() {
                    const i = pp.getNextPageIdx()
                    withPage(i, function(p) {pp.appendPage(p)})
                }
            }
        }
        return r
    }
}
