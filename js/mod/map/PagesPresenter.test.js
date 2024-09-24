import PagesPresenter from './PagesPresenter.js'
import ViewModelMapper from './ViewModelMapper.js'
import TestCase from '../TestCase.js'

const test = new TestCase('PagesPresenter')
let p = null
let v = null

function newPP(n) {
    return new PagesPresenter({
        maxPages: n,
        viewModelMapper: new ViewModelMapper({
            nameMapper: {mapName: x => 'con' + x}
        })
    })
}

p = newPP(1)
v = p.getViewModel()
test.assertEqual("none is none", [], v)

const exp = [
    {key: 7, time: "times erased", names: ["con4"], messages: [
        [{type: "write", body: "one"}]
    ]},
    {key: 8, time: "times erased", names: ["con4"], messages: [
        [{type: "write", body: "two"}]
    ]},
]

p = newPP(2)
p.pushEvent({firstPageIdx: 0, events: []})
v = p.getViewModel()
test.assertEqual("no page, no moment, empty view model", [], v)
test.assertEqual("no events, touches top", true, p.getTouchesTop())

p = newPP(2)
p.pushEvent({firstPageIdx: 0, events: []})
p.pushEvent({connId: 0, type: "newPage", body: 7})
p.pushEvent({connId: 0, type: "newMoment", body: 732.0})
p.pushEvent({connId: 4, type: "write", body: "one"})
v = p.getViewModel()
for (let e of v) for (let e2 of e.moments) e2.time = 'times erased'
test.assertEqual("1 page 1 moment", [{moments: [exp[0]]}], v)
test.assertEqual("1 page, touches top", true, p.getTouchesTop())

p = newPP(2)
p.pushEvent({firstPageIdx: 0, events: []})
p.pushEvent({connId: 0, type: "newPage", body: 7})
p.pushEvent({connId: 0, type: "newMoment", body: 732.0})
p.pushEvent({connId: 4, type: "write", body: "one"})
p.pushEvent({connId: 0, type: "newMoment", body: 1024.0})
p.pushEvent({connId: 4, type: "write", body: "two"})
v = p.getViewModel()
for (let e of v) for (let e2 of e.moments) e2.time = 'times erased'
test.assertEqual("1 page 2 moments", [{moments: exp}], v)
test.assertEqual("1 page 2 moments, at top", true, p.getTouchesTop())

p = newPP(2)
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

p = newPP(1)
p.pushEvent({firstPageIdx: 0, events: []})
p.pushEvent({connId: 0, type: "newPage", body: 7})
p.pushEvent({connId: 0, type: "newMoment", body: 732.0})
p.pushEvent({connId: 4, type: "write", body: "one"})
p.pushEvent({connId: 0, type: "newPage", body: 8})
p.pushEvent({connId: 0, type: "newMoment", body: 1024.0})
p.pushEvent({connId: 4, type: "write", body: "two"})
v = p.getViewModel()
for (let e of v) for (let e2 of e.moments) e2.time = 'times erased'
test.assertEqual("maxPages 1, 2 pages, got last",
                 [{moments: [exp[1]]}],
                 v)
test.assertEqual("pages > max, not at top", false, p.getTouchesTop())

export default test
