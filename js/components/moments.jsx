import React, { useEffect, useRef, useState } from "react"

export default function Moments({o, styles}) {
    const [state, setState] = useState({atBottom: true, moments: []})
    const ref = useRef(null)
    useEffect(function() {
        if (ref.current && state.atBottom) scrollToBottom(ref.current)
    }, [state])
    if (o === null || o === undefined) {
        return <code>{"Loading..."}</code>
    }
    o.onSocketError = function() {
        setState({atBottom: getIsAtBottom(ref.current), moments: null})
    }
    o.setMoments = function(v) {
        setState({atBottom: getIsAtBottom(ref.current), moments: v})
    }
    let finalPres = <code>{"ERROR"}</code>
    try {
        const pres = state.moments.map(
            moment => MomentToBubble({moment, styles}))
        finalPres = pres
    }
    catch (err) {
        console.error("couldn't present:")
        console.error(state.moments)
        console.error(err)
    }
    return <section ref={ref}
                    className={styles.chat}
           >{finalPres}</section>
}

function getIsAtBottom(element) {
    const visible = element.clientHeight
    const above = Math.floor(element.scrollTop)
    const all = element.scrollHeight
    return visible + above + 5 > all
}

function scrollToBottom(element) {
    element.scrollTop = element.scrollHeight
}

function MomentToBubble({moment, styles}) {
    try {
        const m = moment
        const namesAndCommas = m.names.reduce((a, x) => a + ', ' + x, '')
        const msgs = m.messages.map(
            (person, i) => PersonToLi({person, i, styles}))
        return (
            <React.Fragment key={m.key}>
                <h2 className={styles.bubbleTop}>
                    {(m.time || '') + namesAndCommas}
                </h2>
                <ul className={styles.bubbleGroupSpacing + ' ' +
                               styles.noBullets}>
                    {msgs}
                </ul>
            </React.Fragment>
        )
    }
    catch (e) {
        console.error("error rendering moment:")
        console.error(moment)
        throw e
    }
}

function PersonToLi({person, i, styles}) {
    try {
        return <li id={person.id} key={i}>
                   <pre className={styles.bubble}>
                       {person.message.map(
                           (diff, i) => DiffToSpan({diff, i, styles}))}
                   </pre>
               </li>
    }
    catch (e) {
        console.error("error rendering person " + i + ':')
        console.error(person)
        throw e
    }
 }

function DiffToSpan({diff, i, styles}) {
    if (diff.type === "write") {
        return <span key={i}>{diff.body}</span>
    }
    if (diff.type === "delete") {
        return <del className={styles.delete}
                    key={i}>{diff.body}</del>
    }
    if (diff.type === "erase") {
        return <del className={styles.erase}
                    key={i}>{diff.body}</del>
    }
    if (diff.type === "event") {
        return <code className={styles.event}
                     key={i}>{diff.body}</code>
    }
    else return <code key={i}>ERROR</code>
}
