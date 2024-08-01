
export default function presentMoment(_, names, diffs) {
    let result = []
    let prev = "nothing"
    for (let i = 0; i < diffs.length; i++) {
        const d = diffs[i]
        if (d.type === prev) {
            let m = result[result.length - 1].message
            m[m.length - 1].body += d.body
        }
        else {
            result.push({name: names[d.connId], message: [{
                type: "write", body: d.body
            }]})
        }
        prev = d.type
    }
    return result
}
