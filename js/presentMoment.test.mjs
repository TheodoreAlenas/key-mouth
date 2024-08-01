import presentMoment from './presentMoment.mjs'
import assertEqual from './testLib.mjs'

assertEqual(
    "none is none",
    [],
    presentMoment([], []))

const names = {
    4: "Sotiris",
    5: "Mark"
}

assertEqual(
    "one writing",
    [{name: "Sotiris", message: [{type: "write", body: "hello"}]}],
    presentMoment(
        names,
        [{connId: 4, type: "write", body: "hello"}]))

assertEqual(
    "two writings",
    [{name: "Sotiris", message: [{type: "write", body: "hello"}]}],
    presentMoment(
        names,
        [{connId: 4, type: "write", body: "he"},
         {connId: 4, type: "write", body: "llo"}]))

assertEqual(
    "write delete",
    [{name: "Sotiris", message: [{type: "write", body: "he"},
                                 {type: "delete", body: "he"}]}],
    presentMoment(
        names,
        [{connId: 4, type: "write", body: "he"},
         {connId: 4, type: "delete", body: "he"}]))

assertEqual(
    "one deletion",
    [{name: "Sotiris", message: [{type: "delete", body: "hello"}]}],
    presentMoment(
        names,
        [{connId: 4, type: "delete", body: "hello"}]))

assertEqual(
    "a writes, b writes",
    [{name: "Sotiris", message: [{type: "write", body: "hi"}]},
     {name: "Mark", message: [{type: "write", body: "HELLO"}]}],
    presentMoment(
        names,
        [{connId: 4, type: "write", body: "hi"},
         {connId: 5, type: "write", body: "HELLO"}]))

assertEqual(
    "a writes, b writes, a writes",
    [{name: "Sotiris", message: [{type: "write", body: "hi"}]},
     {name: "Mark", message: [{type: "write", body: "HELLO"}]}],
    presentMoment(
        names,
        [{connId: 4, type: "write", body: "h"},
         {connId: 5, type: "write", body: "HELLO"},
         {connId: 4, type: "write", body: "i"}]))
