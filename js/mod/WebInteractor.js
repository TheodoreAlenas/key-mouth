import presentMoment from './presentMoment.js'

export default class WebInteractor {
    setSetOldMoments(v) {this.setOldMoments = v}
    setSetLastMoment(v) {this.setLastMoment = v}
    setSetInputValue(v) {this.setInputValue = v}
    setOnReadySocket(f) {this.onReadySocket = f}
    constructor(env, session) {
        try {
            return this.constructorUnhandled(env, session)
        }
        catch (e) {
            console.error("Error constructing web interactor, args: " +
                          JSON.stringify({env, session}))
            throw e
        }
    }
    constructorUnhandled(env, session) {
        ifSessionIsntStringThrowError(session)
        this.socket = new WebSocket(env.webSocketUri +
                                    "?session=" + encodeURI(session))
        this.setMomentsOnceFetched(env)
        this.onOpenSendVersionAndUnlock(this.socket)
        this.onMessageSetLatest(this.socket)
    }
    getDestructor() {
        const socket = this.socket
        return function() {socket.close()}
    }
    setMomentsOnceFetched(env) {
        const self = this
        fetch(env.lastMomentsUri)
            .then(res => res.json())
            .catch("the response of " + env.lastMomentsUri + "isn't JSON")
            .then(function(moments) {
                if (moments.length == 0) return
                const p = moments.map(m => presentMoment(getConnName, m))
                self.setOldMoments(p.slice(0, -1))
                const last = p[p.length - 1]
                if (last.length !== 0) self.setLastMoment(last)
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
    onMessageSetLatest(socket) {
        const self = this
        socket.addEventListener("message", function(event) {
            try {
                const diffsAndMore = JSON.parse(event.data)
                const diffs = diffsAndMore.curMoment
                const p = presentMoment(getConnName, diffs)
                self.setLastMoment(p)
            }
            catch (e) {
                console.error("Error setting last moment to " + event.data)
                throw e
            }
        })
    }

}

function ifSessionIsntStringThrowError(session) {
    if (typeof(session) !== 'string') {
        throw new Error(
            "session isn't string (.../?session=hello let's say), " +
                "typeof(session) = " + typeof(session) +
                ", session = " + session)
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
