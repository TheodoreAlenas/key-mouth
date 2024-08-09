
function getArg() {
    if (process.env.KEYMOUTH_DEPLOY === undefined) {
        const ui = ["http", "localhost:3000"]
        const api = ["http", "localhost:8000"]
        const ws = "ws://localhost:8000"
        return {home: [ui, api], room: [ws, api]}
    }
    const ui = [
        process.env.KEYMOUTH_UI_HTTP,
        process.env.KEYMOUTH_UI_PRE
    ]
    const api = [
        process.env.KEYMOUTH_API_HTTP,
        process.env.KEYMOUTH_API_PRE
    ]
    const ws = process.env.KEYMOUTH_WS
    return {home: [ui, api], room: [ws, api]}
}

const uriFirstArg = getArg()

export default uriFirstArg
