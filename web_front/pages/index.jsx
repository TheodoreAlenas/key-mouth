import sayHi from '../../a_feature/say_hi.mjs'
import { useState } from "react"

export default function Home() {
    let [messages, setMessages] = useState(
        [{name: "Sotiris", msg: "Hi Mark"},
         {name: "Sotiris", msg: "Are you there?"}])
    return (
        <>
            <h1>{sayHi()}</h1>
            <table>
                <tbody>
                    { messages.map(e =>
                        <tr><td>{e.name}</td><td>{e.msg}</td></tr>) }
                </tbody>
            </table>
            <input type="text" />
            <button onClick={ function() {setMessages([])} }
            >Send and clear</button>
        </>)
}
