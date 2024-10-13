export default class IoHome {
    constructor({uri}) {
        this.uri = uri
    }
    withRooms(callback) {
        const uri = this.uri
        withJsonFetched(uri.rooms(), function(json) {
            const massaged = json.map(e => ({
                text: e.name || '<unnamed>',
                href: uri.room(e.id)
            }))
            callback(massaged)
        })
    }
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
