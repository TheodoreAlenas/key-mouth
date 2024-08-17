import shapes from './shapes.module.css'
import colors from './colors.module.css'
import React, { useEffect, useState } from "react"

export default function Moments({o}) {
    const [state, setState] = useState({atBottom: true, moments: []})
    useEffect(function() {
        if (state.atBottom) scrollToBottom()
    }, [state])
    if (o === null || o === undefined) {
        return <code>{"Loading..."}</code>
    }
    o.setSetMoments(function(v) {
        setState({atBottom: getIsAtBottom(), moments: v})
    })
    let finalPres = <code>{"ERROR"}</code>
    try {
        const pres = state.moments.map(momentAndIdToUl)
        finalPres = pres
    }
    catch (err) {
        console.error("couldn't present:")
        console.error(state.moments)
        console.error(err)
    }
    return <section className={shapes.stretch}>{finalPres}</section>
}

function getIsAtBottom() {
    const visible = window.innerHeight
    const above = Math.floor(window.scrollY)
    const all = document.body.scrollHeight
    return visible + above + 5 > all
}

function scrollToBottom() {
    window.scrollTo({
        top: document.body.scrollHeight
    })
}

function momentAndIdToUl(momentAndId) {
    try {
        const m = momentAndId
        if (m.length === 0) return
        return (
            <React.Fragment key={m.key}>
                <ul className={shapes.bubbleGroupSpacing + ' ' +
                               shapes.noBullets + ' ' +
                               colors.moment}>
                    {m.body.map(personToLi)}
                </ul>
                <h2 className={shapes.time}>time</h2>
            </React.Fragment>
        )
    }
    catch (e) {
        console.error("error rendering moment and id:")
        console.error(momentAndId)
        throw e
    }
}

function personToLi(person, i) {
    try {
        return <li id={person.id} key={i}>
                   <pre className={colors.bubble + ' ' +
                                   shapes.bubble}>
                       <strong key="name">{person.name + ': '}</strong>
                       {person.message.map(pieceToSpan)}
                   </pre>
               </li>
    }
    catch (e) {
        console.error("error rendering person " + i + ':')
        console.error(person)
        throw e
    }
 }

function pieceToSpan(piece, i) {
    if (piece.type === "write") {
        return <span key={i}>{piece.body}</span>
    }
    if (piece.type === "delete") {
        return <del className={colors.delete + ' ' + shapes.delete}
                    key={i}>{piece.body}</del>
    }
    if (piece.type === "erase") {
        return <del className={colors.erase + ' ' + shapes.erase}
                    key={i}>{piece.body}</del>
    }
    else return <span key={i}>ERROR</span>
}
