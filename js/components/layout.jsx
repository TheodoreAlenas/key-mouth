import UriHome from '../mod/UriHome.js'

export default function Layout({ env, children }) {
    const uri = new UriHome(env.home, 'ERROR, LAYOUT HAS NO ROOM')
    return <>
               <a href={uri.home()}>Home</a>
               {children}
           </>
}
