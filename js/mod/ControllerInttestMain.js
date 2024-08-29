import Controller from './Controller.js'
import UriRoom from './UriRoom.js'
import uriFirstArg from './uriFirstArg.js'
import TestCase from './TestCase.js'

const test = new TestCase()

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

let shouldThrow = new Controller(uriMissing)
let threw = 'no'
shouldThrow.onSocketError = function() {threw = 'yes'}
setTimeout(function() {
    test.assertEqual("missing room returns error", 'yes', threw)
}, 100)

function withController(uri, ret, callback) {
    const wi = new Controller(uri)

    wi.setInputValue = function() {}
    wi.setMoments = function(v) {
        ret.v = v
        for (let moment of ret.v) {
            moment.time = "-"
            moment.names = "(#)" + moment.names.length
        }
    }
    function close() { wi.close() }
    wi.onReadySocket = function(unlocked) {
        callback(unlocked, close)
    }
}

const expShutdownMsg = [
    {key: 0, time: "-", names: "(#)0", messages: []},
    {key: 1, time: "-", names: "(#)1", messages: [{message: [
        {type: "event", body: "[room created]"},
        {type: "event", body: "[server shutting down]"}
    ]}]},
    {key: 2, time: "-", names: "(#)1", messages: [{message: [
        {type: "event", body: "[server started]"}
    ]}]},
    {key: 3, time: "-", names: "(#)1", messages: [{message: [
        {type: "event", body: "[connected]"}
    ]}]}
]
const realShutdownMsg = {v: null}

withController(uriRestarted, realShutdownMsg, function(_, close) {
    setTimeout(function() {
        close()
        test.assertEqual(
            "seeing shutdown", expShutdownMsg, realShutdownMsg.v)
    }, 100)
})

const expOneMoment = [
    {key: 0, time: "-", names: "(#)0", messages: []},
    {key: 1, time: "-", names: "(#)2", messages: [
        {message: [{type: "event", body: "[room created]"}]},
        {message: [{type: "event", body: "[connected]"},
                   {type: "write", body: "too soon"}]}
    ]}
]
const realOneMoment = []

for (let i = 0; i < 10; i++) {
    const uri = new UriRoom(uriFirstArg.room, "one-moment-" + i)
    await uri.fetchPutRoom()
    realOneMoment.push({v: null})
    withController(uri, realOneMoment[i], function(unlocked, close) {
        setTimeout(function() {unlocked.onInputChange("too soon")}, 150)
        setTimeout(function() {close()}, 200)
    })
}
setTimeout(function() {
    test.assertEqual(
        "one oneMessage", expOneMoment, realOneMoment[0].v)
    const t = new TestCase()
    for (let i = 0; i < 10; i++) {
        t.assertEqual('', expOneMoment, realOneMoment[i].v)
    }
    test.assertEqual(
        "all oneMessage", 10, 10 - t.getFails())
}, 200)

const expTwoMoments = [
    {key: 0, time: "-", names: "(#)0", messages: []},
    {key: 1, time: "-", names: "(#)2", messages: [
        {message: [{type: "event", body: "[room created]"}]},
        {message: [{type: "event", body: "[connected]"}]}
    ]},
    {key: 2, time: "-", names: "(#)1", messages: [
        {message: [{type: "write", body: "late"}]}
    ]}
]
const realTwoMoments = []

for (let i = 0; i < 10; i++) {
    const uri = new UriRoom(uriFirstArg.room, "two-moments-" + i)
    await uri.fetchPutRoom()
    realTwoMoments.push({v: null})
    withController(uri, realTwoMoments[i], function(unlocked, close) {
        setTimeout(function() {unlocked.onInputChange("late")}, 220)
        setTimeout(function() {close()}, 300)
    })
}
setTimeout(function() {
    test.assertEqual(
        "one twoMoments", expTwoMoments, realTwoMoments[0].v)
    const t = new TestCase()
    for (let i = 0; i < 10; i++) {
        t.assertEqual('', expTwoMoments, realTwoMoments[i].v)
    }
    test.assertEqual(
        "all twoMoments", 10, 10 - t.getFails())
}, 300)

const expConnDis = [
    {key: 0, time: "-", names: "(#)0", messages: []},
    {key: 1, time: "-", names: "(#)3", messages: [
        {message: [{type: "event", body: "[room created]"}]},
        {message: [{type: "event", body: "[connected]"},
                   {type: "event", body: "[disconnected]"}]},
        {message: [{type: "event", body: "[connected]"}]}
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
        "one connDis", expConnDis, realConnDis[0].v)
    const t = new TestCase()
    for (let i = 0; i < 10; i++) {
        t.assertEqual('', expConnDis, realConnDis[i].v)
    }
    test.assertEqual(
        "all connDis", 10, 10 - t.getFails())
}, 150)

setTimeout(function() {
    test.printResults()
    if (test.getFails() > 0) process.exit(1)
}, 300)
