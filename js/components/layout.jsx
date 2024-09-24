import UriHome from '../mod/io/UriHome.js'
import Link from 'next/link'
import { useEffect } from "react"

export default function Layout({env, styles, showHome, children}) {
    const uri = new UriHome(env.home, 'ERROR, LAYOUT HAS NO ROOM')
    if (showHome) {
        return <div className={styles.layout}>
                   <Wrapper styles={styles}>
                       <li><HomeLink uri={uri} styles={styles} /></li>
                   </Wrapper>
                   <main className={styles.main}>
                       {children}
                   </main>
               </div>
    }
    return <>
               <Wrapper styles={styles} />
               {children}
           </>

}

function Wrapper({styles, children}) {
    return <nav className={styles.barContainer}>
               <ul className={styles.bar}>
                   {children}
                   <li><ThemeToggle styles={styles} /></li>
               </ul>
           </nav>
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
