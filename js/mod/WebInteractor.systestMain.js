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

const d = [0,0,0,0].map(x => ({inp: [], mom: [], all: []}))

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
    for (let person of d) {
        for (let snapshot of person.mom) {
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
    test.assertEqual(
        "speaker saw an empty moment, then 2",
        [
            [{key:'0', body:[], time: "erased times"}],
            [{key:'0', body:[], time: "erased times"},
             {key:'1', body:[]}]
        ],
        [d[0].mom[0], d[0].mom[1]]
    )
    test.assertEqual(
        "speaker finally saw the full text he wrote",
        [{
            "type": "write",
            "body": "hi there"
        }],
        d[0].mom[3][1].body[0].message
    )
    test.assertEqual(
        "speaker got same moments as listener",
        d[0].mom, d[1].mom
    )
    test.assertEqual(
        "interruptor joined and the first moment is empty as always",
        [[], []], [d[2].mom[0][0].body, d[2].mom[1][0].body]
    )
    test.assertEqual(
        "interruptor joined and found one moment",
        2, d[2].mom[1].length
    )
    test.assertEqual(
        "the speaker has 4 snapshots",
        4, d[0].mom.length
    )
    test.assertEqual(
        "after interruption the previous moment didn't change",
        d[2].mom[1][0],
        d[2].mom[2][0]
    )
    test.assertEqual(
        "interruptor interrupted and created a moment",
        d[2].mom[1].length + 1,
        d[2].mom[2].length
    )
    //console.log(JSON.stringify(d[3].mom, null, 2))
    test.assertEqual(
        "last visitor got the same as the last time",
        [
        [
            {
                "key": "0",
                "body": [],
                "time": "erased times"
            },
            {
                "key": "1",
                "body": [
                    {
                        "name": "erased names",
                        "message": [
                            {
                                "type": "write",
                                "body": "hi there"
                            },
                            {
                                "type": "event",
                                "body": "[disconnected]"
                            }
                        ]
                    },
                    {
                        "name": "erased names",
                        "message": [
                            {
                                "type": "event",
                                "body": "[disconnected]"
                            }
                        ]
                    }
                ],
                "time": "erased times"
            }
        ],
        [
            {
                "key": "0",
                "body": [],
                "time": "erased times"
            },
            {
                "key": "1",
                "body": [
                    {
                        "name": "erased names",
                        "message": [
                            {
                                "type": "write",
                                "body": "hi there"
                            },
                            {
                                "type": "event",
                                "body": "[disconnected]"
                            }
                        ]
                    },
                    {
                        "name": "erased names",
                        "message": [
                            {
                                "type": "event",
                                "body": "[disconnected]"
                            }
                        ]
                    }
                ],
                "time": "erased times"
            },
            {
                "key": "2",
                "body": [
                    {
                        "name": "erased names",
                        "message": [
                            {
                                "type": "write",
                                "body": "interrupt"
                            }
                        ]
                    }
                ]
            }
        ],
        [
            {
                "key": "0",
                "body": [],
                "time": "erased times"
            },
            {
                "key": "1",
                "body": [
                    {
                        "name": "erased names",
                        "message": [
                            {
                                "type": "write",
                                "body": "hi there"
                            },
                            {
                                "type": "event",
                                "body": "[disconnected]"
                            }
                        ]
                    },
                    {
                        "name": "erased names",
                        "message": [
                            {
                                "type": "event",
                                "body": "[disconnected]"
                            }
                        ]
                    }
                ],
                "time": "erased times"
            },
            {
                "key": "2",
                "body": [
                    {
                        "name": "erased names",
                        "message": [
                            {
                                "type": "write",
                                "body": "interrupt"
                            },
                            {
                                "type": "event",
                                "body": "[disconnected]"
                            }
                        ]
                    }
                ]
            }
        ]
    ],
        d[3].mom
    )
    test.printResults()
    if (test.getFails() !== 0) process.exit(1)
}
