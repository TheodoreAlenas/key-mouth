
export default class Io {
    constructor(args) {
        try {
            return this._constructor(args)
        }
        catch (e) {
            console.error("Error constructing web io, args:")
            console.error(args)
            throw e
        }
    }
    _constructor({uri, onReadySocket, onSocketError}) {
        this.uri = uri
        this.socket = new WebSocket(uri.webSocket())
        this.socket.addEventListener('error', onSocketError)
        this.socketQueue = Promise.resolve()
        onOpenSendVersionAnd(this.socket, onReadySocket, this)
    }
    _enqueue(f) {
        this.socketQueue = this.socketQueue.then(f)
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
        const self = this
        this.socket.addEventListener("message", function(event) {
            self._enqueue(function() {
                try {
                    callback(JSON.parse(event.data))
                }
                catch (e) {
                    console.error(
                        "Error JSON parsing " + event +
                            " or calling moments message callback " +
                            "with arg " + event.data)
                    console.error(e)
                }
            })
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
