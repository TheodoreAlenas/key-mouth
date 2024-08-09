
export default class UriRoom {
    constructor([ws, [http, pre]], room) {
        ifRoomIsntStringThrowError(room)
        this.room = room
        this.ws = ws
        this.http = http + '://'
        this.pre = pre + '/' + encodeURI(this.room)
    }
    webSocket() {
        return this.ws + '/' + encodeURI(this.room)
    }
    lastMoments() {
        return this.http + this.pre
    }
    momentsRange(start, end) {
        return this.http + this.pre +
            "?start=" + start +
            "&end=" + end
    }
    fetchPutRoom() {
        const u = this.http + this.pre
        const f = fetch(u, {method: "PUT"})
        f.catch(function(err) {
            console.error("can't fetch PUT room at " + u)
        })
        return f
    }
}

function ifRoomIsntStringThrowError(room) {
    if (typeof(room) !== 'string') {
        throw new Error("room isn't string, " +
                        "typeof(room) = " + typeof(room) +
                        ", room = " + room)
    }
}
