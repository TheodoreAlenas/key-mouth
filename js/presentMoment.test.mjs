import presentMoment from './presentMoment.mjs'
import assertEqual from './testLib.mjs'

assertEqual(
    "None is none",
    [],
    presentMoment([], [], []))

assertEqual(
    "State but no diff, nothing in moment",
    [],
    presentMoment(["whatever"], [], []))

const names = {
    4: "Sotiris",
    5: "Mark"
}

assertEqual(
    "No state, one writing",
    [{name: "Sotiris", message: [{type: "write", body: "hello"}]}],
    presentMoment(
        [],
        names,
        [{connId: 4, type: "write", body: "hello"}]))

assertEqual(
    "No state, two writings",
    [{name: "Sotiris", message: [{type: "write", body: "hello"}]}],
    presentMoment(
        [],
        names,
        [{connId: 4, type: "write", body: "he"},
         {connId: 4, type: "write", body: "llo"}]))

const exampleState = [
    {connId: 4, inputFieldText: "hello", cutOn: 3},
    {connId: 5, inputFieldText: "I thought", cutOn: 0}
]

const exampleDiffs = [
    {connId: 4, time: 10.0, type: "delete", n: 2},
    {connId: 4, time: 11.0, type: "write", body: "p me"},
    {connId: 5, time: 11.5, type: "write", body: " something"}
]

const exampleAccumulation = [
    [
        {
            name: "Sotiris",
            message: [
                {type: "wrote", body: "Hi M"},
                {type: "deleted", body: "st"},
                {type: "wrote", body: "ark"},
            ]
        }
    ],
    [
        {
            name: "Sotiris",
            message: [
                {type: "wrote", body: "Are you there?"}
            ]
        },
        {
            name: "Mark",
            message: [
                {type: "event", body: "Joined"}
            ]
        },
        {
            name: "Mark",
            id: "edited-123",
            message: [
                {type: "wrote", body: "I thought I'd find you"}
            ]
        },
        {
            name: "Mark",
            message: [
                {type: "old left", body: "I ", ref: "#edited-123"},
                {type: "wrote", body: "knew"},
                {type: "old right", body: " I'd find you", ref: "#edited-123"},
            ]
        },
        {
            name: "Mark",
            message: [
                {type: "wrote", body: "in the park"},
            ]
        }
    ]
]
