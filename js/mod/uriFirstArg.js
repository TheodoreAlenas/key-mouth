
function getArg() {
    if (process.env.KEYMOUTH_PROD === undefined) {
        return {
            home: ["http", "localhost", "3000"],
            room: ["http", "localhost", "8000"]
        }
    }
    const same = [
        process.env.KEYMOUTH_HTTP,
        process.env.KEYMOUTH_HOST,
        process.env.KEYMOUTH_PORT
    ]
    return {home: same, room: same}
}

const uriFirstArg = getArg()

export default uriFirstArg
