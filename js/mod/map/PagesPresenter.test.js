import PagesPresenter from './PagesPresenter.js'
import ViewModelMapper from './ViewModelMapper.js'
import TestCase from '../TestCase.js'
import Splitter from './Splitter.js'

const test = new TestCase('PagesPresenter')
let p = null
let v = null

function newPP(n) {
    return new PagesPresenter({
        maxPages: n,
        viewModelMapper: new ViewModelMapper({
            nameMapper: {mapName: x => 'con' + x}
        }),
        splitter: new Splitter()
    })
}

test.wrap(function() {
    p = newPP(2)
    v = p.getViewModel()
    test.assertEqual("none is none", [], v)
})

const exp = [
    {key: 7, time: "times erased", names: ["con4"], messages: [
        [{type: "write", body: "one"}]
    ]},
    {key: 8, time: "times erased", names: ["con4"], messages: [
        [{type: "write", body: "two"}]
    ]},
    {key: 9, time: "times erased", names: ["con4"], messages: [
        [{type: "write", body: "three"}]
    ]},
]

p = newPP(2)
test.wrap(function() {
    p.pushEvent({firstPageIdx: 0, events: []})
    v = p.getViewModel()
    test.assertEqual("no page, no moment, empty view model", [], v)
    test.assertEqual("no events, touches top", true, p.getTouchesTop())
})

p = newPP(2)
test.wrap(function() {
    p.pushEvent({firstPageIdx: 0, events: []})
    p.pushEvent({connId: 0, type: "newPage", body: 7})
    p.pushEvent({connId: 0, type: "newMoment", body: 732.0})
    p.pushEvent({connId: 4, type: "write", body: "one"})
    p.pushEvent({connId: 0, type: "newPage", body: 8})
    p.pushEvent({connId: 0, type: "newMoment", body: 1024.0})
    p.pushEvent({connId: 4, type: "write", body: "two"})
    v = p.getViewModel()
    for (let e of v) for (let e2 of e.moments) e2.time = 'times erased'
    test.assertEqual("2 pages 1 moment each",
                     [{moments: [exp[0]]}, {moments: [exp[1]]}],
                     v)
    test.assertEqual("2 pages, still at top", true, p.getTouchesTop())
})

test.wrap(function() {
    p.pushEvent({connId: 0, type: "newPage", body: 9})
    p.pushEvent({connId: 0, type: "newMoment", body: 17326.0})
    p.pushEvent({connId: 4, type: "write", body: "three"})
    v = p.getViewModel()
    for (let e of v) for (let e2 of e.moments) e2.time = 'times erased'
    test.assertEqual("maxPages 2, 3 pages, got last 2",
                     [{moments: [exp[1]]}, {moments: [exp[2]]}],
                     v)
    test.assertEqual("pages > max, not at top", false, p.getTouchesTop())
})

export default test
