import bubSt from './bubbleList.module.css'
import shapes from './shapes.module.css'
import Link from "next/link"
import { useEffect, useState } from "react"

export default function RoomList({rooms}) {
    if (rooms === null) return <code>Loading...</code>
    return (
        <main className={shapes.thinCentered} style={{backgroundColor: "var(--bg-pale)"}}>
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
