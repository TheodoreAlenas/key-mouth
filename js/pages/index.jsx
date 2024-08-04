import initSocketReturnTeardown from '../mod/socket.js'
import { useEffect, useRef, useState } from "react"

export default function Home({env}) {
    const [inputValue, setInputValue] = useState('')
    const [oldMoments, setOldMoments] = useState([])
    const [lastMoment, setLastMoment] = useState([])
    const defaultHooks = {
        onSubmit: function(e) {e.preventDefault},
        onChange: function() {}
    }
    const [hooks, setHooks] = useState(defaultHooks)
    useEffect(function() {
        return initSocketReturnTeardown(
            {env, setInputValue, setOldMoments, setLastMoment},
            function(unlocked) {
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
    }, [])
    return (
        <>
            <ul>{oldMoments.concat(lastMoment).map(momentToLiUl)}</ul>
            <form onSubmit={hooks.onClear}>
                <input
                    type="text"
                    value={inputValue}
                    onChange={hooks.onChange}
                />
                <button type="submit">Clear</button>
            </form>
        </>)
}

function momentToLiUl(m, i) {
    return <li key={i}><ul>{m.map(personToLi)}</ul></li>
}

function personToLi(e, i) {
    return <li id={e.id} key={i}>
               <span key="name">{e.name}</span>
               {': '}
               {e.message.map(pieceToSpan)}
           </li>
 }

function pieceToSpan(m, i) {
    if (m.type === "write")
        return <span key={i}>{m.body}</span>
    if (m.type === "delete")
        return <s key={i}>{m.body}</s>
    else
        return <span key={i}>ERROR</span>
}

export async function getStaticProps() {
    const env = {
        webSocketUri: "ws://localhost:8000",
        lastMomentsUri: "http://localhost:8000/last"
    }
    return {props: {env}}
}
