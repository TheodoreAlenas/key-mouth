import t1 from './accumulateDiffs.test.js'
import t2 from './PagePresenter.test.js'
import t3 from './PagesPresenter.test.js'

t1.printResults()
t2.printResults()
t3.printResults()
if (t1.fails.length !== 0) process.exit(1)
if (t2.fails.length !== 0) process.exit(1)
if (t3.fails.length !== 0) process.exit(1)
