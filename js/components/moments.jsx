import styles from './moments.module.css'
import { useEffect, useRef, useState } from "react"

export default function Moments({o}) {
    if (o === null || o === undefined) {
        return <code>{"Loading..."}</code>
    }
    const [moments, setMoments] = useState([])
    o.setSetMoments(setMoments)
    let pres = <code>{"ERROR"}</code>
    try {pres = <>{oldMoments.map(momentToLiUl)}</>}
    catch (e) {}
    return <section className={styles.speechBubbles}>
               {moments.map(momentAndIdToUl)}
           </section>
}

function momentAndIdToUl(momentAndId) {
    const m = momentAndId
    if (m.length === 0) return
    try {
        return <ul key={m.key}>{m.body.map(personToLi)}</ul>
    }
    catch (e) {
        console.error("Error rendering moment " + JSON.stringify(m))
        throw e
    }
}

function personToLi(person, i) {
    return <li id={person.id} key={i}>
               <div className={styles.speechBubble}>
                   <strong key="name">{person.name + ': '}</strong>
                   {person.message.map(pieceToSpan)}
               </div>
           </li>
 }

function pieceToSpan(piece, i) {
    if (piece.type === "write") return <span key={i}>{piece.body}</span>
    if (piece.type === "delete") return <s key={i}>{piece.body}</s>
    else return <span key={i}>ERROR</span>
}
