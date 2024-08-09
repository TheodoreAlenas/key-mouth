import WebInteractor from '../mod/WebInteractor.js'
import UriRoom from '../mod/UriRoom.js'
import uriFirstArg from '../mod/uriFirstArg.js'
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
            const uri = new UriRoom(env.room, roomName)
            const newO = new WebInteractor(uri)
            setO(newO)
            return newO.getDestructor()
        }
    }, [router.isReady])
    return <Layout env={env}>
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
    return {props: {env: uriFirstArg}}
}
