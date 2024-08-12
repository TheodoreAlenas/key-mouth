import shapes from './shapes.module.css'
import colors from './colors.module.css'
import UriHome from '../mod/UriHome.js'
import Link from 'next/link'

export default function Layout({ env, showHome, children }) {
    const uri = new UriHome(env.home, 'ERROR, LAYOUT HAS NO ROOM')
    return <>
               <nav className={shapes.stickyTop + ' ' + shapes.stretch}>
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
    return <button className={shapes.button + ' ' +
                              colors.button}
           >Switch light/dark theme</button>
}
