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

        prevInputBoxValue = document.getElementById(messageInputID).value
        return function() {
            console.log("end")
            s.close()
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
            <input id={ messageInputID } type="text" onChange={ function() {
                       const v = document.getElementById(messageInputID).value
                       console.log(diff(prevInputBoxValue, v))
                       prevInputBoxValue = v
                   } } />
            <button onClick={ function() { setMessages([]) } }
            >Send and clear</button>
        </>)
}

let prevInputBoxValue = ""

function diff(a, b) {
    if (b.startsWith(a)) {
        return b.substr(a.length)
    }
    if (a.startsWith(b)) {
        return a.length - b.length
    }
    return { a, b }
}
