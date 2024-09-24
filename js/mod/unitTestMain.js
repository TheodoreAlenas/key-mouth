import t1 from './map/accumulateDiffs.test.js'
import t2 from './map/PagesPresenter.test.js'

t1.printResults()
t2.printResults()
if (t1.fails.length !== 0) process.exit(1)
if (t2.fails.length !== 0) process.exit(1)
