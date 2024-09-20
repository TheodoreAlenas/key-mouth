
// License at the bottom

import Io from './Io.js'
import Presenter from './Presenter.js'

export default class Controller {
    setMoments(v) {this._sayUnset('setMoments', v)}
    setInputValue(v) {this._sayUnset('setInputValue', v)}
    onReadySocket(v) {this._sayUnset('onReadySocket', v)}
    onSocketError(v) {this._sayUnset('onSocketError', v)}
    _sayUnset(f, v) {
        let j = null
        try {j = JSON.stringify(v)}
        finally {throw new Error(f + ' unset, arg: ' + (j ? j : v))}
    }
    constructor(args) {
        try {
            this._constructor(args)
        }
        catch (e) {
            console.error("Error constructing the controller, args:")
            console.error(args)
            throw e
        }
    }
    _constructor({uri, maxPages, eavesdropper}) {
        const self = this
        function onReadySocket(io) {
            self.onReadySocket(new Unlocked(io, self.setInputValue))
        }
        function onSocketError(arg) {
            self.onSocketError(arg)
        }
        this.io = new Io({uri, onReadySocket, onSocketError})
        this.presenter = new Presenter({maxPages})
        this.io.onEvent(function(event) {
            if (eavesdropper) eavesdropper(event)
            self.presenter.push(event)
            self.setMoments(self.presenter.getViewModel(getConnName))
        })
    }
    close() {
        this.io.close()
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
