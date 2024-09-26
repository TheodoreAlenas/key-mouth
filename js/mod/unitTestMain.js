import t1 from './map/accumulateDiffs.test.js'
import t2 from './map/PagesPresenter.test.js'
import t3 from './map/pagination.test.js'
import t4 from './map/PageIndexTracker.test.js'

const t = [t1, t2, t3, t4]
let line = ''
for (let ti of t) line += ti.line
console.log(line)
for (let ti of t) for (let e of ti.fails) console.error(e)
for (let ti of t) if (ti.fails.length !== 0) process.exit(1)
