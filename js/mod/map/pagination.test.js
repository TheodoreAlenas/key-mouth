import PagesPresenter from './PagesPresenter.js'
import TestCase from '../TestCase.js'

const test = new TestCase('pagination')

function newPP(n) {
    return new PagesPresenter({
        maxPages: n,
        viewModelMapper: {mapPages: x => ({mapped: x})},
        splitter: {
            lastPage: null,
            pushEvent: function(e) {
                if (e === 'new page') {
                    const p = this.lastPage
                    this.lastPage = []
                    return p
                }
                this.lastPage.push(e)
            }
        }
    })
}

test.wrap(function() {
    let threw = "didn't actually throw"
    try {newPP(0)}
    catch (_) {threw = "threw"}
    test.assertEqual("maxPages 0 throws error", "threw", threw)

    threw = "didn't actually throw"
    try {newPP(1)}
    catch (_) {threw = "threw"}
    test.assertEqual("maxPages 1 throws error", "threw", threw)
})

test.wrap(function() {
    const pp = newPP(100)
    let v = pp.getViewModel()
    test.assertEqual("no events, returns empty view", {mapped: []}, v)

    pp.pushEvent({firstPageIdx: 0, events: []})
    v = pp.getViewModel()
    test.assertEqual("first batch emtpy, returns empty view",
                     {mapped: []}, v)
    test.assertEqual("there's no undefined or anything either",
                     0, v.mapped.length)
})

test.wrap(function() {
    const pp = newPP(2)
    pp.pushEvent({
        firstPageIdx: 0,
        events: ['new page', 'a']
    })
    const v = pp.getViewModel()
    test.assertEqual("1 in first batch", {mapped: [['a']]}, v)
})

test.wrap(function() {
    const pp = newPP(2)
    pp.pushEvent({
        firstPageIdx: 0,
        events: ['new page', 'a', 'b', 'c']
    })
    const v = pp.getViewModel()
    test.assertEqual("1 with many moments in first batch",
                     {mapped: [['a', 'b', 'c']]}, v)
})

test.wrap(function() {
    const pp = newPP(2)
    pp.pushEvent({
        firstPageIdx: 0,
        events: ['new page', 'a', 'new page', 'b']
    })
    const v = pp.getViewModel()
    test.assertEqual("max in first batch",
                     {mapped: [['a'], ['b']]}, v)
})

test.wrap(function() {
    const pp = newPP(2)
    pp.pushEvent({
        firstPageIdx: 0,
        events: ['new page', 'a', 'new page', 'b', 'new page', 'c']
    })
    const v = pp.getViewModel()
    test.assertEqual("beyond max in first batch",
                     {mapped: [['b'], ['c']]}, v)
})

test.wrap(function() {
    const pp = newPP(2)
    pp.pushEvent({firstPageIdx: 0, events: ['new page', 'a']})
    pp.pushEvent('new page')
    pp.pushEvent('b')
    const v = pp.getViewModel()
    test.assertEqual("max pages, one was after the first batch",
                     {mapped: [['a'], ['b']]}, v)
})

test.wrap(function() {
    const pp = newPP(2)
    pp.pushEvent({firstPageIdx: 0, events: ['new page', 'a']})
    pp.pushEvent('new page')
    pp.pushEvent('b')
    pp.pushEvent('new page')
    pp.pushEvent('c')
    const v = pp.getViewModel()
    test.assertEqual("beyond max pages. Not just first batch",
                     {mapped: [['b'], ['c']]}, v)
})

test.wrap(function() {
    const pp = newPP(2)
    test.assertEqual("no events, touches top", true, pp.getTouchesTop())
})

test.wrap(function() {
    const pp = newPP(2)
    pp.pushEvent({firstPageIdx: 0, events: ['new page', 'a']})
    test.assertEqual("1 page, touches top", true, pp.getTouchesTop())
})

test.wrap(function() {
    const pp = newPP(2)
    pp.pushEvent({firstPageIdx: 0, events:
                  ['new page', 'a', 'new page', 'b']})
    test.assertEqual("max pages, touches top", true, pp.getTouchesTop())
})

test.wrap(function() {
    const pp = newPP(2)
    pp.pushEvent({firstPageIdx: 0, events:
                  ['new page', 'a', 'new page', 'b', 'new page', 'c']})
    test.assertEqual("beyond max pages, doesn't touch top",
                     false, pp.getTouchesTop())
})

test.wrap(function() {
    const pp = newPP(2)
    pp.pushEvent({firstPageIdx: 1, events: ['new page', 'a']})
    test.assertEqual("starting from page 1, doesn't touch top",
                     false, pp.getTouchesTop())
})

test.wrap(function() {
    const pp = newPP(3)
    pp.pushEvent({firstPageIdx: 1, events: ['new page', 'a']})
    pp.prependPage(['prepen', 'ded'])
    const v = pp.getViewModel()
    test.assertEqual("prepend one",
                     {mapped: [['prepen', 'ded'], ['a']]}, v)
})

test.wrap(function() {
    const pp = newPP(3)
    pp.pushEvent({
        firstPageIdx: 1,
        events: ['new page', 'a', 'new page', 'b']
    })
    pp.prependPage(['prepen', 'ded'])
    const v = pp.getViewModel()
    test.assertEqual("prepend one on max pages",
                     {mapped: [['prepen', 'ded'], ['a'], ['b']]}, v)
})

test.wrap(function() {
    const pp = newPP(3)
    pp.pushEvent({
        firstPageIdx: 1,
        events: ['new page', 'a']
    })
    pp.prependPage(['prepen', 'ded'])
    pp.prependPage(['newer'])
    const v = pp.getViewModel()
    test.assertEqual("prepend twice on a page",
                     {mapped: [['newer'], ['prepen', 'ded'], ['a']]}, v)
})

test.wrap(function() {
    const pp = newPP(3)
    pp.pushEvent({
        firstPageIdx: 1,
        events: ['new page', 'a', 'new page', 'b']
    })
    pp.prependPage(['prepen', 'ded'])
    pp.prependPage(['newer'])
    const v = pp.getViewModel()
    test.assertEqual("prepend twice on max (prepend on detached)",
                     {mapped: [['newer'], ['prepen', 'ded']]}, v)
})

test.wrap(function() {
    const pp = newPP(3)
    pp.pushEvent({
        firstPageIdx: 1,
        events: ['new page', 'a', 'new page', 'b']
    })
    pp.prependPage(['p1'])
    pp.prependPage(['p2'])
    pp.prependPage(['p3'])
    test.assertEqual("just a check",
                     {mapped: [['p3'], ['p2']]},
                     pp.getViewModel())
    pp.appendPage(['a1'])
    test.assertEqual("append well after detached",
                     {mapped: [['p2'], ['a1']]},
                     pp.getViewModel())
    pp.appendPage(['a2'])
    test.assertEqual("append again and reattach",
                     {mapped: [['a1'], ['a2'], ['b']]},
                     pp.getViewModel())
})

export default test
