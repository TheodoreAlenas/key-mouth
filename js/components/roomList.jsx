import shapes from './shapes.module.css'
import colors from './colors.module.css'
import Link from "next/link"

export default function RoomList({rooms}) {
    let inside = <code>Error</code>
    if (rooms === null) inside = <code>Loading...</code>
    else if (rooms === 'error') inside = <code>Error</code>
    else inside = rooms.map(roomToLiLink)

    return (
        <main className={shapes.bg + ' ' + colors.bg}>
            <h1 style={{textAlign: "center"}}>Rooms</h1>
            <ul className={shapes.bubbleGroupSpacing + ' ' +
                           shapes.noBullets + ' ' +
                           colors.links + ' ' +
                           shapes.links}
            >{inside}</ul>
        </main>
    )
}

function roomToLiLink(s, i) {
    return <li key={i}>
               <Link className={colors.bubble + ' ' +
                                shapes.bubble}
                     href={s.href}
               >{s.text}</Link>
           </li>
}
