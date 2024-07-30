import sayHi from '../../a_feature/say_hi.mjs'
import { useEffect, useState } from "react"

export default function Home() {
    let [messages, setMessages] = useState(
        [{name: "Sotiris", message: "Hi Mark"},
         {name: "Sotiris", message: "Are you there?"}])
    const messageInputID = "message-input"
    useEffect(function() {
        console.log("start")
        const s = new WebSocket("ws://localhost:8000")
        const d = "date is " + Date.now()
        s.addEventListener("open", function(event) {
            s.send(d)
        })
        s.addEventListener("message", function(event) {
            if (event.data === "Message was " + d) console.log("same")
            else console.log("different")
        })

        keyScan("")
        return function() {
            keyScannerStop = true
            console.log("end")
            s.close()
        }
    }, [])
    return (
        <>
            <h1>{sayHi()}</h1>
            <table>
                <tbody>
                    { messages.map((e, i) =>
                        <tr key={i}>
                            <td key="name">{e.name}</td>
                            <td key="message">{e.message}</td>
                        </tr>) }
                </tbody>
            </table>
            <input id={ messageInputID } type="text" />
            <button onClick={ function() { setMessages([]); keyScannerStop = true } }
            >Send and clear</button>
        </>)
}

let keyScannerStop = false

function keyScan(prev) {
    if (keyScannerStop) {
        keyScannerStop = false
    }
    else {
        setTimeout(function() { keyScan(keyScanPure(prev)) }, 1000)
    }
}

function keyScanPure(prev) {
    console.log(prev)
    return prev + "."
}
