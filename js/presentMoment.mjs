
export default function presentMoment(names, diffs) {
    let conns = {}
    let order = []
    for (let i = 0; i < diffs.length; i++) {
        const diff = diffs[i]
        if (conns[diff.connId] === undefined) {
            conns[diff.connId] = {prevType: null, message: []}
            order.push(diff.connId)
        }
        const conn = conns[diff.connId]
        if (diff.type === "write" && conn.prevType === "write") {
            const m = conn.message
            m[m.length - 1].body += diff.body
        }
        else if (diff.type === "delete" && conn.prevType === "delete") {
            const m = conn.message
            const last = m[m.length - 1]
            last.body = diff.body + last.body
        }
        else {
            conn.message.push({
                type: diff.type,
                body: diff.body
            })
        }
        conn.prevType = diff.type
    }
    let result = []
    order.forEach(function(e) {result.push({
        name: names[e],
        message: conns[e].message
    })})
    return result
}
