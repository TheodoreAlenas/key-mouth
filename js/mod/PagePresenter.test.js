import PagePresenter from './PagePresenter.js'
import TestCase from './TestCase.js'

const test = new TestCase()
let ep = null
let v = null

ep = new PagePresenter(0)
test.assertEqual(
    "none is none",
    [],
    ep.getMomentViews(x => x)
)

ep = new PagePresenter(7)
ep.push({connId: 0, type: "newMoment", body: 732})
ep.push({connId: 4, type: "write", body: "HELLO"})
ep.push({connId: 0, type: "newMoment", body: 1024})
ep.push({connId: 4, type: "write", body: "hi again"})
v = ep.getMomentViews(x => "con" + x)
for (let e of v) if (typeof(e.time) == 'string') e.time = 'times erased'
test.assertEqual(
    "2 moments",
    [
        {key: 7, time: "times erased", names: ["con4"], messages: [{
            message: [{type: "write", body: "HELLO"}]
        }]},
        {key: 8, time: "times erased", names: ["con4"], messages: [{
            message: [{type: "write", body: "hi again"}]
        }]},
    ],
    v
)

ep = new PagePresenter(7)
ep.push({connId: 0, type: "newMoment", body: 732})
ep.push({connId: 4, type: "write", body: "llo"})
ep.push({connId: 4, type: "delete", body: "llo"})
ep.push({connId: 4, type: "delete", body: "e"})
ep.push({connId: 4, type: "delete", body: "h"})
ep.push({connId: 4, type: "disconnect", body: null})
v = ep.getMomentViews(x => "con" + x)
for (let e of v) if (typeof(e.time) == 'string') e.time = 'times erased'
test.assertEqual(
    "write 2 delete 1 delete 1 delete 1 disconnect",
    [{key: 7, time: "times erased", names: ["con4"], messages: [
        {message: [
            {type: "delete", body: "he"},
            {type: "erase", body: "llo"},
            {type: "event", body: "[disconnected]"}
        ]}
    ]}],
    v
)

ep = new PagePresenter(7)
ep.push({connId: 0, type: "newMoment", body: 732})
ep.push({connId: 4, type: "write", body: "h"})
ep.push({connId: 5, type: "write", body: "HELLO"})
ep.push({connId: 4, type: "write", body: "i"})
v = ep.getMomentViews(x => "con" + x)
for (let e of v) if (typeof(e.time) == 'string') e.time = 'times erased'
test.assertEqual(
    "a writes, b writes, a writes",
    [{key: 7, time: "times erased", names:["con4", "con5"], messages: [
        {message: [{type: "write", body: "hi"}]},
        {message: [{type: "write", body: "HELLO"}]}
    ]}],
    v
)

test.printResults()
if (test.getFails() !== 0) process.exit(1)
