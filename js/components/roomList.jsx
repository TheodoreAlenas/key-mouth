import Link from "next/link"

export default function RoomList({rooms, styles}) {
    let inside = <code>Error</code>
    if (rooms === null) inside = <code>Loading...</code>
    else if (rooms === 'error') inside = <code>Error</code>
    else inside = rooms.map((s, i) => RoomToLiLink({s, i, styles}))

    return (
        <main className={styles.bg}>
            <h1 style={{textAlign: "center"}}>Rooms</h1>
            <ul className={styles.bubbleGroupSpacing + ' ' +
                           styles.noBullets + ' ' +
                           styles.links}
            >{inside}</ul>
        </main>
    )
}

function RoomToLiLink({s, i, styles}) {
    return <li key={i}>
               <Link className={styles.bubble}
                     href={s.href}
               >{s.text}</Link>
           </li>
}
