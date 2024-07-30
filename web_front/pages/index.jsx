import sayHi from '../../a_feature/say_hi.mjs'
import { useEffect, useRef, useState } from "react"

export default function Home() {
    const [inputValue, setInputValue] = useState('')
    const preventDefClearInp = function(event) {
        event.preventDefault()
        setInputValue("")
        socketRef.current.send("cleared")
    }
    const f = function(event) {
        const v = event.target.value
        setInputValue(v)
        socketRef.current.send(v)
    }
    let [messages, setMessages] = useState(
        [{name: "Sotiris", message: "Hi Mark"},
         {name: "Sotiris", message: "Are you there?"}])
    const inputId = "message-input"
    const socketRef = useRef(null)
    useEffect(function() {
        console.log("start")
        socketRef.current = new WebSocket("ws://localhost:8000")
        const d = "date is " + Date.now()
        socketRef.current.addEventListener("open", function(event) {
            socketRef.current.send(d)
        })
        socketRef.current.addEventListener("message", function(event) {
            if (event.data === "Message was " + d) console.log("same")
            else console.log("different: " + event.data)
        })
        return function() {
            console.log("end")
            socketRef.current.close()
        }
    }, [])
    return (
        <>
            <h1>{sayHi()}</h1>
            <table>
                <tbody>
                    {
                        messages.map((e, i) =>
                            <tr key={i}>
                                <td key="name">{e.name}</td>
                                <td key="message">{e.message}</td>
                            </tr>
                        )
                    }
                </tbody>
            </table>
            <form onSubmit={preventDefClearInp}>
                <input
                    type="text"
                    value={inputValue}
                    onChange={f}
                />
                <button type="submit">Clear</button>
            </form>
        </>)
}