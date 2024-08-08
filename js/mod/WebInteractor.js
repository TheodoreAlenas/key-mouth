import presentMoment from './presentMoment.js'

export default class WebInteractor {
    setSetOldMoments(v) {this.setOldMoments = v}
    setSetLastMoment(v) {this.setLastMoment = v}
    setSetInputValue(v) {this.setInputValue = v}
    setOnReadySocket(f) {this.onReadySocket = f}
    constructor(env, room) {
        try {
            return this.constructorUnhandled(env, room)
        }
        catch (e) {
            console.error("Error constructing web interactor, args: " +
                          JSON.stringify({env, room}))
            throw e
        }
    }
    constructorUnhandled(env, room) {
        ifRoomIsntStringThrowError(room)
        this.cachedPresentedOldMoments = []
        this.socket = new WebSocket(env.webSocketUri +
                                    "?room=" + encodeURI(room))
        this.setMomentsOnceFetched(env, room)
        this.onOpenSendVersionAndUnlock(this.socket)
        this.onMessageSetLatest(env, this.socket)
    }
    getDestructor() {
        const socket = this.socket
        return function() {socket.close()}
    }
    withJsonFetched(uri, callback) {
        const withStr = fetch(uri)
        withStr.catch(function(err) {
            console.error("Error, can't fetch " + uri)
            throw err
        })
        const withJson = withStr.then(function(err) {
            if (res.status !== 200) {
                throw new Error("Error, fetched " + uri +
                                " with status " + res.status)
            }
            return res.json()
        })
        withJson.then(callback)
        withJson.catch(function(err) {
            console.error("Error, res.json() failed, " + uri)
            throw err
        })
    }
    setMomentsOnceFetched(env, room) {
        const self = this
        const lastMomRoom = env.lastMomentsUri +
              "?room=" + encodeURI(room)
        this.withJsonFetched(lastMomRoom, function(moments) {
            try {
                if (moments.length == 0) return
                const p = moments.map(m => presentMoment(getConnName, m))
                self.cachedPresentedOldMoments = p
                self.lastMomentN = null
                self.setOldMoments(p)
            }
            catch (err) {
                console.error("Error setting last moments to " +
                              JSON.stringify(moments))
                throw err
            }
        })
    }
    onOpenSendVersionAndUnlock(socket) {
        const self = this
        socket.addEventListener("open", function() {
            try {
                socket.send('{"version": 0}')
                self.onReadySocket(new Unlocked(socket, self.setInputValue))
            }
            catch (e) {
                console.error("Error sending version or unlocking input")
                throw e
            }
        })
    }
    onMessageSetLatest(env, socket) {
        const self = this
        socket.addEventListener("message", function(event) {
            try {
                const {n, last} = JSON.parse(event.data)
                const p = presentMoment(getConnName, last)
                self.setLastMoment(p)
                if (n == self.lastMomentN) return
                if (n < self.lastMomentN) {
                    console.error("Error, got n = " + n +
                                  " < self.lastMomentN = " +
                                  self.lastMomentN)
                }
                fetch(env.momentsRangeUri, function)
                self.lastMomentN = n
                const l = presentMoment(getConnName, n)
                self.cachedPresentedOldMoments =
                    self.cachedPresentedOldMoments.concat([l])
                self.setOldMoments(self.cachedPresentedOldMoments)
            }
            catch (e) {
                console.error("Error setting last moment to " +
                              event.data)
                throw e
            }
        })
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

function getConnName(conn) {
    if (conn % 2) return "Vaggas" + conn
    return "Sotiris" + conn
}

class Unlocked {
    constructor(socket, setInputValue) {
        this.socket = socket
        this.inputValue = ""
        this.setInputValue = setInputValue
    }
    onClear() {
        this.inputValue = ""
        this.setInputValue("")
        this.socket.send("clear")
    }
    onInputChange(newValue) {
        const oldValue = this.inputValue
        try {
            this.onInputChangeUnhandled(newValue)
        }
        catch (e) {
            console.error("Error changing input '" + oldValue +
                          "' -> '" + newValue + "'")
            throw e
        }
    }
    onInputChangeUnhandled(newValue) {
        if (newValue === this.inputValue) return
        const d = getDiff(this.inputValue, newValue)
        this.inputValue = newValue
        this.setInputValue(newValue)
        const s = this.socket
        d.forEach(function(e) { trySending(s, e, d) })
    }
}

function getDiff(a, b) {
    if (a.startsWith(b)) {
        return ["-", a.substr(b.length)]
    }
    if (b.startsWith(a)) {
        return ["+", b.substr(a.length)]
    }
    for (let i = 0; i < a.length && i < b.length; i++) {
        if (a[i] !== b[i]) {
            return [":", a.substr(i), b.substr(i)]
        }
    }
    throw new Error("can't handle diff, a: " + a + ", b: " + b)
}

function trySending(s, e, d) {
    try {
        s.send(e)
    }
    catch (err) {
        console.error("Error sending " + JSON.stringify(d) +
                      ", maybe set input before init")
        throw err
    }
}
