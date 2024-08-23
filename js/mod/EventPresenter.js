
// License at the bottom

import accumulateDiffs from './accumulateDiffs.js'

export default class EventPresenter {

    constructor(firstMomentIdx) {
        if (typeof(firstMomentIdx) !== 'number') {
            throw new Error(
                "firstMomentIdx isn't number: " + firstMomentIdx)
        }
        this.firstMomentIdx = firstMomentIdx
        this.moments = []
        this.last = []
    }
    push(viewEvent) {
        if (viewEvent.type === 'endOfMoment') {
            this.moments.push({
                time: viewEvent.body,
                raw: this.last
            })
            this.last = []
        }
        else {
            this.last.push(viewEvent)
        }
    }
    getMomentViews(getNames) {
        let i = this.firstMomentIdx
        const views = this.moments.map(({time, raw}) => ({
            key: i++,
            time: presentTimeFromSecondsSince1970(time),
            body: getViewModel(getNames, raw)
        }))
        if (this.last.length !== 0) views.push({
            key: i,
            time: null,
            body: getViewModel(getNames, this.last)
        })
        return views
    }
    // future idea: updateNames(getNames) and getMomentViews()
    // to pre - bake the views and relax the garbage collector
}

function presentTimeFromSecondsSince1970(secondsSince1970) {
    const msSince1970 = Math.ceil(secondsSince1970 * 1000)
    const msOf24h = 1000 * 60 * 60 * 24
    const now = Date.now()
    const date = new Date(msSince1970)
    if (now - msSince1970 < msOf24h) {
        return date.toLocaleTimeString()
    }
    return date.toLocaleString()
}

function getViewModel(getNames, events) {
    const massaged = events.map(massageEvent)
    const r = accumulateDiffs(massaged)
    const ans = r.map(({connId, message}) => ({
        name: getNames(connId),
        message
    }))
    return ans
}

function massageEvent(event) {
    if (event.type === 'connect') return {
        connId: event.connId,
        type: 'event',
        body: '[connected]'
    }
    if (event.type === 'disconnect') return {
        connId: event.connId,
        type: 'event',
        body: '[disconnected]'
    }
    if (event.type === 'shutdown') return {
        connId: event.connId,
        type: 'event',
        body: '[server shutting down]'
    }
    return event
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
