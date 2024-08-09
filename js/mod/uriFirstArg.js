
function getArg() {
    if (process.env.KEYMOUTH_PROD === undefined) {
        const ui = ["http", "localhost", "3000"]
        const api = ["http", "localhost", "8000"]
        return {
            home: [ui, api],
            room: api
        }
    }
    const same = [
        process.env.KEYMOUTH_HTTP,
        process.env.KEYMOUTH_HOST,
        process.env.KEYMOUTH_PORT
    ]
    return {home: [same, same], room: same}
}

const uriFirstArg = getArg()

export default uriFirstArg
