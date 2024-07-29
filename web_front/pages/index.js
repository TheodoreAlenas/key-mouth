import sayHi from '../../a_feature/say_hi.mjs'
import { useState } from "react"

export default function Home() {
    let [s, ss] = useState(
        [{name: "Sotiris", msg: "Hi Mark"},
         {name: "Sotiris", msg: "Are you there?"}])
    return (
        <>
            <h1>{sayHi()}</h1>
            <table>
                <tbody>
                  {s.map(e => <tr><td>{e.name}</td><td>{e.msg}</td></tr>)}
                </tbody>
            </table>
            <section>
                <ul>
                    <li>Hi Mark</li>
                    <li>Are you there?</li>
                </ul>
            </section>
            <input type="text" />
            <button onClick={function() {ss([])}}>Send and clear</button>
        </>)
}
