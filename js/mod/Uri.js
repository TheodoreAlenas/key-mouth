
export default class Uri {
    constructor(mode, room) {
        ifRoomIsntStringThrowError(room)
        this.room = room
        if (mode === "dev") {
            this.http = "http://"
            this.hostPort = "localhost:8000"
        }
        else if (mode == "systest") {
            this.http = "http://"
            this.hostPort = "localhost:8001"
        }
        else {
            throw new Error("Invalid Uri mode in constructor: " + mode)
        }
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
