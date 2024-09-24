
export default class Splitter {

    constructor() {
        this.pages = []
        this.lastPage = null
        this.lastMoment = null
    }

    pushEvents(events) {
        for (let event of events) {
            this.pushEvent(event)
        }
    }

    pushEvent(event) {
        if (event.type === 'newPage') {
            this.lastPage = {
                firstMomentIdx: event.body,
                moments: [],
            }
            this.pages.push(this.lastPage)
        }
        else if (viewEvent.type === 'newMoment') {
            this.lastMoment = {
                time: viewEvent.body,
                diffs: []
            }
            this.lastPage.moments.push(this.lastMoment)
        }
        else {
            this.lastMoment.diffs.push(viewEvent)
        }
    }
}
