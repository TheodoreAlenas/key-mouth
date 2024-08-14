
export default class UriRoom {
    constructor({ws, api}, room) {
        ifRoomIsntStringThrowError(room)
        this.ws = ws + '/' + encodeURI(room)
        this.api = api + '/' + encodeURI(room)
    }
    webSocket() {
        return this.ws
    }
    lastMoments() {
        return this.api
    }
    momentsRange(start, end) {
        return this.api + "?start=" + start + "&end=" + end
    }
    fetchPutRoom() {
        const f = fetch(this.api, {method: "PUT"})
        f.catch(function(err) {
            console.error("can't fetch PUT room at " + this.api)
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
