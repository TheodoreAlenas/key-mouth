
export default class UriHome {
    constructor([[httpUi, preUi], [httpApi, preApi]]) {
        this.httpUi = httpUi + '://'
        this.httpApi = httpApi + '://'
        this.preUi = preUi
        this.preApi = preApi
    }
    home() {
        return this.httpUi + this.preUi + '/'
    }
    room(room) {
        return this.httpUi + this.preUi +
            "/room?name=" + encodeURI(room)
    }
    rooms() {
        return this.httpApi + this.preApi + '/'
    }
}
