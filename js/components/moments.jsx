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
    o.setMoments = function(v) {
        setState({atBottom: getIsAtBottom(), moments: v})
    }
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
                {m.time ? <h2 className={shapes.time}>{m.time}</h2> :''}
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
                       {person.message.map(diffToSpan)}
                   </pre>
               </li>
    }
    catch (e) {
        console.error("error rendering person " + i + ':')
        console.error(person)
        throw e
    }
 }

function diffToSpan(diff, i) {
    if (diff.type === "write") {
        return <span key={i}>{diff.body}</span>
    }
    if (diff.type === "delete") {
        return <del className={colors.delete + ' ' + shapes.delete}
                    key={i}>{diff.body}</del>
    }
    if (diff.type === "erase") {
        return <del className={colors.erase + ' ' + shapes.erase}
                    key={i}>{diff.body}</del>
    }
    if (diff.type === "event") {
        return <code key={i}>{diff.body}</code>
    }
    else return <code key={i}>ERROR</code>
}
