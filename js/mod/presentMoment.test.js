import presentMoment from './presentMoment.js'
import TestCase from './TestCase.js'

const test = new TestCase()

test.assertEqual(
    "none is none",
    [],
    presentMoment([], []))

function getNames(conn) {
    if (conn === 4) return "Sotiris"
    if (conn === 5) return "Mark"
    return "...But there's only conn 4 and conn 5"
}

test.assertEqual(
    "write 2 delete 1 delete 1 delete 1 disconnect",
    [{name: "Sotiris", message: [
        {type: "delete", body: "he"},
        {type: "erase", body: "llo"},
        {type: "event", body: "[disconnected]"}]}],
    presentMoment(
        getNames,
        [{connId: 4, type: "write", body: "llo"},
         {connId: 4, type: "delete", body: "llo"},
         {connId: 4, type: "delete", body: "e"},
         {connId: 4, type: "delete", body: "h"},
         {connId: 4, type: "disconnect", body: null}
        ]))


test.assertEqual(
    "a writes, b writes, a writes",
    [{name: "Sotiris", message: [{type: "write", body: "hi"}]},
     {name: "Mark", message: [{type: "write", body: "HELLO"}]}],
    presentMoment(
        getNames,
        [{connId: 4, type: "write", body: "h"},
         {connId: 5, type: "write", body: "HELLO"},
         {connId: 4, type: "write", body: "i"}]))

test.printResults()
if (test.getFails() !== 0) process.exit(1)
