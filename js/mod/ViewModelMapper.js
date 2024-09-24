
// License at the bottom

export default class ViewModelMapper {
    constructor(nameMapper) {
        this.nameMapper = nameMapper
    }
    mapPages(pages) {
        return pages.map(p => this.mapPage(p))
    }
    mapPage(page) {
        return page.moments.map((m, i) =>
            this.mapMoment(page.firstMomentIdx + i, m))
    }
    mapMoment(key, moment) {
        const massaged = moment.diffs.map(massageEvent)
        const acc = accumulateDiffs(massaged)

        const time = presTime(moment.time)
        const names = acc.map(e => this.nameMapper.mapName(e.connId))
        const messages = acc.map(e => e.message)
        return {key, time, names, messages}
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
