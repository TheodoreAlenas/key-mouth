import Controller from './Controller.js'
import UriRoom from './io/UriRoom.js'
import uriFirstArg from './io/uriFirstArg.js'
import TestCase from './TestCase.js'

const test = new TestCase('integration test')
function wrapAssertEq(name, a, b) {
    test.wrap(function() {test.assertEqual(name, a, b)})
}

const uriRestarted = new UriRoom(uriFirstArg.room, "pre\nmade")
const uriMissing = new UriRoom(uriFirstArg.room, "doesn't exist")
const uriNew = new UriRoom(uriFirstArg.room, "new\n room")
let res = null

res = await uriNew.fetchPutRoom()
wrapAssertEq("inttest widget injected a 500", 500, res.status)

res = await uriNew.fetchPutRoom()
wrapAssertEq("server mutex released and got 200", 200, res.status)

res = await uriNew.fetchPutRoom()
wrapAssertEq("creating room twice throws error", 409, res.status)

let shouldThrow = new Controller({uri: uriMissing, maxPages: 10})
let threw = false
shouldThrow.onSocketError = function() {threw = true}
shouldThrow.onReadySocket = function() {}
setTimeout(function() {
    wrapAssertEq("missing room returns error", true, threw)
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
            wrapAssertEq("seeing shutdown, moment #" + i,
                             expShutdownMsg[i],
                             realShutdownMsg.v.pages[0].moments[i])
        }
    }, 200)
}, function(event) {
    const ed = forEavesDropper
    if (ed.i === 0) {
        wrapAssertEq(
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
        wrapAssertEq("shutdown event #1", "newMoment", event.type)
    }
    else if (ed.i === 2) {
        wrapAssertEq("shutdown event #2", "connect", event.type)
    }
    else {
        wrapAssertEq("no excess events on shutdown", true, false)
    }
    ed.i += 1
})

const expTwoMoments = [
    {key: 0, time: "-", names: "(#)1", messages: [
        [{type: "event", body: "[room created]"}]
    ]},
    {key: 1, time: "-", names: "(#)1", messages: [
        [{type: "event", body: "[connected]"},
         {type: "write", body: "late"},
         {type: "erase", body: "x"}]
    ]}
]
const n = 20
let twoMomentRes = ""
let twoMomentNooneReported = true

async function speakLate(i) {
    const real = {v: null}
    function onceGotController(unlocked, close) {
        setTimeout(function() {
            unlocked.onInputChange("latex")
            unlocked.onInputChange("late")
        }, 100)
        setTimeout(function() {
            close()
            const t = new TestCase()
            const eq = t.equal(expTwoMoments, real.v.pages[0].moments)
            twoMomentRes += eq ? '.' : 'F'
            if (twoMomentNooneReported && eq) {
                twoMomentNooneReported = false
                wrapAssertEq('2 moments', expTwoMoments,
                             real.v.pages[0].moments)
            }
        }, 200)
    }
    const uri = new UriRoom(uriFirstArg.room, 'two-moments-' + i)
    await uri.fetchPutRoom()
    setTimeout(function() {
        withController(uri, real, onceGotController)
    }, 500)
}
const promises = []
for (let i = 0; i < n; i++) {
    promises.push(speakLate(i))
}
Promise.all(promises)

setTimeout(function() {
    let hope = ""
    for (let i = 0; i < n; i++) hope += '.'
    wrapAssertEq("all twoMoment tests", hope, twoMomentRes)
    console.log(test.line)
    for (let e of test.fails) console.error(e)
    if (test.fails.length > 0) process.exit(1)
}, 1000)
