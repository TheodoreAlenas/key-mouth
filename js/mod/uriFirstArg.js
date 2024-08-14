
function getArg() {
    const ui = process.env.KEYMOUTH_UI
    const api = process.env.KEYMOUTH_API
    const ws = process.env.KEYMOUTH_WS
    return {home: {ui, api}, room: {ws, api}}
}

const uriFirstArg = getArg()

export default uriFirstArg
