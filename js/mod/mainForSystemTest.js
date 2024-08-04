import initSocketReturnTeardown from './socket.js'

function run() {
    const close = initSocketReturnTeardown(
        {env, setInputValue, setOldMoments, setLastMoment},
        function(unlocked) {
            unlocked.onInputChange("hi")
            unlocked.onInputChange("hi there")
            unlocked.onClear()
            setTimeout(close, 200)
        })
}

const env = {
    webSocketUri: "ws://localhost:8001",
    lastMomentsUri: "http://localhost:8001/last"
}

function log(m) {
    console.log(Date.now() + "\t" + m)
}
function setInputValue(newValue) {
    log("input value set to '" + newValue + "'")
}
function setOldMoments(m) {
    log("old moments set to " + JSON.stringify(m))
}
function setLastMoment(m) {
    log("last moment set to " + JSON.stringify(m))
}

run()
