import laySt from './index.module.css'
import bubSt from './bubbleList.module.css'
import Link from "next/link"
import { useEffect, useState } from "react"

export default function RoomList({rooms}) {
    if (rooms === null) return <code>Loading...</code>
    return (
        <main className={laySt.main} style={{backgroundColor: "var(--bg-pale)"}}>
            <h1>Rooms</h1>
            <ul className={bubSt.bubbleList}>{rooms.map(roomToLiLink)}</ul>
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
