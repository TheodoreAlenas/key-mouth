import Link from 'next/link'
import { useEffect, useState } from "react"

export default function Layout({io, styles, children}) {
    const [rooms, setRooms] = useState(null)
    useEffect(function() {
        io.withRooms(setRooms)
    }, [])

    const anchors = {
        ham: <a id="ham" href="#menu"
                className={styles.hamburger + ' ' + styles.link}
             >Menu</a>,
        chat: <a id="menu" href="#chat-input">Back to chat</a>,
    }
    const github = "https://github.com/TheodoreAlenas/key-mouth"

    const f = (title, lis) => (
        <>
            <h2 className={styles.barTitle}>{title}</h2>
            <ul className={styles.barList}>
                {lis.map((e, i) => <li key={i}>{e}</li>)}
            </ul>
        </>
    )

    return <div className={styles.layout}>
               {anchors.ham}
               <nav className={styles.bar + ' ' + styles.links}>
                   {f("App", [anchors.chat,
                              <a href={github}>GitHub</a>,
                              <ThemeToggle styles={styles} />])}
                   {f("Chat rooms", getRoomLinks(rooms))}
               </nav>
               <main className={styles.main}>
                   {children}
               </main>
           </div>
}


function getRoomLinks(rooms) {
    if (rooms === null) return [<code>Loading...</code>]
    if (rooms === 'error') return [<code>Error</code>]
    return rooms.map(s => <Link href={s.href}>{s.text}</Link>)
}

function ThemeToggle({styles}) {
    useEffect(function() {
        initColorScheme()
    }, [])
    return <button className={styles.button}
                   onClick={switchColorScheme}
           >Switch light/dark theme</button>
}

const lsKey = {
    pref: "keyMouth_colorScheme_lastPreferred",
    last: "keyMouth_colorScheme_last"
}

function initColorScheme() {
    const prefersDark = window.matchMedia('(prefers-color-scheme: dark)').matches;
    const preferred = prefersDark ? "dark" : "light";
    const lastPreferred = localStorage.getItem(lsKey.pref);
    localStorage.setItem(lsKey.pref, preferred);

    if (lastPreferred === preferred && localStorage.getItem(lsKey.last))
        setColorScheme(localStorage.getItem(lsKey.last));
    else
        setColorScheme(preferred);
}

function switchColorScheme() {
    if (localStorage.getItem(lsKey.last) === "dark")
        setColorScheme("light");
    else
        setColorScheme("dark");
}
function setColorScheme(value) {
    document.querySelector("html").style.colorScheme = value;
    document.querySelector("html").setAttribute("data-sch", value);
    localStorage.setItem(lsKey.last, value);
}
