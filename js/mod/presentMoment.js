
// License at the bottom

export default function presentMoment(getNames, diffs) {
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
        else if (diff.type === "write") {
            conn.message.push({
                type: "write",
                body: diff.body
            })
        }
        else if (diff.type === "delete") {
            const m = conn.message
            if (m.length === 0) {
                m.push({
                    type: "delete",
                    body: diff.body
                })
            }
            else if (m[m.length - 1].type == "delete") {
                m[m.length - 1].body = diff.body + m[m.length - 1].body
            }
            else {
                let toPushInTheEnd = null
                if (m[m.length - 1].type == "erase") {
                    toPushInTheEnd = m.pop()
                }
                const last = m[m.length - 1]
                if (last.type == "write" &&
                    last.body.endsWith(diff.body)) {

                    const end = last.body.length - diff.body.length
                    if (end > 0) last.body = last.body.substr(0, end)
                    else conn.message.pop()
                }
                if (toPushInTheEnd === null) {
                    conn.message.push({
                        type: "erase",
                        body: diff.body
                    })
                }
                else {
                    toPushInTheEnd.body = diff.body + toPushInTheEnd.body;
                    m.push(toPushInTheEnd)
                }
            }
        }
        conn.prevType = diff.type
    }
    let result = []
    order.forEach(function(e) {result.push({
        name: getNames(e),
        message: conns[e].message
    })})
    return result
}

/*
Copyright 2024 <dimakopt732@gmail.com>

Permission is hereby granted, free of charge, to any person obtaining a
copy of this software and associated documentation files
(the “Software”), to deal in the Software without restriction,
including without limitation the rights to use, copy, modify, merge,
publish, distribute, sublicense, and/or sell copies of the Software,
and to permit persons to whom the Software is furnished to do so,
subject to the following conditions:

The above copyright notice and this permission notice shall be included
in all copies or substantial portions of the Software.

THE SOFTWARE IS PROVIDED “AS IS”, WITHOUT WARRANTY OF ANY KIND,
EXPRESS OR IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF
MERCHANTABILITY, FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT.
IN NO EVENT SHALL THE AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR
ANY CLAIM, DAMAGES OR OTHER LIABILITY, WHETHER IN AN ACTION OF CONTRACT,
TORT OR OTHERWISE, ARISING FROM, OUT OF OR IN CONNECTION WITH THE
SOFTWARE OR THE USE OR OTHER DEALINGS IN THE SOFTWARE.
*/
