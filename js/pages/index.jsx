
import Link from "next/link"

export default function Home({env}) {
    const ss = [
        {text: "Zero",  href: env.roomUri + "?id=0"},
        {text: "Hello", href: env.roomUri + "?id=hello"}
    ]
    return (
        <>
            <h1>Rooms</h1>
            <ul>{ss.map(roomToLiLink)}</ul>
        </>
    )
}

function roomToLiLink(s, i) {
    return <li key={i}><Link href={s.href}>{s.text}</Link></li>
}

export async function getStaticProps() {
    const env = {
        roomUri: "http://localhost:3000/room"
    }
    return {props: {env}}
}
