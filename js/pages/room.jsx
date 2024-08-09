import WebInteractor from '../mod/WebInteractor.js'
import Uri from '../mod/Uri.js'
import styles from './room.module.css'
import Moments from '../components/moments.jsx'
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
               <main className={styles.main + ' ' + styles.bgPale}>
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
                         styles.messengerInputForm + ' ' +
                         styles.bgPale}>
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
