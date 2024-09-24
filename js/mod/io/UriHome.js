
export default class UriHome {
    constructor({ui, api}) {
        this.ui = ui
        this.api = api
    }
    home() {
        return this.ui + '/'
    }
    room(room) {
        return this.ui + "/room?name=" + encodeURI(room)
    }
    rooms() {
        return this.api + '/'
    }
}
