
export default function presentMoment(names, diffs) {
    let conns = {}
    let order = []
    for (let i = 0; i < diffs.length; i++) {
        const d = diffs[i]
        if (conns[d.connId] === undefined) {
            conns[d.connId] = {prevType: null, result: []}
            order.push(d.connId)
        }
        if (d.type === conns[d.connId].prevType) {
            const r = conns[d.connId].result
            let m = r[r.length - 1].message
            m[m.length - 1].body += d.body
        }
        else {
            conns[d.connId].result.push({
                name: names[d.connId],
                message: [{
                    type: d.type,
                    body: d.body}]
            })
        }
        conns[d.connId].prevType = d.type
    }
    return order.reduce((a, e) => a.concat(conns[e].result), [])
}
