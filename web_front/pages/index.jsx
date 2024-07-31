import sayHi from '../../a_feature/say_hi.mjs'
import { useEffect, useRef, useState } from "react"

export default function Home() {
    const [inputValue, setInputValue] = useState('')
    let [messages, setMessages] = useState(example)
    const socketRef = useRef(null)
    const preventDefClearInp = function(event) {
        event.preventDefault()
        setInputValue("")
        socketRef.current.send("clear")
    }
    const setInpSockSend = function(event) {
        const v = event.target.value
        setInputValue(v)
        socketRef.current.send("=" + v)
    }
    useEffect(function() {
        console.log("start")
        socketRef.current = new WebSocket("ws://localhost:8000")
        socketRef.current.addEventListener("open", function() {
            socketRef.current.send('{"version": 0}')
        })
        socketRef.current.addEventListener("message", function(event) {
            setMessages(JSON.parse(event.data))
            console.log(event.data)
        })
        return function() {
            console.log("end")
            socketRef.current.close()
        }
    }, [])
    return (
        <>
            <h1>{sayHi()}</h1>
            <ul>
                {
                    messages.map((m, i) =>
                        <li key={i}><ul>{m.map(postToLi)}</ul></li>)
                }
            </ul>
            <form onSubmit={preventDefClearInp}>
                <input
                    type="text"
                    value={inputValue}
                    onChange={setInpSockSend}
                />
                <button type="submit">Clear</button>
            </form>
        </>)
}

function postToLi(e, i) {
    return <li id={e.id} key={i}>
               <span key="name">{e.name}</span>
               {': '}
               {e.message.map(messageToSpan)}
           </li>
 }

function messageToSpan(m, i) {
    if (m.type === "wrote")
        return <span key={i}>{m.body}</span>
    if (m.type === "deleted")
        return <s key={i}>{m.body}</s>
    if (m.type === "old left")
        return <a href={m.ref} key={i}>{m.body}</a>
    if (m.type === "old right")
        return <a href={m.ref} key={i}>{m.body}</a>
}

const example = [
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
