import shapes from './shapes.module.css'
import colors from './colors.module.css'
import { useEffect, useState } from "react"

export default function Moments({o}) {
    if (o === null || o === undefined) {
        return <code>{"Loading..."}</code>
    }
    const [state, setState] = useState({atBottom: true, moments: []})
    o.setSetMoments(function(v) {
        setState({atBottom: getIsAtBottom(), moments: v})
    })
    useEffect(function() {
        if (state.atBottom) scrollToBottom()
    }, [state])
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
    const d = {
        'document.body.scrollHeight': document.body.scrollHeight,
        'document.body.offsetHeight': document.body.offsetHeight,
        'window.innerHeight': window.innerHeight,
        'Math.floor(window.scrollY)': Math.floor(window.scrollY)
    }
    return <pre>
               {"\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n"}
               {JSON.stringify(d, null, 2)}
           </pre>
//    return <section className={shapes.stretch}>{finalPres}</section>
}

function getIsAtBottom() {
    const e = document.documentElement
    const visiblePlusAboveIt = e.clientHeight + window.scrollY
    const allOfIt = e.scrollHeight
    return visiblePlusAboveIt === allOfIt
}

function scrollToBottom() {
    window.scrollTo({
        top: document.documentElement.scrollHeight
    })
}

function momentAndIdToUl(momentAndId) {
    try {
        const m = momentAndId
        if (m.length === 0) return
        return <ul key={m.key}
                   className={shapes.bubbleGroupSpacing + ' ' +
                              shapes.noBullets}>
                   {m.body.map(personToLi)}
               </ul>
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
                   <div className={colors.bubbleColors + ' ' +
                                   shapes.bubbleSpacing + ' ' +
                                   shapes.bubbleWrap}>
                       <strong key="name">{person.name + ': '}</strong>
                       {person.message.map(pieceToSpan)}
                   </div>
               </li>
    }
    catch (e) {
        console.error("error rendering person " + i + ':')
        console.error(person)
        throw e
    }
 }

function pieceToSpan(piece, i) {
    if (piece.type === "write") return <span key={i}>{piece.body}</span>
    if (piece.type === "delete") return <s key={i}>{piece.body}</s>
    else return <span key={i}>ERROR</span>
}
