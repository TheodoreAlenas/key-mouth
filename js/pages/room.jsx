import Controller from '../mod/Controller.js'
import IoHome from '../mod/io/IoHome.js'
import UriHome from '../mod/io/UriHome.js'
import uriFirstArg from '../mod/io/uriFirstArg.js'
import IoRoom from '../mod/io/IoRoom.js'
import UriRoom from '../mod/io/UriRoom.js'
import Room from '../components/room.jsx'
import Layout from '../components/layout.jsx'
import styles from '../components/styles.module.css'
import { useEffect, useState } from "react"
import { useRouter } from "next/router"

export default function PageRoom({uriFirstArg, maxPages}) {
    const [o, setO] = useState(null)
    const router = useRouter()
    useEffect(function() {
        if (router.isReady) {
            const s = new URLSearchParams(router.query)
            const roomName = s.get('name')
            const uri = new UriRoom(uriFirstArg.room, roomName)
            const newO = new Controller({uri, maxPages})
            setO(newO)
            return function() { newO.close() }
        }
    }, [router.isReady])
    const io = new IoHome({uri: new UriHome(uriFirstArg.home)})
    return <Layout env={uriFirstArg} io={io} styles={styles}>
               <Room o={o} styles={styles} />
           </Layout>
}

export async function getStaticProps() {
    const maxPages = Number(process.env.KEYMOUTH_MAX_PAGES || "10")
    return {props: {uriFirstArg, maxPages}}
}
