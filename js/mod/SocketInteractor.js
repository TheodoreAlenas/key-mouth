import presentMoment from './presentMoment.js'

export default class SocketInteractor {
    constructor(setMessages, setLatest, setInputValue) {
        this.s = new WebSocket("ws://localhost:8000")
        this.inp = ""
        this.setInputValue = setInputValue
        setMomentsOnceFetched(setMessages, setLatest)
        onOpenSendVersion(this.s)
        onMessageSetLatest(this.s, setLatest)
    }
    getFunctionThatClosesSocket() {
        const s = this.s
        return function() {s.close()}
    }
    onClear() {
        this.inp = ""
        this.setInputValue("")
        this.s.send("clear")
    }
    onInputChange(newValue) {
        if (newValue === this.inp) return
        const d = getDiff(this.inp, newValue)
        this.inp = newValue
        this.setInputValue(newValue)
        const s = this.s
        d.forEach(function(e) {s.send(e)})
    }
}

function setMomentsOnceFetched(setMessages, setLatest) {
    fetch("http://localhost:8000/last")
        .then(res => res.json())
        .then(function(res) {
            if (res.length == 0) return
            const p = res.map(r => presentMoment(getConnName, r))
            setMessages(p.slice(0, -1))
            const last = p[p.length - 1]
            if (last.length !== 0) setLatest([last])
        })
}

function onOpenSendVersion(socket) {
    socket.addEventListener("open", function() {
        socket.send('{"version": 0}')
    })
}

function onMessageSetLatest(socket, setLatest) {
    socket.addEventListener("message", function(event) {
        const diffsAndMore = JSON.parse(event.data)
        const diffs = diffsAndMore.curMoment
        const p = [presentMoment(getConnName, diffs)]
        setLatest(p)
    })
}

function getConnName(conn) {
    if (conn % 2) return "Vaggas" + conn
    return "Sotiris" + conn
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
    throw Exception("can't handle diff, a: " + a + ", b: " + b)
}
