import SocketInteractor from '../mod/SocketInteractor.js'
import { useEffect, useRef, useState } from "react"

export default function Home({env}) {
    const [inputValue, setInputValue] = useState('')
    const [oldMoments, setOldMoments] = useState([])
    const [lastMoment, setLastMoment] = useState([])
    const interactorRef = useRef(null)
    useEffect(function() {
        interactorRef.current = new SocketInteractor(
            env, inputValue, setInputValue,
            setOldMoments, setLastMoment)
        return interactorRef.current.getFunctionThatClosesSocket()
    }, [])
    const preventDefClearInp = function(event) {
        event.preventDefault()
        interactorRef.current.onClear()
    }
    const setInpSockSend = function(event) {
        const newValue = event.target.value
        interactorRef.current.onInputChange(newValue)
    }
    return (
        <>
            <ul>{oldMoments.concat(lastMoment).map(messageToInnerUl)}</ul>
            <form onSubmit={preventDefClearInp}>
                <input
                    type="text"
                    value={inputValue}
                    onChange={setInpSockSend}
                />
                <button type="submit">Clear</button>
            </form>
        </>)
}

function messageToInnerUl(m, i) {
    return <li key={i}><ul>{m.map(postToLi)}</ul></li>
}

function postToLi(e, i) {
    return <li id={e.id} key={i}>
               <span key="name">{e.name}</span>
               {': '}
               {e.message.map(messageToSpan)}
           </li>
 }

function messageToSpan(m, i) {
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
