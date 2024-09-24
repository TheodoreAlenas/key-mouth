import Controller from './Controller.js'
import UriRoom from './UriRoom.js'
import uriFirstArg from './uriFirstArg.js'
import TestCase from './TestCase.js'

const test = new TestCase('integration test')

const uriRestarted = new UriRoom(uriFirstArg.room, "pre\nmade")
const uriMissing = new UriRoom(uriFirstArg.room, "doesn't exist")
const uriNew = new UriRoom(uriFirstArg.room, "new\n room")
let res = null

res = await uriNew.fetchPutRoom()
test.assertEqual("inttest widget injected a 500", 500, res.status)

res = await uriNew.fetchPutRoom()
test.assertEqual("server mutex released and got 200", 200, res.status)

res = await uriNew.fetchPutRoom()
test.assertEqual("creating room twice throws error", 409, res.status)

let shouldThrow = new Controller({uri: uriMissing, maxPages: 10})
let threw = false
shouldThrow.onSocketError = function() {threw = true}
shouldThrow.onReadySocket = function() {}
setTimeout(function() {
    test.assertEqual("missing room returns error", true, threw)
}, 100)

function withController(uri, ret, callback, eavesdropper) {
    const wi = new Controller({uri, maxPages: 10, eavesdropper})

    wi.setInputValue = function() {}
    wi.setMoments = function(v) {
        ret.v = v
        for (let page of ret.v.pages) {
            for (let moment of page.moments) {
                moment.names = "(#)" + moment.names.length
                if (typeof(moment.time) === 'string') {
                    moment.time = "-"
                }
            }
        }
    }
    function close() { wi.close() }
    wi.onReadySocket = function(unlocked) {
        callback(unlocked, close)
    }
}

const expShutdownMsg = [
    {key: 0, time: "-", names: "(#)1", messages: [[
        {type: "event", body: "[room created]"},
        {type: "event", body: "[server shutting down]"},
        {type: "event", body: "[server started]"}
    ]]},
    {key: 1, time: "-", names: "(#)1", messages: [[
        {type: "event", body: "[connected]"}
    ]]}
]
const realShutdownMsg = {v: null}

const forEavesDropper = { i: 0 }
withController(uriRestarted, realShutdownMsg, function(_, close) {
    setTimeout(function() {
        close()
        for (let i = 0; i < expShutdownMsg.length; i++) {
            test.assertEqual("seeing shutdown, moment #" + i,
                             expShutdownMsg[i],
                             realShutdownMsg.v.pages[0].moments[i])
        }
    }, 100)
}, function(event) {
    const ed = forEavesDropper
    if (ed.i === 0) {
        test.assertEqual(
            "expected shutdown init event types",
            [
                "newPage",
                "newMoment",
                "create",
                "shutdown",
                "start"
            ],
            event.events.map(e => e.type)
        )
    }
    else if (ed.i === 1) {
        test.assertEqual("shutdown event #1", "newMoment", event.type)
    }
    else if (ed.i === 2) {
        test.assertEqual("shutdown event #2", "connect", event.type)
    }
    else {
        test.assertEqual("no excess events on shutdown", true, false)
    }
    ed.i += 1
})

const expTwoMoments = [
    {key: 0, time: "-", names: "(#)2", messages: [
        [{type: "event", body: "[room created]"}],
        [{type: "event", body: "[connected]"}]
    ]},
    {key: 1, time: "-", names: "(#)1", messages: [
        [{type: "write", body: "late"}]
    ]}
]
const realTwoMoments = []

for (let i = 0; i < 10; i++) {
    const uri = new UriRoom(uriFirstArg.room, "two-moments-" + i)
    await uri.fetchPutRoom()
    realTwoMoments.push({v: null})
    withController(uri, realTwoMoments[i], function(unlocked, close) {
        setTimeout(function() {unlocked.onInputChange("late")}, 280)
        setTimeout(function() {close()}, 500)
    })
}
setTimeout(function() {
    test.assertEqual(
        "one twoMoments", expTwoMoments,
        realTwoMoments[0].v.pages[0].moments)
    const t = new TestCase()
    for (let i = 0; i < 10; i++) {
        t.assertEqual('', expTwoMoments,
                      realTwoMoments[i].v.pages[0].moments)
    }
    test.assertEqual(
        "all twoMoments", 10, 10 - t.fails.length)
}, 500)

const expConnDis = [
    {key: 0, time: "-", names: "(#)3", messages: [
        [{type: "event", body: "[room created]"}],
        [{type: "event", body: "[connected]"},
         {type: "event", body: "[disconnected]"}],
        [{type: "event", body: "[connected]"}]
    ]}
]
const realConnDis = []

for (let i = 0; i < 10; i++) {
    const uri = new UriRoom(uriFirstArg.room, "conn-dis-" + i)
    await uri.fetchPutRoom()
    realConnDis.push({v: null})
    withController(uri, realConnDis[i], function(_, close) {
        setTimeout(close, 50)
    })
    setTimeout(function() {
        withController(uri, realConnDis[i], function(_, close) {
            setTimeout(close, 50)
        })
    }, 100)
}
setTimeout(function() {
    test.assertEqual(
        "one connDis", expConnDis, realConnDis[0].v.pages[0].moments)
    const t = new TestCase()
    for (let i = 0; i < 10; i++) {
        t.assertEqual('', expConnDis, realConnDis[i].v.pages[0].moments)
    }
    test.assertEqual(
        "all connDis", 10, 10 - t.fails.length)
}, 150)

setTimeout(function() {
    test.printResults()
    if (test.fails.length > 0) process.exit(1)
}, 500)
