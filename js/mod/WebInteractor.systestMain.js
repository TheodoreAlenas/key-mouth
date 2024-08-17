import WebInteractor from './WebInteractor.js'
import UriRoom from './UriRoom.js'
import uriFirstArg from './uriFirstArg.js'
import TestCase from './TestCase.js'
import fs from 'fs'

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
        buf.inp.push(m)
    })
    wi.setSetMoments(function(m) {
        buf.snap.push(m)
    })
    const close = wi.getDestructor()
    wi.setOnReadySocket(function(unlocked) {
        callback(unlocked, close)
    })
}

const d = [0,0,0,0].map(_ => ({inp: [], snap: []}))

withNoError.then(function() {
    withWebInteractor(d[0], "my\nroom", function(unlocked, close) {
        setTimeout(function() {
            unlocked.onInputChange("hi")
            unlocked.onInputChange("hi there")
            unlocked.onClear()
        }, 50)
        setTimeout(close, 200)
    })
    setTimeout(function() {
        withWebInteractor(d[1], "my\nroom", function(unlocked, close) {
            setTimeout(close, 200)
        })
    }, 20)
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

const json = fs.readFileSync(
    'git-ignores/systest-golden-standard-expected.json')
const lastTimeResults = JSON.parse(json)
function writeNewResults(r) {
    fs.writeFileSync(
        'git-ignores/systest-golden-standard-real.json',
        JSON.stringify(r, null, 4))
}

function check() {
    const test = new TestCase()
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
    const last = d[3].snap
    writeNewResults(last)
    for (let i = 0; i < last.length; i++) {
        for (let j = 0; j < last[i].length; j++) {
            test.assertEqual(
                `at least hasn't changed, snapshot ${i}, moment ${j}`,
                lastTimeResults[i][j],
                last[i][j]
            )
        }
    }
    test.printResults()
    if (test.getFails() !== 0) process.exit(1)
}
