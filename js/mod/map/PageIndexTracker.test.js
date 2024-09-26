
import PageIndexTracker from './PageIndexTracker.js'
import TestCase from '../TestCase.js'


const test = new TestCase('PageIndexTracker')

test.wrap(function() {
    const p = new PageIndexTracker({splitter: {
        pushEvent: function(e) {this.es.push(e)},
        es: []
    }})
    test.assertEqual("new, top", true, p.getTouchesTop())
    test.assertEqual("new, attached", false, p.getIsDetached())
    p.initPageIdx(0)
    test.assertEqual("initPageIdx(0), top", true, p.getTouchesTop())
    test.assertEqual("initPageIdx(0), attached", false, p.getIsDetached())
    p.pushEvent('a')
    test.assertEqual("pushEvent, top", true, p.getTouchesTop())
    test.assertEqual("pushEvent, attached", false, p.getIsDetached())
})

test.wrap(function() {
    const p = new PageIndexTracker({splitter: {
        pushEvent: function(e) {this.es.push(e)},
        es: []
    }})
    p.initPageIdx(1)
    test.assertEqual("initPageIdx(1), no top", false, p.getTouchesTop())
    test.assertEqual("initPageIdx(1), attached", false, p.getIsDetached())
    p.unshift('a')
    test.assertEqual("unshift, top", true, p.getTouchesTop())
    test.assertEqual("unshift, attached", false, p.getIsDetached())
    p.shift()
    test.assertEqual("shift, no top", false, p.getTouchesTop())
    test.assertEqual("shift, attached", false, p.getIsDetached())
})

test.wrap(function() {
    const p = new PageIndexTracker({splitter: {
        pushEvent: function(e) {this.es.push(e)},
        es: []
    }})
    p.initPageIdx(1)
    p.unshift('a')
    p.pop()
    test.assertEqual("pop, top", true, p.getTouchesTop())
    test.assertEqual("pop, detached", true, p.getIsDetached())
    p.push('a')
    test.assertEqual("push, top", true, p.getTouchesTop())
    test.assertEqual("push, attached", false, p.getIsDetached())
})

test.wrap(function() {
    const p = new PageIndexTracker({splitter: {
        pushEvent: function(e) {this.es.push(e)},
        es: []
    }})
    p.initPageIdx(2)
    p.unshift('a')
    p.unshift('b')
    test.assertEqual("unshift x2, top", true, p.getTouchesTop())
    test.assertEqual("unshift x2, attached", false, p.getIsDetached())
    p.pop()
    test.assertEqual("pop, top", true, p.getTouchesTop())
    test.assertEqual("pop, detached", true, p.getIsDetached())
    p.pop()
    test.assertEqual("pop x2, top", true, p.getTouchesTop())
    test.assertEqual("pop x2, detached", true, p.getIsDetached())
    p.push('b')
    test.assertEqual("push x1, top", true, p.getTouchesTop())
    test.assertEqual("push x1, detached", true, p.getIsDetached())
    p.push('a')
    test.assertEqual("push x2, top", true, p.getTouchesTop())
    test.assertEqual("push x2, attached", false, p.getIsDetached())
})

export default test
