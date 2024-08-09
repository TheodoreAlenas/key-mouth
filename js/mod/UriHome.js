
export default class UriHome {
    constructor([http, host, port]) {
        this.http = http + '://'
        this.hostPort = host + ':' + port
    }
    home() {
        return this.http + this.hostPort
    }
    room(room) {
        return this.http + this.hostPort +
            "/room?name=" + encodeURI(room)
    }
}
