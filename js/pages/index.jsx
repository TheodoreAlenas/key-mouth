import UriHome from '../mod/UriHome.js'
import uriFirstArg from '../mod/uriFirstArg.js'
import Link from "next/link"

export default function Home({env}) {
    const uri = new UriHome(env.home)
    const ss = [
        {text: "Zero",  href: uri.room("0")},
        {text: "Hello", href: uri.room("hello")}
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
    return {props: {env: uriFirstArg}}
}
