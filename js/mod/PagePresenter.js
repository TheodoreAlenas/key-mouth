
// License at the bottom

import accumulateDiffs from './accumulateDiffs.js'

/*
  pastMoments
  lastMoments   doesn't overlap pastMoments
  lastMoment

  There's a load later messages button.
  If the lastMoments touch the pastMoments,
  they merge and the ceiling lowers.
  If the lastMoments have some of the desired moments,
  these moments are kept and the in-between are fetched from the DB.
  If the lastMoments don't have any of the desired moments,
  all those moments are fetched from the DB.
 */

export default class PagePresenter {

    constructor(firstMomentIdx) {
        if (typeof(firstMomentIdx) !== 'number') {
            throw new Error(
                "firstMomentIdx isn't number: " + firstMomentIdx)
        }
        this.firstMomentIdx = firstMomentIdx
        this.moments = []
        this.last = []
        this.lastTime = null
    }
    push(viewEvent) {
        if (viewEvent.type === 'newMoment') {
            this.moments.push({
                time: this.lastTime,
                raw: this.last
            })
            this.last = []
            this.lastTime = viewEvent.body
        }
        else {
            this.last.push(viewEvent)
        }
    }
    getMomentViews(getNames) {
        let i = this.firstMomentIdx
        const views = this.moments.map(({time, raw}) =>
            getViewModel(i++, presTime(time), getNames, raw))
        if (this.last.length !== 0) views.push(
            getViewModel(i, presTime(this.lastTime), getNames,
                         this.last))
        return views
    }
    touchesTop() {
        return this.firstMomentIdx === 0
    }
    keepLast(n) {
        if (n > this.moments.length) return
        const ground = this.moments.length - n
        this.moments = this.moments.filter((_, i) => i > ground)
        this.firstMomentIdx += n
    }
}

function presTime(secondsSince1970) {
    if (secondsSince1970 === null) return null
    const msSince1970 = Math.ceil(secondsSince1970 * 1000)
    const msOf24h = 1000 * 60 * 60 * 24
    const now = Date.now()
    const date = new Date(msSince1970)
    if (now - msSince1970 < msOf24h) {
        return date.toLocaleTimeString()
    }
    return date.toLocaleString()
}

function getViewModel(key, time, getNames, events) {
    const massaged = events.map(massageEvent)
    const r = accumulateDiffs(massaged)
    const names = r.map(e => getNames(e.connId))
    const messages = r.map(e => ({message: e.message}))
    return {key, time, names, messages}
}

function massageEvent(event) {
    if (event.type === 'write') return event
    if (event.type === 'delete') return event

    let body = null
    if (event.type === 'connect') body = '[connected]'
    else if (event.type === 'disconnect') body = '[disconnected]'
    else if (event.type === 'shutdown') body = '[server shutting down]'
    else if (event.type === 'start') body = '[server started]'
    else if (event.type === 'create') body = '[room created]'
    else throw new Error("unknown type on event: " + event)
    return {
        connId: event.connId,
        type: 'event',
        body
    }
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
