import UriHome from '../mod/io/UriHome.js'
import Link from 'next/link'
import { useEffect, useState } from "react"

export default function Layout({io, styles, children}) {
    const [rooms, setRooms] = useState(null)
    useEffect(function() {
        io.withRooms(setRooms)
    }, [])
    const uri = io.uri

    return <div className={styles.layout}>
               <a id="ham" href="#menu" className={styles.hamburger}
               >Menu</a>
               <nav className={styles.bar + ' ' + styles.links}>
                   <h2 className={styles.barTitle}>Resume</h2>
                   <ul className={styles.barList}>
                       <li><a id="menu" href="#ham">Back to chat</a></li>
                       <li><a href="#chat-input">Stream typing</a></li>
                   </ul>
                   <h2 className={styles.barTitle}>App</h2>
                   <ul className={styles.barList}>
                       <li><a href="https://github.com/TheodoreAlenas/key-mouth">GitHub</a></li>
                       <li><ThemeToggle styles={styles} /></li>
                   </ul>
                   <h2 className={styles.barTitle}>Chat rooms</h2>
                   <ul className={styles.barList}>
                       {RoomList({styles, rooms})}
                   </ul>
               </nav>
               <main className={styles.main}>                   
                   {children}
               </main>
           </div>
}

function RoomList({styles, rooms}) {
    let inside = <code>Error</code>
    if (rooms === null) inside = <code>Loading...</code>
    else if (rooms === 'error') inside = <code>Error</code>
    else inside = rooms.map((s, i) => RoomToLiLink({s, i, styles}))
    return <>{inside}</>
}

function RoomToLiLink({s, i, styles}) {
    return <li key={i}><Link href={s.href}>{s.text}</Link></li>
}

function HomeLink({uri, styles}) {
    return <Link href={uri.home()}
                 className={styles.link}
    >Home</Link>
}

function ThemeToggle({styles}) {
    useEffect(function() {
        initColorScheme()
    }, [])
    return <button className={styles.button}
                   onClick={switchColorScheme}
           >Switch light/dark theme</button>
}

function initColorScheme() {
    const prefersDark = window.matchMedia('(prefers-color-scheme: dark)').matches;
    const preferred = prefersDark ? "dark" : "light";
    const lastPreferred = localStorage.getItem("lastPreferredColorScheme");
    localStorage.setItem("lastPreferredColorScheme", preferred);

    if (lastPreferred === preferred && localStorage.getItem("lastColorScheme"))
        setColorScheme(localStorage.getItem("lastColorScheme"));
    else
        setColorScheme(preferred);
}

function switchColorScheme() {
    if (localStorage.getItem("lastColorScheme") === "dark")
        setColorScheme("light");
    else
        setColorScheme("dark");
}
function setColorScheme(value) {
    document.querySelector("html").style.colorScheme = value;
    document.querySelector("html").setAttribute("data-sch", value);
    localStorage.setItem("lastColorScheme", value);
}
