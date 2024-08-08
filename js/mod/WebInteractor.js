import Io from './Io.js'
import presentMoment from './presentMoment.js'

export default class WebInteractor {
    setSetOldMoments(v) {this.setOldMoments = v}
    setSetLastMoment(v) {this.setLastMoment = v}
    setSetInputValue(v) {this.setInputValue = v}
    setOnReadySocket(f) {this.onReadySocket = f}
    constructor(uri) {
        try {
            return this.constructorUnhandled(uri)
        }
        catch (e) {
            console.error("Error constructing web interactor, " +
                          "typeof(uri) = " + uri + " (exp object)")
            throw e
        }
    }
    constructorUnhandled(uri) {
        const self = this
        function onReadySocket(io) {
            self.onReadySocket(new Unlocked(io, self.setInputValue))
        }
        this.io = new Io(uri, onReadySocket)
        this.cached = []
        this._setMomentsOnceFetched()
        function setLast(n, last) {self._setLast(n, last)}
        this.io.onMomentsMessage(setLast)
    }
    getDestructor() {
        return this.io.getDestructor()
    }
    _setMomentsOnceFetched(io) {
        const self = this
        this.io.withLastMoments(function(res) {
            try {
                self._setMomentsOnceFetchedInner(res)
            }
            catch (err) {
                console.error("Error setting last moments from " +
                              JSON.stringify(res))
                throw err
            }
        })
    }
    _setMomentsOnceFetchedInner({start, end, moments}) {
        const p = moments.map(m => presentMoment(getConnName, m))
        this.cached = p
        this.lastMomentN = end
        this.setOldMoments(p)
    }
    _setLast(n, last) {
        try {
            const p = presentMoment(getConnName, last)
            this.setLastMoment(p)
            this._updateOldMoments(n)
        }
        catch (e) {
            console.error("Error setting last moment, " +
                          JSON.stringify({n, last}))
            throw e
        }
    }
    _updateOldMoments(n) {
        if (n == this.lastMomentN) return
        if (n < this.lastMomentN) {
            throw new Error("Error updating old moments, got n = " +
                            n + " < self.lastMomentN = " +
                            this.lastMomentN)
        }
        const self = this
        this.io.withMomentsRange(this.lastMomentN, n, function(res) {
            self._updateOldMomentsInner(n, res)
        })
    }
    _updateOldMomentsInner(n,  moments) {
        const p = moments.map(
            m => presentMoment(getConnName, m))
        this.lastMomentN = n
        this.cached = this.cached.concat(p)
        this.setOldMoments(this.cached)
    }

}

function getConnName(conn) {
    if (conn % 2) return "Vaggas" + conn
    return "Sotiris" + conn
}

class Unlocked {
    constructor(io, setInputValue) {
        this.io = io
        this.inputValue = ""
        this.setInputValue = setInputValue
    }
    onClear() {
        this.inputValue = ""
        this.setInputValue("")
        this.io.sendOne("clear")
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
        this.io.sendList(d)
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
