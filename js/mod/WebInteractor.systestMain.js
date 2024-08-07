import WebInteractor from './WebInteractor.js'

const roomUri = "http://localhost:8001/room?room=" +
      encodeURI("my\nroom")
const withRoom = fetch(roomUri, {method: "PUT"})
withRoom.catch(function(err) {
    console.error("Error, can't create room")
    throw err
})
const unreachable = withRoom.then(function() {
    fetch(roomUri, {method: "PUT"}).then(function(res) {
        if (res.status !== 409) {
            throw new Error("creating room twice, error code: " +
                            res.status)
        }
    })
})

unreachable.then(shit)

function shit() {
    const wi = new WebInteractor(
        {
            webSocketUri: "ws://localhost:8001",
            lastMomentsUri: "http://localhost:8001/last"
        },
        "my\nroom")

    function log(m) {console.log(Date.now() + "\t" + m)}
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
        unlocked.onInputChange("hi")
        unlocked.onInputChange("hi there")
        unlocked.onClear()
        setTimeout(close, 200)
    })
}
