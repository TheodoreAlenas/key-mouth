import WebInteractor from '../mod/WebInteractor.js'
import Uri from '../mod/Uri.js'
import { useEffect, useState } from "react"
import { useRouter } from "next/router"

export default function Home({env}) {
    const [o, setO] = useState(null)
    const router = useRouter()
    useEffect(function() {
        if (router.isReady) {
            const s = new URLSearchParams(router.query)
            const newO = new WebInteractor(env, s.get('name'))
            setO(newO)
            return newO.getDestructor()
        }
    }, [router.isReady])
    return <><Moments o={o} /><Input o={o} /></>
}

export async function getStaticProps() {
    const env = {
        webSocketUri: "ws://localhost:8000",
        lastMomentsUri: "http://localhost:8000/last",
        momentsRangeUri: "http://localhost:8000/moments"
    }
    return {props: {env}}
}

function Moments({o}) {
    if (o === null || o === undefined) {
        return <>{"Loading..."}</>
    }
    return <ul><OldMoments o={o} /><LastMoment o={o} /></ul>
}

function OldMoments({o}) {
    const [oldMoments, setOldMoments] = useState([])
    o.setSetOldMoments(setOldMoments)
    try {
        return <>{oldMoments.map(momentToLiUl)}</>
    }
    catch (e) {
        console.error("Error rendering the old moments")
        console.error(e.message)
        return <code>{"ERROR"}</code>
    }
}

function LastMoment({o}) {
    const [lastMoment, setLastMoment] = useState([])
    o.setSetLastMoment(setLastMoment)
    try {
        return <>{momentToLiUl(lastMoment)}</>
    }
    catch (e) {
        console.error("Error rendering the last moment")
        console.error(e.message)
        return <code>{"ERROR"}</code>
    }
}

function Input({o}) {
    const [inputValue, setInputValue] = useState('')
    const defaultHooks = {
        onSubmit: function(e) {e.preventDefault},
        onChange: function() {}
    }
    const [hooks, setHooks] = useState(defaultHooks)
    if (!(o === null || o === undefined)) {
        o.setSetInputValue(setInputValue)
        o.setOnReadySocket(function(unlocked) {
            setHooks({
                onClear: function(event) {
                    event.preventDefault()
                    unlocked.onClear()
                },
                onChange: function(event) {
                    unlocked.onInputChange(event.target.value)
                }
            })
        })
    }
    return (
        <form onSubmit={hooks.onClear}>
            <input
                type="text"
                value={inputValue}
                onChange={hooks.onChange}
            />
            <button type="submit">Clear</button>
        </form>
    )
}

function momentToLiUl(moment, i) {
    if (moment.length === 0) return
    try {
        return <li key={i}><ul>{moment.map(personToLi)}</ul></li>
    }
    catch (e) {
        console.error("Error rendering moment " + JSON.stringify(moment))
        throw e
    }
}

function personToLi(person, i) {
    return <li id={person.id} key={i}>
               <span key="name">{person.name}</span>
               {': '}
               {person.message.map(pieceToSpan)}
           </li>
 }

function pieceToSpan(piece, i) {
    if (piece.type === "write") return <span key={i}>{piece.body}</span>
    if (piece.type === "delete") return <s key={i}>{piece.body}</s>
    else return <span key={i}>ERROR</span>
}
