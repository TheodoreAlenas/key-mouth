import WebInteractor from '../mod/WebInteractor.js'
import UriRoom from '../mod/UriRoom.js'
import uriFirstArg from '../mod/uriFirstArg.js'
import Room from '../components/room.jsx'
import Layout from '../components/layout.jsx'
import { useEffect, useRef, useState } from "react"
import { useRouter } from "next/router"

export default function PageRoom({env}) {
    const [o, setO] = useState(null)
    const router = useRouter()
    useEffect(function() {
        if (router.isReady) {
            const s = new URLSearchParams(router.query)
            const roomName = s.get('name')
            const uri = new UriRoom(env.room, roomName)
            const newO = new WebInteractor(uri)
            setO(newO)
            return newO.getDestructor()
        }
    }, [router.isReady])
    return <Layout env={env} showHome>
               <Room o={o} />
           </Layout>
}

export async function getStaticProps() {
    return {props: {env: uriFirstArg}}
}
