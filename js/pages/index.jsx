import presentMoment from '../presentMoment.mjs'
import { useEffect, useRef, useState } from "react"

function getDiff(a, b) {
    if (a.startsWith(b)) {
        return ["-", a.substr(b.length)]
    }
    if (b.startsWith(a)) {
        return ["+", b.substr(a.length)]
    }
    for (let i = 0; i < a.length && i < b.length; i++) {
        if (a[i] !== b[i]) {
            return [":", a.substr(i), b.substr(i)]
        }
    }
    throw Exception("can't handle diff, a: " + a + ", b: " + b)
}

function setUpSocket(socket, setMessages, setLatest) {
    const connNames = {4: "Sotiris", 5: "Vaggas"}
    fetch("http://localhost:8000/last")
        .then(res => res.json())
        .then(function(res) {
            const p = res.map(r => presentMoment(connNames, r))
            setMessages(p)
        })
    socket.addEventListener("open", function() {
        socket.send('{"version": 0}')
    })
    socket.addEventListener("message", function(event) {
        console.log(event.data)
        const diffs = JSON.parse(event.data)
        const p = [presentMoment(connNames, diffs)]
        setLatest(p)
    })
    return function() {
        socket.close()
    }
}

export default function Home() {
    const [inputValue, setInputValue] = useState('')
    const [messages, setMessages] = useState([])
    const [latest, setLatest] = useState([])
    const socketRef = useRef(null)
    const preventDefClearInp = function(event) {
        event.preventDefault()
        setInputValue("")
        socketRef.current.send("clear")
    }
    const setInpSockSend = function(event) {
        const newValue = event.target.value
        if (newValue === inputValue) return
        const d = getDiff(inputValue, newValue)
        setInputValue(newValue)
        d.forEach(function(e) {socketRef.current.send(e)})
    }
    useEffect(function() {
        socketRef.current = new WebSocket("ws://localhost:8000")
        return setUpSocket(socketRef.current, setMessages, setLatest)
    }, [])
    return (
        <>
            <ul>{messages.concat(latest).map(messageToInnerUl)}</ul>
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

function messageToInnerUl(m, i) {
    return <li key={i}><ul>{m.map(postToLi)}</ul></li>
}

function postToLi(e, i) {
    return <li id={e.id} key={i}>
               <span key="name">{e.name}</span>
               {': '}
               {e.message.map(messageToSpan)}
           </li>
 }

function messageToSpan(m, i) {
    if (m.type === "write")
        return <span key={i}>{m.body}</span>
    if (m.type === "delete")
        return <s key={i}>{m.body}</s>
    else
        return <span key={i}>ERROR</span>
}
