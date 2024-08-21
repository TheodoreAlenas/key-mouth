import EventPresenter from './EventPresenter.js'
import TestCase from './TestCase.js'

const test = new TestCase()
let ep = null

ep = new EventPresenter()
test.assertEqual(
    "none is none",
    [],
    ep.getMomentViews(x => x)
)

ep = new EventPresenter()
ep.push({connId: 4, type: "write", body: "llo"})
ep.push({connId: 4, type: "delete", body: "llo"})
ep.push({connId: 4, type: "delete", body: "e"})
ep.push({connId: 4, type: "delete", body: "h"})
ep.push({connId: 4, type: "disconnect", body: null})
test.assertEqual(
    "write 2 delete 1 delete 1 delete 1 disconnect",
    [{time: null, diffs: [
        {name: "con4", message: [
            {type: "delete", body: "he"},
            {type: "erase", body: "llo"},
            {type: "event", body: "[disconnected]"}
        ]}
    ]}],
    ep.getMomentViews(x => "con" + x)
)

ep = new EventPresenter()
ep.push({connId: 4, type: "write", body: "h"})
ep.push({connId: 5, type: "write", body: "HELLO"})
ep.push({connId: 4, type: "write", body: "i"})
test.assertEqual(
    "a writes, b writes, a writes",
    [{time: null, diffs: [
        {name: "con4", message: [{type: "write", body: "hi"}]},
        {name: "con5", message: [{type: "write", body: "HELLO"}]}
    ]}],
    ep.getMomentViews(x => "con" + x)
)

ep = new EventPresenter()
ep.push({connId: 0, type: "endOfMoment", body: 732})
let v = ep.getMomentViews(x => "con" + x)
for (let e of v) if (typeof(e.time) == 'string') e.time = 'times erased'
test.assertEqual(
    "only end of moment",
    [{"time": "times erased", "diffs": []}],
    v
)

ep = new EventPresenter()
ep.push({connId: 4, type: "write", body: "HELLO"})
ep.push({connId: 0, type: "endOfMoment", body: 732})
ep.push({connId: 4, type: "write", body: "hi again"})
v = ep.getMomentViews(x => "con" + x)
for (let e of v) if (typeof(e.time) == 'string') e.time = 'times erased'
test.assertEqual(
    "only end of moment",
    [
        {"time": "times erased", "diffs": [{
            "name": "con4",
            "message": [{"type": "write", "body": "HELLO"}]
        }]},
        {"time": null, "diffs": [{
            "name": "con4",
            "message": [{"type": "write", "body": "hi again"}]
        }]},
    ],
    v
)

test.printResults()
if (test.getFails() !== 0) process.exit(1)
