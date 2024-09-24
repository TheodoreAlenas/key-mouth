import PagesPresenter from './PagesPresenter.js'

export default class Presenter {
    constructor({pagesPresenter}) {
        this.pagesPresenter = pagesPresenter
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
        if (this.pagesPresenter.getTouchesTop() === false) {
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
