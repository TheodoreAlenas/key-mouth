
// License at the bottom

import Io from './Io.js'
import presentMoment from './presentMoment.js'

export default class WebInteractor {
    setSetMoments(v) {this.setMoments = v}
    setSetInputValue(v) {this.setInputValue = v}
    setOnReadySocket(f) {this.onReadySocket = f}
    constructor(uri) {
        try {
            this.constructorUnhandled(uri)
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
        this.cached = {}
        this._setMomentsOnceFetched()
        function setLast(n, last) {self._setLast(n, last)}
        this.io.onLastMomentUpdate(setLast)
    }
    getDestructor() {
        return this.io.getDestructor()
    }
    _setMomentsOnceFetched() {
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
    _updateOldMoments(n) {
        if (this.lastMomentN === undefined) return
        if (n == this.lastMomentN) return
        if (n < this.lastMomentN) {
            throw new Error("Error updating old moments, got n = " +
                            n + " < self.lastMomentN = " +
                            this.lastMomentN)
        }
        const self = this
        const oldLastMomentN = this.lastMomentN
        this.lastMomentN = n
        this.io.withMomentsRange(oldLastMomentN, n, function(moments) {
            self._updateOldMomentsInner(oldLastMomentN, moments)
        })
    }
    _setMomentsOnceFetchedInner({start, end, moments}) {
        const p = moments.map(m => ({
            people: presentMoment(getConnName, m.diffs),
            time: m.time
        }))
        for (let i = 0; i < p.length; i++) this.cached[i + start] = p[i]
        this.lastMomentN = end
        this._setMomentsFromCached()
    }
    _updateOldMomentsInner(oldLastMomentN, moments) {
        const p = moments.map(m => ({
            people: presentMoment(getConnName, m.diffs),
            time: m.time
        }))
        const start = oldLastMomentN
        for (let i = 0; i < p.length; i++) this.cached[i + start] = p[i]
        this._setMomentsFromCached()
    }
    _setMomentsFromCached() {
        const keys = Object.keys(this.cached)
        const s = keys.map(k => this._keyToMoment(k))
        this.setMoments(s)
    }
    _keyToMoment(k) {
        const e = this.cached[k]
        if (e.time) return {
            key: k, body: e.people,
            time: (new Date(e.time)).toLocaleString()
        }
        return {key: k, body: e.people}
    }
    _setLast(n, last) {
        try {
            const p = presentMoment(getConnName, last)
            this.cached[n] = {people: p, time: undefined}
            this._setMomentsFromCached()
            this._updateOldMoments(n)
        }
        catch (e) {
            console.error("Error setting last moment, " +
                          JSON.stringify({n, last}))
            throw e
        }
    }

}

function getConnName(conn) {
    return "Visitor#" + conn
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
        return ["-" + a.substr(b.length)]
    }
    if (b.startsWith(a)) {
        return ["+" + b.substr(a.length)]
    }
    for (let i = 0; i < a.length && i < b.length; i++) {
        if (a[i] !== b[i]) {
            return ["-" + a.substr(i), "+" + b.substr(i)]
        }
    }
    throw new Error("can't handle diff, a: " + a + ", b: " + b)
}

/*
Copyright 2024 <dimakopt732@gmail.com>

Permission is hereby granted, free of charge, to any person obtaining a
copy of this software and associated documentation files
(the “Software”), to deal in the Software without restriction,
including without limitation the rights to use, copy, modify, merge,
publish, distribute, sublicense, and/or sell copies of the Software,
and to permit persons to whom the Software is furnished to do so,
subject to the following conditions:

The above copyright notice and this permission notice shall be included
in all copies or substantial portions of the Software.

THE SOFTWARE IS PROVIDED “AS IS”, WITHOUT WARRANTY OF ANY KIND,
EXPRESS OR IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF
MERCHANTABILITY, FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT.
IN NO EVENT SHALL THE AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR
ANY CLAIM, DAMAGES OR OTHER LIABILITY, WHETHER IN AN ACTION OF CONTRACT,
TORT OR OTHERWISE, ARISING FROM, OUT OF OR IN CONNECTION WITH THE
SOFTWARE OR THE USE OR OTHER DEALINGS IN THE SOFTWARE.
*/
