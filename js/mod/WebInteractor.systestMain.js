import WebInteractor from './WebInteractor.js'
import Uri from './Uri.js'

const uri = new Uri("systest", "my\nroom")
const withRoom = uri.fetchPutRoom()
withRoom.catch(function(err) {
    console.error("Error, can't create room")
    throw err
})
const withNoError = withRoom.then(function() {
    uri.fetchPutRoom().then(function(res) {
        if (res.status !== 409) {
            throw new Error("creating room twice, error code: " +
                            res.status)
        }
    })
})

function withWebInteractor(name, room, callback) {
    const wi = new WebInteractor(uri)

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
        setTimeout(function() {
            unlocked.onInputChange("hi")
            unlocked.onInputChange("hi there")
            unlocked.onClear()
        }, 50)
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
    }, 650)
})
