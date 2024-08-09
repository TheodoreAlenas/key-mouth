import WebInteractor from '../mod/WebInteractor.js'
import Uri from '../mod/Uri.js'
import styles from './room.module.css'
import Moments from '../components/moments.jsx'
import InputAndButton from '../components/inputAndButton.jsx'
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
                   <InputAndButton
                       o={o}
                       className={styles.bgPale + ' ' +
                                  styles.stickyBottom} />
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
