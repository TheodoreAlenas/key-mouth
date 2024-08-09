
export default class UriRoom {
    constructor([http, host, port], room) {
        ifRoomIsntStringThrowError(room)
        this.room = room
        this.http = http + '://'
        this.hostPortRoom = host + ':' + port +
            '/' + encodeURI(this.room)
    }
    webSocket() {
        return "ws://" + this.hostPortRoom
    }
    lastMoments() {
        return this.http + this.hostPortRoom
    }
    momentsRange(start, end) {
        return this.http + this.hostPortRoom +
            "?start=" + start +
            "&end=" + end
    }
    fetchPutRoom() {
        const u = this.http + this.hostPortRoom
        return fetch(u, {method: "PUT"})
    }
}

function ifRoomIsntStringThrowError(room) {
    if (typeof(room) !== 'string') {
        throw new Error("room isn't string, " +
                        "typeof(room) = " + typeof(room) +
                        ", room = " + room)
    }
}
