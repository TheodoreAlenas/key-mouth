
export default class Io {
    constructor(args) {
        try {
            return this.constructorUnhandled(args)
        }
        catch (e) {
            console.error("Error constructing web io, args: " +
                          JSON.stringify(args))
            throw e
        }
    }
    constructorUnhandled({env, room, onReadySocket}) {
        ifRoomIsntStringThrowError(room)
        this.env = env
        this.room = room
        this.socket = new WebSocket(env.webSocketUri +
                                    "?room=" + encodeURI(room))
        onOpenSendVersionAnd(this.socket, onReadySocket, this)
    }
    getDestructor() {
        const socket = this.socket
        return function() {socket.close()}
    }
    sendList(list) {
        const socket = this.socket
        list.forEach(function(e) { trySending(socket, e, list) })
    }
    sendOne(e) {
        this.socket.send(e)
    }
    withLastMoments(callback) {
        const self = this
        const lastMomRoom = this.env.lastMomentsUri +
              "?room=" + encodeURI(this.room)
        withJsonFetched(lastMomRoom, function(res) {
            try {
                callback(res)
            }
            catch (err) {
                console.error("Error on last moments callback, res = " +
                              JSON.stringify(res))
                throw err
            }
        })
    }
    withMomentsRange(start, end, callback) {
        const rangeUri = this.env.momentsRangeUri +
              "?room=" + encodeURI(this.room) +
              "&start=" + start +
              "&end=" + end
        withJsonFetched(rangeUri, function(res) {
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
    onMomentsMessage(callback) {
        const self = this
        this.socket.addEventListener("message", function(event) {
            try {
                const {n, last} = JSON.parse(event.data)
                callback(n, last)
            }
            catch (e) {
                console.error("Error JSON parsing " +
                              event.data +
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

function ifRoomIsntStringThrowError(room) {
    if (typeof(room) !== 'string') {
        throw new Error(
            "room isn't string (.../?room=hello let's say), " +
                "typeof(room) = " + typeof(room) +
                ", room = " + room)
    }
}

function trySending(socket, e, list) {
    try {
        socket.send(e)
    }
    catch (err) {
        console.error("Error sending " + JSON.stringify(list) +
                      ", maybe set input before init")
        throw err
    }
}
