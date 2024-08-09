
export default class UriHome {
    constructor([[httpUi, hostUi, portUi],
                 [httpApi, hostApi, portApi]]) {
        this.httpUi = httpUi + '://'
        this.httpApi = httpApi + '://'
        this.hostPortUi = hostUi + ':' + portUi
        this.hostPortApi = hostApi + ':' + portApi
    }
    home() {
        return this.httpUi + this.hostPortUi
    }
    room(room) {
        return this.httpUi + this.hostPortUi +
            "/room?name=" + encodeURI(room)
    }
    rooms() {
        return this.httpApi + this.hostPortApi + '/'
    }
}
