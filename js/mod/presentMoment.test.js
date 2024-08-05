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
    "one writing",
    [{name: "Sotiris", message: [{type: "write", body: "hello"}]}],
    presentMoment(
        getNames,
        [{connId: 4, type: "write", body: "hello"}]))

test.assertEqual(
    "two writings",
    [{name: "Sotiris", message: [{type: "write", body: "hello"}]}],
    presentMoment(
        getNames,
        [{connId: 4, type: "write", body: "he"},
         {connId: 4, type: "write", body: "llo"}]))

test.assertEqual(
    "two deletes",
    [{name: "Sotiris", message: [{type: "delete", body: "hello"}]}],
    presentMoment(
        getNames,
        [{connId: 4, type: "delete", body: "llo"},
         {connId: 4, type: "delete", body: "he"}]))

test.assertEqual(
    "write delete",
    [{name: "Sotiris", message: [{type: "write", body: "he"},
                                 {type: "delete", body: "he"}]}],
    presentMoment(
        getNames,
        [{connId: 4, type: "write", body: "he"},
         {connId: 4, type: "delete", body: "he"}]))

test.assertEqual(
    "a writes, b writes",
    [{name: "Sotiris", message: [{type: "write", body: "hi"}]},
     {name: "Mark", message: [{type: "write", body: "HELLO"}]}],
    presentMoment(
        getNames,
        [{connId: 4, type: "write", body: "hi"},
         {connId: 5, type: "write", body: "HELLO"}]))

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
