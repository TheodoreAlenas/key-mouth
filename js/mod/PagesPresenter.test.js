import PagesPresenter from './PagesPresenter.js'
import TestCase from './TestCase.js'

const test = new TestCase('PagesPresenter')
let p = null
let v = null

p = new PagesPresenter({firstPageIdx: 0})
test.assertEqual("firstPageIdx 0 touches top", true, p.getTouchesTop())

p = new PagesPresenter({firstPageIdx: 1})
test.assertEqual("firstPageIdx 1 not at top", false, p.getTouchesTop())

p = new PagesPresenter({firstPageIdx: 0})
v = p.getViewModel(x => "con" + x)
test.assertEqual("none is none", [], v)

const exp = [
    {key: 7, time: "times erased", names: ["con4"], messages: [
        [{type: "write", body: "one"}]
    ]},
    {key: 8, time: "times erased", names: ["con4"], messages: [
        [{type: "write", body: "two"}]
    ]},
]

p = new PagesPresenter({firstPageIdx: 0})
v = p.getViewModel(x => "con" + x)
test.assertEqual("no page, no moment, empty view model", [], v)

p = new PagesPresenter({firstPageIdx: 0})
p.push({connId: 0, type: "newPage", body: 7})
p.push({connId: 0, type: "newMoment", body: 732.0})
p.push({connId: 4, type: "write", body: "one"})
v = p.getViewModel(x => "con" + x)
for (let e of v) e.time = 'times erased'
test.assertEqual("1 page 1 moment", [exp[0]], v)

p = new PagesPresenter({firstPageIdx: 0})
p.push({connId: 0, type: "newPage", body: 7})
p.push({connId: 0, type: "newMoment", body: 732.0})
p.push({connId: 4, type: "write", body: "one"})
p.push({connId: 0, type: "newMoment", body: 1024.0})
p.push({connId: 4, type: "write", body: "two"})
v = p.getViewModel(x => "con" + x)
for (let e of v) e.time = 'times erased'
test.assertEqual("1 page 2 moments", exp, v)

p = new PagesPresenter({firstPageIdx: 0})
p.push({connId: 0, type: "newPage", body: 7})
p.push({connId: 0, type: "newMoment", body: 732.0})
p.push({connId: 4, type: "write", body: "one"})
p.push({connId: 0, type: "newPage", body: 8})
p.push({connId: 0, type: "newMoment", body: 1024.0})
p.push({connId: 4, type: "write", body: "two"})
v = p.getViewModel(x => "con" + x)
for (let e of v) e.time = 'times erased'
test.assertEqual("2 pages 1 moment each", exp, v)

function redoV() {
    v = p.getViewModel(x => "con" + x)
    for (let e of v) e.time = 'times erased'
}

p.keepLast(3)
redoV()
test.assertEqual("keepLast(excess) doesn't bother", exp, v)

p.keepLast(2)
redoV()
test.assertEqual("keepLast(len) doesn't bother", exp, v)

p.keepLast(1)
redoV()
test.assertEqual("keepLast(1) keeps last 1", [exp[1]], v)

p.keepLast(0)
redoV()
test.assertEqual("keepLast(0) makes []", [], v)

export default test
