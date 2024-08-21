
export default class Io {
    constructor(uri, onReadySocket) {
        try {
            return this.constructorUnhandled(uri, onReadySocket)
        }
        catch (e) {
            console.error("Error constructing web io")
            throw e
        }
    }
    constructorUnhandled(uri, onReadySocket) {
        this.uri = uri
        this.socket = new WebSocket(uri.webSocket())
        onOpenSendVersionAnd(this.socket, onReadySocket, this)
    }
    close() {
        this.socket.close()
    }
    sendList(list) {
        const socket = this.socket
        for (let e of list) {
            try {socket.send(e)}
            catch (err) {
                console.error("Error sending '" + e +
                              "' of " + JSON.stringify(list))
                throw err
            }
        }
    }
    withMomentsRange(start, end, callback) {
        const u = this.uri.momentsRange(start, end)
        withJsonFetched(u, function(res) {
            try {
                callback(res)
            }
            catch (err) {
                console.error("Error on moment range callback, res = " +
                              JSON.stringify(res))
                throw err
            }
        })
    }
    onEvent(callback) {
        this.socket.addEventListener("message", function(event) {
            try {
                callback(JSON.parse(event.data))
            }
            catch (e) {
                console.error("Error JSON parsing " + event +
                              " or calling moments message callback")
                throw e
            }
        })
    }
}
function onOpenSendVersionAnd(socket, onReadySocket, io) {
    socket.addEventListener("open", function() {
        try {
            socket.send('{"version": 0}')
            onReadySocket(io)
        }
        catch (e) {
            console.error("Error sending version or unlocking input")
            throw e
        }
    })
}

function withJsonFetched(uri, callback) {
    const withStr = fetch(uri)
    withStr.catch(function(err) {
        console.error("Error, can't fetch " + uri)
        throw err
    })
    const withJson = withStr.then(function(res) {
        if (res.status !== 200) {
            throw new Error("Error, fetched " + uri +
                            " with status " + res.status)
        }
        return res.json()
    })
    withJson.then(callback)
    withJson.catch(function(err) {
        console.error("Error, res.json() failed, " + uri)
        throw err
    })
}
