export default function assertEqual(message, a, b) {
    if (isEqual(a, b)) {
        console.log("Passed: " + message)
    }
    else {
        console.log("Failed: " + message)
        console.log(JSON.stringify(a))
        console.log(JSON.stringify(b))
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
}
