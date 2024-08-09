import WebInteractor from '../mod/WebInteractor.js'
import Uri from '../mod/Uri.js'
import styles from './room.module.css'
import Layout from '../components/layout.jsx'
import { useEffect, useRef, useState } from "react"
import { useRouter } from "next/router"

export default function Home({env}) {
    const [o, setO] = useState(null)
    const router = useRouter()
    useEffect(function() {
        if (router.isReady) {
            const s = new URLSearchParams(router.query)
            const roomName = s.get('name')
            const uri = new Uri(env, roomName)
            const newO = new WebInteractor(uri)
            setO(newO)
            return newO.getDestructor()
        }
    }, [router.isReady])
    return <Layout>
               <main className={styles.main}>
                   <Moments o={o} />
                   <InputAndButton o={o} />
               </main>
           </Layout>
}

export async function getStaticProps() {
    if (process.env.KEYMOUTH_PROD === undefined) {
        return {props: {env: ["http", "localhost", "8000"]}}
    }
    return {props: {env: [
        process.env.KEYMOUTH_HTTP,
        process.env.KEYMOUTH_HOST,
        process.env.KEYMOUTH_PORT
    ]}}
}

function Moments({o}) {
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

function InputAndButton({o}) {
    const defaultHooks = {
        onSubmit: function(e) {e.preventDefault},
        onChange: function() {}
    }
    const [hooks, setHooks] = useState(defaultHooks)
    if (o !== null) {
        o.setOnReadySocket(function(unlocked) {
            setHooks({
                onClear: function(event) {
                    event.preventDefault()
                    unlocked.onClear()
                },
                onChange: function(event) {
                    const t = event.target
                    t.style.height = 'auto'
                    t.style.height = t.scrollHeight + 'px'
                    unlocked.onInputChange(t.value)
                }
            })
        })
    }
    return (
        <form onSubmit={hooks.onClear}
              className={styles.stickyBottom + ' ' +
                         styles.messengerInputForm}>
            <Input o={o} onChange={hooks.onChange} />
            <button className="clearButton" type="submit">Clear</button>
        </form>
    )
}

function Input({o, onChange}) {
    const [inputValue, setInputValue] = useState('')
    if (o !== null) o.setSetInputValue(setInputValue)
    const inpRef = useRef(null)
    useEffect(function() {
        const t = inpRef.current
        t.style.height = 'auto'
        t.style.height = t.scrollHeight + 'px'
    }, [])
    return (
        <div className={styles.messengerInputContainer}>
            <textarea
                ref={inpRef}
                name="message"
                placeholder="Each key will be sent"
                className={styles.messengerInput}
                value={inputValue}
                onChange={onChange}
            />
        </div>
    )
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
