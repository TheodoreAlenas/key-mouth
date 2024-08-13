import shapes from './shapes.module.css'
import colors from './colors.module.css'
import UriHome from '../mod/UriHome.js'
import Link from 'next/link'
import { useEffect, useState } from "react"

export default function Layout({ env, showHome, children }) {
    const uri = new UriHome(env.home, 'ERROR, LAYOUT HAS NO ROOM')
    return <>
               <nav className={shapes.menuWrapper + ' ' +
                               colors.menuWrapper}>
                   <ul className={shapes.menu}>
                       {showHome ? <li><HomeLink uri={uri} /></li> : ''}
                       <li><ThemeToggle /></li>
                   </ul>
               </nav>
               {children}
           </>
}

function HomeLink({uri}) {
    return <Link href={uri.home()}
                 className={colors.link + ' ' +
                            shapes.link}
    >Home</Link>
}

function ThemeToggle() {
    useEffect(function() {
        initColorScheme()
    }, [])
    return <button className={shapes.button + ' ' +
                              colors.button}
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
