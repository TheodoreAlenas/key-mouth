import UriHome from '../mod/UriHome.js'
import laySt from './index.module.css'
import bubSt from '../components/bubbleList.module.css'
import uriFirstArg from '../mod/uriFirstArg.js'
import Link from "next/link"

export default function Home({env}) {
    const uri = new UriHome(env.home)
    const ss = [
        {text: "Zero",  href: uri.room("0")},
        {text: "Hello", href: uri.room("hello")}
    ]
    return (
        <main className={laySt.main} style={{backgroundColor: "var(--bg-pale)"}}>
            <h1>Rooms</h1>
            <ul className={bubSt.bubbleList}>{ss.map(roomToLiLink)}</ul>
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
