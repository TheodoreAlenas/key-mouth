import shapes from './shapes.module.css'
import colors from './colors.module.css'
import Link from "next/link"

export default function RoomList({rooms}) {
    if (rooms === null) return <code>Loading...</code>
    return (
        <main className={shapes.thinCentered + ' ' + colors.bgPale + ' ' + shapes.stretch}>
            <h1 style={{textAlign: "center"}}>Rooms</h1>
            <ul className={shapes.bubbleGroupSpacing + ' ' +
                           shapes.noBullets + ' ' +
                           colors.links + ' ' +
                           shapes.links}
            >{rooms.map(roomToLiLink)}</ul>
        </main>
    )
}

function roomToLiLink(s, i) {
    return <li key={i}>
               <Link className={colors.bubbleColors + ' ' +
                                shapes.bubbleSpacing + ' ' +
                                shapes.bubbleWrap}
                     href={s.href}
               >{s.text}</Link>
           </li>
}
