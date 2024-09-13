import Controller from '../mod/Controller.js'
import UriRoom from '../mod/UriRoom.js'
import uriFirstArg from '../mod/uriFirstArg.js'
import Room from '../components/room.jsx'
import Layout from '../components/layout.jsx'
import styles from '../components/styles.module.css'
import { useEffect, useState } from "react"
import { useRouter } from "next/router"

export default function PageRoom({env, pageSize}) {
    const [o, setO] = useState(null)
    const router = useRouter()
    useEffect(function() {
        if (router.isReady) {
            const s = new URLSearchParams(router.query)
            const roomName = s.get('name')
            const uri = new UriRoom(env.room, roomName)
            const newO = new Controller(uri, pageSize)
            setO(newO)
            return function() { newO.close() }
        }
    }, [router.isReady])
    return <Layout env={env} styles={styles} showHome>
               <Room o={o} styles={styles} />
           </Layout>
}

export async function getStaticProps() {
    const pageSize = process.env.KEYMOUTH_PAGE_SIZE || 50
    return {props: {env: uriFirstArg, pageSize}}
}
