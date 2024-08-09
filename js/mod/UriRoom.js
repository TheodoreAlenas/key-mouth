
export default class UriRoom {
    constructor([http, host, port], room) {
        ifRoomIsntStringThrowError(room)
        this.room = room
        this.http = http + '://'
        this.hostPort = host + ':' + port
    }
    home() {
        return this.http + this.hostPort
    }
    webSocket() {
        return "ws://" + this.hostPort +
            "?room=" + encodeURI(this.room)
    }
    lastMoments() {
        return this.http + this.hostPort +
            "/last?room=" + encodeURI(this.room)
    }
    momentsRange(start, end) {
        return this.http + this.hostPort +
            "/moments?room=" + encodeURI(this.room) +
            "&start=" + start +
            "&end=" + end
    }
    fetchPutRoom() {
        const u = this.http + this.hostPort +
              "/room?name=" + encodeURI(this.room)
        return fetch(u, {method: "PUT"})
    }
}

function ifRoomIsntStringThrowError(room) {
    if (typeof(room) !== 'string') {
        throw new Error(
            "room isn't string (.../?room=hello let's say), " +
                "typeof(room) = " + typeof(room) +
                ", room = " + room)
    }
}
