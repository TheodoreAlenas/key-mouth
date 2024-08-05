import WebInteractor from './WebInteractor.js'

const wi = new WebInteractor(
    {
        webSocketUri: "ws://localhost:8001",
        lastMomentsUri: "http://localhost:8001/last"
    },
    "my\nsession")

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
