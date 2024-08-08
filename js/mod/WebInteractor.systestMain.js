import WebInteractor from './WebInteractor.js'

const roomUri = "http://localhost:8001/room?name=" +
      encodeURI("my\nroom")
const withRoom = fetch(roomUri, {method: "PUT"})
withRoom.catch(function(err) {
    console.error("Error, can't create room")
    throw err
})
const withNoError = withRoom.then(function() {
    fetch(roomUri, {method: "PUT"}).then(function(res) {
        if (res.status !== 409) {
            throw new Error("creating room twice, error code: " +
                            res.status)
        }
    })
})

function withWebInteractor(name, room, callback) {
    const wi = new WebInteractor(
        {
            webSocketUri: "ws://localhost:8001",
            lastMomentsUri: "http://localhost:8001/last",
            momentsRangeUri: "http://localhost:8001/moments"
        },
        room)

    function log(m) {
        console.log(Date.now() + "\t[" + name + "]\t" + m)
    }
    wi.setSetInputValue(function(m) {
        log("input value set to '" + m + "'")
    })
    wi.setSetOldMoments(function(m) {
        log("old moments set to " + JSON.stringify(m))
    })
    wi.setSetLastMoment(function(m) {
        log("last moment set to " + JSON.stringify(m))
    })
    const close = wi.getDestructor()
    wi.setOnReadySocket(function(unlocked) {
        callback(unlocked, close)
    })
}

withNoError.then(function() {
    withWebInteractor("say", "my\nroom", function(unlocked, close) {
        unlocked.onInputChange("hi")
        unlocked.onInputChange("hi there")
        unlocked.onClear()
        setTimeout(close, 200)
    })
    withWebInteractor("hear", "my\nroom", function(unlocked, close) {
        setTimeout(close, 200)
    })
    setTimeout(function() {
        withWebInteractor("stop", "my\nroom", function(unlocked, close) {
            unlocked.onInputChange("interrupt")
            setTimeout(close, 200)
        })
    }, 600)
    setTimeout(function() {
        withWebInteractor("all", "my\nroom", function(unlocked, close) {
            setTimeout(close, 200)
        })
    }, 800)
})
