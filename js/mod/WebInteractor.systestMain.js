import WebInteractor from './WebInteractor.js'
import UriRoom from './UriRoom.js'
import uriFirstArg from './uriFirstArg.js'
import TestCase from './TestCase.js'

const uri = new UriRoom(uriFirstArg.room, "my\nroom")
const withRoom = uri.fetchPutRoom()
const withNoError = withRoom.then(function(res) {
    if (res.status !== 200) {
        throw new Error("creating room failed with error code: " +
                        res.status)
    }
    uri.fetchPutRoom().then(function(res) {
        if (res.status !== 409) {
            throw new Error("creating room twice, error code: " +
                            res.status)
        }
    })
})

function withWebInteractor(buf, room, callback) {
    const wi = new WebInteractor(uri)

    wi.setSetInputValue(function(m) {
        buf.all.push({t: "inp", i: buf.inp.length})
        buf.inp.push(m)
    })
    wi.setSetMoments(function(m) {
        buf.all.push({t: "mom", i: buf.mom.length})
        buf.mom.push(m)
    })
    const close = wi.getDestructor()
    wi.setOnReadySocket(function(unlocked) {
        callback(unlocked, close)
    })
}

const conns = ["say", "hear", "stop", "all"]
const d = conns.map(x => ({conn: x, inp: [], mom: [], all: []}))

withNoError.then(function() {
    withWebInteractor(d[0], "my\nroom", function(unlocked, close) {
        setTimeout(function() {
            unlocked.onInputChange("hi")
            unlocked.onInputChange("hi there")
            unlocked.onClear()
        }, 50)
        setTimeout(close, 200)
    })
    withWebInteractor(d[1], "my\nroom", function(unlocked, close) {
        setTimeout(close, 200)
    })
    setTimeout(function() {
        withWebInteractor(d[2], "my\nroom", function(unlocked, close) {
            unlocked.onInputChange("interrupt")
            setTimeout(close, 200)
        })
    }, 600)
    setTimeout(function() {
        withWebInteractor(d[3], "my\nroom", function(unlocked, close) {
            setTimeout(close, 200)
        })
    }, 650)
})

setTimeout(check, 860)

function check() {
    const test = new TestCase()
    test.assertEqual(
        "speaker got same moments as listener",
        d[0].mom, d[1].mom
    )
    test.printResults()
}
