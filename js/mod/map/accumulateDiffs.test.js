import accumulateDiffs from './accumulateDiffs.js'
import TestCase from '../TestCase.js'

const test = new TestCase('accumulateDiffs')

function wrapAndAssertEqual(name, a, b) {
    test.wrap(function() { test.assertEqual(name, a, b) })
}

wrapAndAssertEqual(
    "none is none",
    [],
    accumulateDiffs([]))

wrapAndAssertEqual(
    "one writing",
    [{connId: 4, message: [{type: "write", body: "hello"}]}],
    accumulateDiffs(
        [{connId: 4, type: "write", body: "hello"}]))

wrapAndAssertEqual(
    "one deletion",
    [{connId: 4, message: [{type: "delete", body: "hello"}]}],
    accumulateDiffs(
        [{connId: 4, type: "delete", body: "hello"}]))

wrapAndAssertEqual(
    "two writings",
    [{connId: 4, message: [{type: "write", body: "hello"}]}],
    accumulateDiffs(
        [{connId: 4, type: "write", body: "he"},
         {connId: 4, type: "write", body: "llo"}]))

wrapAndAssertEqual(
    "two deletions",
    [{connId: 4, message: [{type: "delete", body: "hello"}]}],
    accumulateDiffs(
        [{connId: 4, type: "delete", body: "llo"},
         {connId: 4, type: "delete", body: "he"}]))

wrapAndAssertEqual(
    "write 2 delete 1",
    [{connId: 4, message: [{type: "write", body: "h"},
                                 {type: "erase", body: "e"}]}],
    accumulateDiffs(
        [{connId: 4, type: "write", body: "he"},
         {connId: 4, type: "delete", body: "e"}]))

wrapAndAssertEqual(
    "write 1 delete 1",
    [{connId: 4, message: [{type: "erase", body: "h"}]}],
    accumulateDiffs(
        [{connId: 4, type: "write", body: "h"},
         {connId: 4, type: "delete", body: "h"}]))

wrapAndAssertEqual(
    "write 2 delete 1 delete 1",
    [{connId: 4, message: [{type: "erase", body: "he"}]}],
    accumulateDiffs(
        [{connId: 4, type: "write", body: "he"},
         {connId: 4, type: "delete", body: "e"},
         {connId: 4, type: "delete", body: "h"}]))

wrapAndAssertEqual(
    "write 1 delete 1 delete 1",
    [{connId: 4, message: [{type: "delete", body: "h"},
                                 {type: "erase", body: "e"}]}],
    accumulateDiffs(
        [{connId: 4, type: "write", body: "e"},
         {connId: 4, type: "delete", body: "e"},
         {connId: 4, type: "delete", body: "h"}]))

wrapAndAssertEqual(
    "write 2 delete 1 delete 1 delete 1",
    [{connId: 4, message: [{type: "delete", body: "he"},
                                 {type: "erase", body: "llo"}]}],
    accumulateDiffs(
        [{connId: 4, type: "write", body: "llo"},
         {connId: 4, type: "delete", body: "llo"},
         {connId: 4, type: "delete", body: "e"},
         {connId: 4, type: "delete", body: "h"}]))

wrapAndAssertEqual(
    "write 1 delete 1 write 1 delete 1",
    [{connId: 4, message: [{type: "erase", body: "he"},
                                 {type: "erase", body: "llo"}]}],
    accumulateDiffs(
        [{connId: 4, type: "write", body: "he"},
         {connId: 4, type: "delete", body: "he"},
         {connId: 4, type: "write", body: "llo"},
         {connId: 4, type: "delete", body: "llo"}]))

wrapAndAssertEqual(
    "write 2 delete 1 delete 1 delete 1 odd event",
    [{connId: 4, message: [
        {type: "delete", body: "he"},
        {type: "erase", body: "llo"},
        {type: "event", body: "arbitrary event"}]}],
    accumulateDiffs(
        [{connId: 4, type: "write", body: "llo"},
         {connId: 4, type: "delete", body: "llo"},
         {connId: 4, type: "delete", body: "e"},
         {connId: 4, type: "delete", body: "h"},
         {connId: 4, type: "event", body: "arbitrary event"}
        ]))


wrapAndAssertEqual(
    "a writes, b writes",
    [{connId: 4, message: [{type: "write", body: "hi"}]},
     {connId: 5, message: [{type: "write", body: "HELLO"}]}],
    accumulateDiffs(
        [{connId: 4, type: "write", body: "hi"},
         {connId: 5, type: "write", body: "HELLO"}]))

wrapAndAssertEqual(
    "a writes, b writes, a writes",
    [{connId: 4, message: [{type: "write", body: "hi"}]},
     {connId: 5, message: [{type: "write", body: "HELLO"}]}],
    accumulateDiffs(
        [{connId: 4, type: "write", body: "h"},
         {connId: 5, type: "write", body: "HELLO"},
         {connId: 4, type: "write", body: "i"}]))

export default test
