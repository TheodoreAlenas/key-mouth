import shapes from './shapes.module.css'
import colors from './colors.module.css'
import UriHome from '../mod/UriHome.js'

export default function Layout({ env, children }) {
    const uri = new UriHome(env.home, 'ERROR, LAYOUT HAS NO ROOM')
    return <>
               <a href={uri.home()}
                  className={shapes.stickyTop + ' ' +
                             shapes.tmpCenter + ' ' +
                             colors.link + ' ' +
                             shapes.link}
               >Home</a>
               {children}
           </>
}
