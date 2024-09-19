
// License at the bottom

export default class TestCase {
    constructor(name) {
        this.line = name + ': '
        this.fails = []
    }
    assertEqual(name, a, b) {
        if (isSubset(a, b) && isSubset(b, a)) {
            this.line += '.'
        }
        else {
            this.line += 'F'
            this.fails.push({failed: name, a, b})
        }
    }
    printResults() {
        console.log(this.line + JSON.stringify(this.fails, null, 2))
    }
}

function isSubset(a, b) {
    if (typeof(a) !== 'object') return a === b
    if (typeof(b) !== 'object') return a === b
    return undefined === Object.keys(a).find(k => !isSubset(a[k], b[k]))
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
