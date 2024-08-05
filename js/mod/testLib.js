
export default class TestCase {
    line = ""
    fails = []
    assertEqual(message, a, b) {
        if (isEqual(a, b)) {
            this.line += '.'
        }
        else {
            this.line += 'F'
            this.fails.push({message, a, b})
        }
    }
    printResults() {
        console.log(this.line)
        this.fails.forEach(function(e) {
            console.log(JSON.stringify(e, null, 4))
        })
    }
}

function isEqual(a, b) {
    if (a === b) return true
    if (typeof(a) !== typeof(b)) return false
    const t = typeof(a)
    if (t === 'number' || t === 'string') return a === b
    if (t === 'object') {
        const missing = Object.keys(a).find(k => !isEqual(a[k], b[k]))
        return missing === undefined
    }
    throw new Error("unhandled type: " + t)
}
