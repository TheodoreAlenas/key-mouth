
const ui = process.env.KEYMOUTH_UI
const api = process.env.KEYMOUTH_API
const ws = process.env.KEYMOUTH_WS

const uriFirstArg = {home: {ui, api}, room: {ws, api}}

export default uriFirstArg
