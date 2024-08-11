import styles from './bubbleList.module.css'
import { useEffect, useMemo, useRef, useState } from "react"

export default function Moments({o}) {
    if (o === null || o === undefined) {
        return <code>{"Loading..."}</code>
    }
    const [state, setState] = useState({atBottom: true, moments: []})
    o.setSetMoments(function(v) {
        console.log("o sets the moments to:")
        console.log(v)
        setState({atBottom: getIsAtBottom(), moments: v})
    })
    useEffect(function() {
        console.log("useEffect calls the function")
        if (state.atBottom) scrollToBottom()
    }, [state])
    let pres = <code>{"ERROR"}</code>
    return <section>{state.moments.map(momentAndIdToUl)}</section>
}

function getIsAtBottom() {
    const e = document.documentElement
    const visiblePlusAboveIt = e.clientHeight + window.scrollY
    const allOfIt = e.scrollHeight
    console.log({
        clientHeight: e.clientHeight,
        scrollY: window.scrollY,
        scrollHeight: e.scrollHeight,
        willReturn: (visiblePlusAboveIt === allOfIt)
    })
    return visiblePlusAboveIt === allOfIt
}

function scrollToBottom() {
    console.log("scrollToBottom called")
    window.scrollTo({
        top: document.documentElement.scrollHeight
    })
    console.log("scrollY is now: " + window.scrollY)
}

function momentAndIdToUl(momentAndId) {
    const m = momentAndId
    if (m.length === 0) return
    try {
        return <ul key={m.key} className={styles.bubbleList}>
                   {m.body.map(personToLi)}
               </ul>
    }
    catch (e) {
        console.error("Error rendering moment " + JSON.stringify(m))
        throw e
    }
}

function personToLi(person, i) {
    return <li id={person.id} key={i}>
               <div className={styles.bubbleListItem}>
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
