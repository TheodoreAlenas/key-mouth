
import Link from "next/link"

export default function Home({env}) {
    const ss = [
        {text: "Zero",  href: env.sessionUri + "?id=0"},
        {text: "Hello", href: env.sessionUri + "?id=hello"}
    ]
    return (
        <>
            <h1>Sessions</h1>
            <ul>{ss.map(sessionToLiLink)}</ul>
        </>
    )
}

function sessionToLiLink(s, i) {
    return <li key={i}><Link href={s.href}>{s.text}</Link></li>
}

export async function getStaticProps() {
    const env = {
        sessionUri: "http://localhost:3000/session"
    }
    return {props: {env}}
}
