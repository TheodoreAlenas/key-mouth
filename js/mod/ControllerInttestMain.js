import Controller from './Controller.js'
import UriRoom from './UriRoom.js'
import uriFirstArg from './uriFirstArg.js'
import TestCase from './TestCase.js'
import fs from 'fs'

const test = new TestCase()

const uri = new UriRoom(uriFirstArg.room, "my\nroom")
let res = null

res = await uri.fetchPutRoom()
test.assertEqual("inttest widget injected a 500", 500, res.status)

res = await uri.fetchPutRoom()
test.assertEqual("server mutex released and got 200", 200, res.status)

res = await uri.fetchPutRoom()
test.assertEqual("creating room twice throws error", 409, res.status)

function withController(buf, callback) {
    const wi = new Controller(uri)

    wi.setInputValue = function(m) {
        buf.inp.push(m)
    }
    wi.setMoments = function(m) {
        buf.snap.push(m)
    }
    function close() { wi.close() }
    wi.onReadySocket = function(unlocked) {
        callback(unlocked, close)
    }
}

const d = [0,0,0,0].map(_ => ({inp: [], snap: []}))

withController(d[0], function(unlocked, close) {
    setTimeout(function() {
        unlocked.onInputChange("hi")
        unlocked.onInputChange("hi there")
        unlocked.onClear()
    }, 50)
    setTimeout(close, 200)
})
setTimeout(function() {
    withController(d[1], function(unlocked, close) {
        setTimeout(close, 200)
    })
}, 20)
setTimeout(function() {
    withController(d[2], function(unlocked, close) {
        unlocked.onInputChange("interrupt")
        setTimeout(close, 200)
    })
}, 600)
setTimeout(function() {
    withController(d[3], function(unlocked, close) {
        setTimeout(close, 200)
    })
}, 650)

function getLastTimeResults() {
    const j = fs.readFileSync('js/mod/integr-golden-standard/exp.json')
    return JSON.parse(j)
}
function writeNewResults(r) {
    fs.writeFileSync(
        'js/mod/integr-golden-standard/real.gitig.json',
        JSON.stringify(r, null, 4))
}

setTimeout(check, 860)
function check() {
    eraseUnstableFields()
    const lastTimeResults = getLastTimeResults()
    const last = d[3].snap[d[3].snap.length - 1]
    writeNewResults(last)
    compareToGoldenStandard(lastTimeResults, last, test)
    test.printResults()
    if (test.getFails() !== 0) process.exit(1)
}

function eraseUnstableFields() {
    for (let person of d) {
        for (let snapshot of person.snap) {
            for (let moment of snapshot) {
                if (moment.time) {
                    moment.time = "erased times"
                }
                if (moment.body.length > 0) {
                    for (let person of moment.body) {
                        person.name = "erased names"
                    }
                }
            }
        }
    }
}

function compareToGoldenStandard(lastTimeResults, last, test) {
    for (let i = 0; i < last.length; i++) {
        test.assertEqual(
            `at least hasn't changed, moment ${i}`,
            lastTimeResults[i],
            last[i]
        )
    }
}
