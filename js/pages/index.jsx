import UriHome from '../mod/UriHome.js'
import laySt from './index.module.css'
import bubSt from '../components/bubbleList.module.css'
import uriFirstArg from '../mod/uriFirstArg.js'
import Link from "next/link"
import { useEffect, useState } from "react"

export default function Home({env}) {
    const uri = new UriHome(env.home)
    const [rooms, setRooms] = useState(<code>Loading...</code>)
    useEffect(function() {
        const with200 = fetch(uri.rooms()).then(function(res) {
            if (res.status !== 200) {
                setRooms(<code>ERROR</code>)
                throw new Error("couldn't fetch " + uri.rooms())
            }
            return res.json()
        })
        with200.catch(function(err) {
            console.error("can't JSON parse response of " + uri.rooms())
            throw err
        })
        with200.then(function(json) {
            setRooms(
                json.map(e => ({text: e, href: uri.room(e)}))
                    .map(roomToLiLink)
            )
        })
    }, [])
    return (
        <main className={laySt.main} style={{backgroundColor: "var(--bg-pale)"}}>
            <h1>Rooms</h1>
            <ul className={bubSt.bubbleList}>{rooms}</ul>
        </main>
    )
}

function roomToLiLink(s, i) {
    return <li key={i}>
               <Link className={bubSt.bubbleListItem}
                     href={s.href}
               >{s.text}</Link>
           </li>
}

export async function getStaticProps() {
    return {props: {env: uriFirstArg}}
}
